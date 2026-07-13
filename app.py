import streamlit as st
import numpy as np
import scipy.stats as stats
import requests

st.set_page_config(page_title="TITAN QUANTUM FOOT", page_icon="🌎", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #050b14; }
    .vip-title { text-align: center; color: #FFD700; font-family: 'Arial Black', sans-serif; font-size: 38px; }
    .card-vip { background-color: #0f172a; border: 1px solid #FFD700; border-radius: 8px; padding: 20px; margin-bottom: 15px; }
    </style>
""", unsafe_allowed_html=True)

st.markdown("<h1 class='vip-title'>👑 TITAN QUANTUM FOOT</h1>", unsafe_allowed_html=True)

# Remplacez par votre clé API obtenue sur API-Football
API_KEY = "VOTRE_CLE_API_ICI" 
API_URL = "https://api-sports.io"
headers = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

def chercher_match_mondial(nom_equipe):
    url = f"{API_URL}/fixtures"
    params = {"live": "all"} 
    try:
        response = requests.get(url, headers=headers, params=params).json()
        fixtures = response.get("response", [])
        for f in fixtures:
            eq_dom = f["teams"]["home"]["name"].lower()
            eq_ext = f["teams"]["away"]["name"].lower()
            if nom_equipe.lower() in eq_dom or nom_equipe.lower() in eq_ext:
                return f
    except:
        return None
    return None

def extraire_stats_historiques(team_id, league_id):
    return 1.5, 1.2

def Executer_Loi_Poisson_VIP(lambda_dom, lambda_ext):
    matrice = np.zeros((7, 7))
    for i in range(7):
        for j in range(7):
            matrice[i, j] = stats.poisson.pmf(i, lambda_dom) * stats.poisson.pmf(j, lambda_ext)
    p_1 = np.sum(np.tril(matrice, -1)) * 100
    p_X = np.sum(np.diag(matrice)) * 100
    p_2 = np.sum(np.triu(matrice, 1)) * 100
    return p_1, p_X, p_2, matrice

saisie_equipe = st.text_input("🔍 SCANNER DE COMPÉTITION MONDIALE", placeholder="Entrez le nom d'un club...")

if saisie_equipe:
    match_trouve = chercher_match_mondial(saisie_equipe)
    if match_trouve:
        league_name = match_trouve["league"]["name"]
        eq_dom_name = match_trouve["teams"]["home"]["name"]
        eq_ext_name = match_trouve["teams"]["away"]["name"]
        
        p_1, p_X, p_2, matrice_scores = Executer_Loi_Poisson_VIP(1.4, 1.1)
        max_idx = np.unravel_index(np.argmax(matrice_scores), matrice_scores.shape)
        
        st.markdown("<div class='card-vip'>", unsafe_allowed_html=True)
        st.subheader(f"🏟️ {league_name} : {eq_dom_name} vs {eq_ext_name}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Victoire Domicile", f"{p_1:.2f} %")
        c2.metric("Match Nul", f"{p_X:.2f} %")
        c3.metric("Victoire Extérieur", f"{p_2:.2f} %")
        st.markdown(f"📊 **Score Exact Optimal** : {max_idx} - {max_idx}", unsafe_allowed_html=True)
        st.markdown("</div>", unsafe_allowed_html=True)
    else:
        st.error("❌ Aucun match en cours trouvé.")
