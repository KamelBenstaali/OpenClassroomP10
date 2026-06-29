import azure.functions as func
import logging
import json
import pickle
import os
import io
import numpy as np
import pandas as pd
import implicit
import scipy.sparse as sparse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from azure.storage.blob import BlobServiceClient

# Modèle de programmation V2
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# ==========================================
# 1. CHARGEMENT GLOBAL DES MODÈLES (COLD START)
# ==========================================
logging.info("Démarrage du Cold Start : Téléchargement des modèles depuis Azure Blob Storage...")

# On récupère la chaîne de connexion depuis les variables d'environnement d'Azure
# Assure-toi d'ajouter 'AZURE_STORAGE_CONNECTION_STRING' dans ton portail Azure
CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "models" # Nom du conteneur dans ton Blob Storage

try:
    if not CONNECTION_STRING:
        raise ValueError("La variable d'environnement AZURE_STORAGE_CONNECTION_STRING est manquante !")
        
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    
    def load_blob_to_memory(blob_name):
        logging.info(f"Téléchargement de {blob_name}...")
        return container_client.download_blob(blob_name).readall()

    # 1. Historiques Utilisateurs
    user_histories_dict = pickle.loads(load_blob_to_memory("user_histories_dict.pkl"))
        
    # 2. ALS Model & Mappings
    user_factors = np.load(io.BytesIO(load_blob_to_memory("als_user_factors.npy")))
    item_factors = np.load(io.BytesIO(load_blob_to_memory("als_item_factors.npy")))
    
    model_als = implicit.als.AlternatingLeastSquares(factors=50)
    model_als.user_factors = user_factors
    model_als.item_factors = item_factors
    
    user_array = pickle.loads(load_blob_to_memory("als_user_mapping.pkl"))
    item_array = pickle.loads(load_blob_to_memory("als_item_mapping.pkl"))
        
    real_to_internal_user = {real_id: idx for idx, real_id in enumerate(user_array)}
    real_to_internal_item = {real_id: idx for idx, real_id in enumerate(item_array)}
    internal_to_real_item = item_array
    
    # 3. Content-Based (PCA Embeddings)
    embeddings_pca = pickle.loads(load_blob_to_memory("articles_embeddings_pca.pickle"))
        
    # 4. Popularité
    popularity_df = pd.read_parquet(io.BytesIO(load_blob_to_memory("articles_popularity_time_decay.parquet")))
    dict_popularity = dict(zip(popularity_df['click_article_id'], popularity_df['time_decay_score']))
    
    # 5. Poids Hybrides (Optuna)
    try:
        weights_data = load_blob_to_memory("hybrid_weights.json")
        weights = json.loads(weights_data)
        WEIGHT_ALS = weights.get('weight_als', 0.7447)
        WEIGHT_CB = weights.get('weight_cb', 0.1946)
        WEIGHT_POP = weights.get('weight_pop', 0.1547)
    except Exception:
        WEIGHT_ALS = 0.7447
        WEIGHT_CB = 0.1946
        WEIGHT_POP = 0.1547

    logging.info("✅ Tous les modèles ont été téléchargés en RAM avec succès !")
except Exception as e:
    logging.error(f"❌ Erreur critique lors du téléchargement depuis le Blob Storage : {str(e)}")

# ==========================================
# 2. MOTEURS ISOLÉS
# ==========================================
def get_als_recommendations(user_id, user_history_list, top_n=50):
    if user_id not in real_to_internal_user:
        return {}
    internal_user_id = real_to_internal_user[user_id]
    internal_hist = [real_to_internal_item[art] for art in user_history_list if art in real_to_internal_item]
    
    num_items = len(item_array)
    if not internal_hist:
        user_sparse = sparse.csr_matrix((1, num_items))
    else:
        user_sparse = sparse.csr_matrix((np.ones(len(internal_hist)), (np.zeros(len(internal_hist)), internal_hist)), shape=(1, num_items))
        
    internal_item_ids, scores = model_als.recommend(internal_user_id, user_sparse, N=top_n, filter_already_liked_items=True)
    return {internal_to_real_item[int_id]: float(score) for int_id, score in zip(internal_item_ids, scores)}

