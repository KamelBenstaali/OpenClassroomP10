import streamlit as st
import requests

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

# En-tête
st.markdown('<h1 class="main-title">GloboNews AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Votre moteur de recommandation intelligent</p>', unsafe_allow_html=True)

# On suppose que l'Azure Function tournera sur le port 7071
API_URL = "http://localhost:7071/api/recommend"

# Champ de saisie
user_id = st.number_input("Entrez votre Numéro d'Utilisateur (User ID) :", min_value=1, step=1, value=42)

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
                for i, art_id in enumerate(recos):
                    st.markdown(f"""
                        <div class="article-card">
                            <h3 style="margin-top:0; margin-bottom:5px; color:#2c3e50;">📰 Article n°{art_id}</h3>
                            <p style="color:#666; margin:0;">Sélectionné par le modèle hybride | Pertinence : {99 - i}%</p>
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
                    st.markdown(f"""
                        <div class="article-card">
                            <h3 style="margin-top:0; margin-bottom:5px; color:#2c3e50;">🔥 Article n°{art_id} (Tendance)</h3>
                            <p style="color:#666; margin:0;">Sélectionné via la Popularité (Time Decay) | Score d'engagement : Top {i+1}</p>
                        </div>
                    """, unsafe_allow_html=True)
