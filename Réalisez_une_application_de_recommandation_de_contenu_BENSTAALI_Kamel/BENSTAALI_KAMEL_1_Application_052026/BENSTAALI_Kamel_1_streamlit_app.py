import streamlit as st
import requests
import pandas as pd
import os

# Configuration de la page
st.set_page_config(
    page_title="GloboNews AI",
    page_icon="🚀",
    layout="centered"
)

# Injection de CSS personnalisé pour un design "Premium" (Wow effect)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Titre avec gradient dynamique */
    .main-title {
        background: -webkit-linear-gradient(45deg, #FF416C, #FF4B2B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.2rem;
        padding-top: 2rem;
    }
    
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Design Premium des cartes d'articles */
    .article-card {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        color: #2c3e50;
        border-left: 5px solid #FF416C;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .article-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(255, 65, 108, 0.2);
        border-left: 5px solid #FF4B2B;
    }
    
    /* Style du bouton d'action */
    div.stButton > button {
        background: linear-gradient(45deg, #FF416C, #FF4B2B);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1.1rem;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(255, 65, 108, 0.4);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Chargement des métadonnées des articles en cache pour être rapide
@st.cache_data
def load_metadata():
    metadata_path = "../Data/news-portal-user-interactions-by-globocom/articles_metadata.csv"
    if os.path.exists(metadata_path):
        return pd.read_csv(metadata_path, usecols=['article_id', 'category_id'])
    return pd.DataFrame(columns=['article_id', 'category_id'])

metadata_df = load_metadata()

# En-tête
st.markdown('<h1 class="main-title">GloboNews AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Votre moteur de recommandation intelligent</p>', unsafe_allow_html=True)

# L'URL de production publique sur Azure Functions
API_URL = "https://globonews-api-p10-evg7eza5gqfnendh.francecentral-01.azurewebsites.net/api/recommend"

# --- NOUVEAU : Input libre pour le User ID ---
st.markdown("### 👤 Qui êtes-vous ?")
user_id = st.number_input(
    "Saisissez votre ID Utilisateur (ex: 0, 42, 25, ou 999999 pour un nouvel utilisateur) :",
    min_value=0,
    value=0,
    step=1
)

# Bouton déclencheur
if st.button("🚀 Découvrir mes recommandations"):
    with st.spinner("Analyse de votre profil par l'Intelligence Artificielle..."):
        
        try:
            # Appel à l'API Azure Function
            response = requests.get(f"{API_URL}?user_id={user_id}")
            
            if response.status_code == 200:
                data = response.json()
                recos = data.get("recommendations", [])
                
                st.success("✨ Voici vos recommandations sur mesure !")
                
                # Affichage des cartes avec le design CSS
                for item in recos:
                    art_id = item.get("article_id")
                    score = item.get("score")
                    percent = round(score * 100, 1)
                    
                    # Recherche de la catégorie dans les métadonnées
                    cat_match = metadata_df[metadata_df['article_id'] == art_id]
                    cat_id = cat_match['category_id'].values[0] if not cat_match.empty else "Inconnue"
                    
                    st.markdown(f"""
                        <div class="article-card">
                            <h3 style="margin-top:0; margin-bottom:5px; color:#2c3e50;">📰 Article n°{art_id}</h3>
                            <p style="color:#FF416C; font-weight:500; margin-bottom:5px;">🏷️ Catégorie : {cat_id}</p>
                            <p style="color:#666; margin:0;">Pertinence : {percent}%</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(f"Erreur de l'API (Code {response.status_code}). Vérifiez que l'Azure Function tourne en local !")
                
        except requests.exceptions.ConnectionError:
            st.warning("⚠️ Impossible de joindre l'API de Recommandation Hybride.")
            st.info("💡 L'API est hors-ligne. Affichage des articles les plus populaires en guise de secours (Fallback) :")
            
            # --- FALLBACK : ARTICLES LES PLUS POPULAIRES (Time Decay) ---
            popular_fallback = [160974, 336221, 272143, 234698, 96210]
            
            for i, art_id in enumerate(popular_fallback):
                    # Recherche de la catégorie pour le fallback aussi
                    cat_match = metadata_df[metadata_df['article_id'] == art_id]
                    cat_id = cat_match['category_id'].values[0] if not cat_match.empty else "Inconnue"
                    
                    st.markdown(f"""
                        <div class="article-card">
                            <h3 style="margin-top:0; margin-bottom:5px; color:#2c3e50;">🔥 Article n°{art_id} (Tendance)</h3>
                            <p style="color:#FF416C; font-weight:500; margin-bottom:5px;">🏷️ Catégorie : {cat_id}</p>
                            <p style="color:#666; margin:0;">Sélectionné via la Popularité (Time Decay) | Score d'engagement : Top {i+1}</p>
                        </div>
                    """, unsafe_allow_html=True)