def get_content_based_recommendations(user_history_list, top_n=50):
    if not user_history_list:
        return {} 
    last_article_id = user_history_list[-1]
    if last_article_id >= len(embeddings_pca):
        return {}
        
    target_vector = embeddings_pca[last_article_id].reshape(1, -1)
    similarities = cosine_similarity(target_vector, embeddings_pca)[0]
    top_indices = np.argsort(similarities)[::-1][1:top_n+1]
    return {idx: float(score) for idx, score in zip(top_indices, similarities[top_indices])}

def get_popularity_recommendations(top_n=50):
    sorted_pop = sorted(dict_popularity.items(), key=lambda item: item[1], reverse=True)
    return dict(sorted_pop[:top_n])

# ==========================================
# 3. ROUTE HTTP PRINCIPALE
# ==========================================
@app.route(route="recommend", auth_level=func.AuthLevel.ANONYMOUS)
def recommend(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Nouvelle requête de recommandation reçue.')

    user_id_param = req.params.get('user_id')
    if not user_id_param:
        return func.HttpResponse(json.dumps({"error": "Veuillez fournir un paramètre 'user_id'"}), status_code=400, mimetype="application/json")
        
    try:
        user_id = int(user_id_param)
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Le 'user_id' doit être un nombre entier"}), status_code=400, mimetype="application/json")
    
    top_n = int(req.params.get('top_n', 5))
    
    # Récupération de l'historique
    user_history_list = user_histories_dict.get(user_id, [])
    
    # Exécution des 3 moteurs
    als_recs = get_als_recommendations(user_id, user_history_list, top_n=50)
    cb_recs = get_content_based_recommendations(user_history_list, top_n=50)
    pop_recs = get_popularity_recommendations(top_n=50)
    
    if not als_recs and not cb_recs:
        top_pop = list(pop_recs.items())[:top_n]
        max_pop = float(top_pop[0][1]) if top_pop else 1.0
        final_recs = [{"article_id": int(k), "score": float(v) / max_pop} for k, v in top_pop]
        response_data = {
            "user_id": user_id,
            "status": "cold_start",
            "history_length": 0,
            "recommendations": final_recs
        }
        return func.HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    # Phase d'hybridation des scores
    all_articles = set(list(als_recs.keys()) + list(cb_recs.keys()) + list(pop_recs.keys()))
    df_recs = pd.DataFrame(index=list(all_articles))
    df_recs['score_als'] = pd.Series(als_recs)
    df_recs['score_cb'] = pd.Series(cb_recs)
    df_recs['score_pop'] = pd.Series(pop_recs)
    df_recs = df_recs.fillna(0)
    
    scaler = MinMaxScaler()
    if df_recs['score_als'].max() > 0: df_recs['score_als'] = scaler.fit_transform(df_recs[['score_als']])
    if df_recs['score_cb'].max() > 0: df_recs['score_cb'] = scaler.fit_transform(df_recs[['score_cb']])
    if df_recs['score_pop'].max() > 0: df_recs['score_pop'] = scaler.fit_transform(df_recs[['score_pop']])
        
    # Ajustement des poids si ALS est silencieux (Nouvel utilisateur)
    w_cb = WEIGHT_CB + WEIGHT_ALS if not als_recs else WEIGHT_CB
    w_als = 0.0 if not als_recs else WEIGHT_ALS
        
    df_recs['score_hybrid'] = (df_recs['score_als'] * w_als) + (df_recs['score_cb'] * w_cb) + (df_recs['score_pop'] * WEIGHT_POP)
    df_recs = df_recs.sort_values('score_hybrid', ascending=False)
    
    # Exclusion des articles déjà lus pour forcer la découverte
    df_recs = df_recs[~df_recs.index.isin(user_history_list)]
    
    top_df = df_recs.head(top_n)
    final_recs = [{"article_id": int(idx), "score": float(row['score_hybrid'])} for idx, row in top_df.iterrows()]
    
    # Construction de la réponse JSON Finale
    response_data = {
        "user_id": user_id,
        "status": "warm_user" if als_recs else "new_user",
        "history_length": len(user_history_list),
        "recommendations": final_recs
    }
    
    return func.HttpResponse(json.dumps(response_data), mimetype="application/json")
