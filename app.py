import streamlit as st
import numpy as np
import scipy.stats as stats
import requests

# --- CONFIGURATION INTERFACE ÉLITE MONDIALE ---
st.set_page_config(page_title="TITAN QUANTUM FOOT - GLOBAL COVERAGE", page_icon="🌎", layout="wide")

# CSS Premium Style Dark VIP
st.markdown("""
    <style>
    .reportview-container { background: #050b14; }
    .vip-title { text-align: center; color: #FFD700; font-family: 'Arial Black', sans-serif; font-size: 38px; }
    .card-vip { background-color: #0f172a; border: 1px solid #FFD700; border-radius: 8px; padding: 20px; margin-bottom: 15px; }
    </style>
""", unsafe_allowed_html=True)

st.markdown("<h1 class='vip-title'>👑 TITAN QUANTUM FOOT - BASE MONDIALE INTÉGRALE</h1>", unsafe_allowed_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Zéro restriction : Accès direct aux 950+ championnats du monde en temps réel</p>", unsafe_allowed_html=True)

# --- 1. CONFIGURATION DU FLUX DE DONNÉES PROFESSIONNEL ---
# Remplacer par votre clé obtenue sur API-Football
API_KEY = "VOTRE_CLE_API_ICI" 
API_URL = "https://v3.football.api-sports.io"

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}

# --- 2. FONCTIONS CHIRURGICALES DE RECHERCHE ET DATA EXTRES ---
def chercher_match_mondial(nom_equipe):
    """ Recherche le match en direct sur les serveurs mondiaux de l'API """
    url = f"{API_URL}/fixtures"
    # Recherche les matchs du jour (Live et à venir)
    params = {"live": "all"} 
    try:
        response = requests.get(url, headers=headers, params=params).json()
        fixtures = response.get("response", [])
        
        # Filtrage chirurgical par mot-clé saisi par l'utilisateur
        for f in fixtures:
            eq_dom = f["teams"]["home"]["name"].lower()
            eq_ext = f["teams"]["away"]["name"].lower()
            if nom_equipe.lower() in eq_dom or nom_equipe.lower() in eq_ext:
                return f
        
        # Si aucun live trouvé, recherche dans les prochains matchs planifiés
        from datetime import datetime
        aujourdhui = datetime.today().strftime('%Y-%m-%d')
        params_futur = {"date": aujourdhui}
        response_futur = requests.get(url, headers=headers, params=params_futur).json()
        for f in response_futur.get("response", []):
            eq_dom = f["teams"]["home"]["name"].lower()
            eq_ext = f["teams"]["away"]["name"].lower()
            if nom_equipe.lower() in eq_dom or nom_equipe.lower() in eq_ext:
                return f
    except Exception as e:
        st.error(f"Erreur de connexion API : {e}")
    return None

def extraire_stats_historiques(team_id, league_id, season=2026):
    """ Récupère les vrais buts marqués/encaissés de n'importe quelle équipe du globe """
    url = f"{API_URL}/teams/statistics"
    params = {"team": team_id, "league": league_id, "season": season}
    try:
        res = requests.get(url, headers=headers, params=params).json()
        data = res.get("response", {})
        goals = data.get("goals", {})
        
        # Extraction des moyennes de buts
        buts_marques = float(goals.get("for", {}).get("average", {}).get("home", 1.5))
        buts_encaisses = float(goals.get("against", {}).get("average", {}).get("away", 1.2))
        return buts_marques, buts_encaisses
    except:
        return 1.5, 1.2

# --- 3. MOTEUR MATHÉMATIQUE DE POISSON PUR ---
def Executer_Loi_Poisson_VIP(lambda_dom, lambda_ext):
    matrice = np.zeros((7, 7))
    for i in range(7):
        for j in range(7):
            matrice[i, j] = stats.poisson.pmf(i, lambda_dom) * stats.poisson.pmf(j, lambda_ext)
    
    p_1 = np.sum(np.tril(matrice, -1)) * 100
    p_X = np.sum(np.diag(matrice)) * 100
    p_2 = np.sum(np.triu(matrice, 1)) * 100
    return p_1, p_X, p_2, matrice

# --- INTERFACE STREAMLIT ULTRA DYNAMIQUE ---
saisie_equipe = st.text_input("🔍 SCANNER DE COMPÉTITION MONDIALE", placeholder="Entrez le nom d'un club (Ex: Chelsea, Zamalek, Boca Juniors, Al Nassr...)")

if saisie_equipe:
    with st.spinner("⚡ Interrogation instantanée de la base de données globale..."):
        match_trouve = chercher_match_mondial(saisie_equipe)
        
    if match_trouve:
        # Extraction des identifiants uniques de l'infrastructure FIFA/UEFA
        league_name = match_trouve["league"]["name"]
        pays = match_trouve["league"]["country"]
        id_league = match_trouve["league"]["id"]
        
        eq_dom_name = match_trouve["teams"]["home"]["name"]
        eq_ext_name = match_trouve["teams"]["away"]["name"]
        id_dom = match_trouve["teams"]["home"]["id"]
        id_ext = match_trouve["teams"]["away"]["id"]
        
        with st.spinner("📊 Analyse statistique de l'historique de la ligue..."):
            # Requête chirurgicale des statistiques réelles des deux clubs
            buts_m_dom, buts_e_dom = extraire_stats_historiques(id_dom, id_league)
            buts_m_ext, buts_e_ext = extraire_stats_historiques(id_ext, id_league)
            
            # Calcul de l'espérance mathématique (Lambda)
            lambda_dom = (buts_m_dom + buts_e_ext) / 2
            lambda_ext = (buts_m_ext + buts_e_dom) / 2
            
            # Déclenchement de la loi de Poisson pure
            p_1, p_X, p_2, matrice_scores = Executer_Loi_Poisson_VIP(lambda_dom, lambda_ext)
            
            # Extraction du Score Exact Optimal
            max_idx = np.unravel_index(np.argmax(matrice_scores), matrice_scores.shape)
            
        # Affichage du Rapport Premium
        st.markdown(f"<div class='card-vip'>", unsafe_allowed_html=True)
        st.subheader(f"🏟️ Championnat : {league_name} ({pays})")
        st.markdown(f"### {eq_dom_name} vs {eq_ext_name}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric(f"Victoire {eq_dom_name}", f"{p_1:.2f} %")
        c2.metric("Match Nul", f"{p_X:.2f} %")
        c3.metric(f"Victoire {eq_ext_name}", f"{p_2:.2f} %")
        st.markdown("</div>", unsafe_allowed_html=True)
        
        st.markdown("<div class='card-vip'>", unsafe_allowed_html=True)
        st.markdown(f"### 🎯 PREDICTION CHIRURGICALE SCORE EXACT : <span style='color:#FFD700;'>{max_idx[0]} - {max_idx[1]}</span>", unsafe_allowed_html=True)
        st.write(f"Probabilité pure d'occurrence du score : {matrice_scores[max_idx]*100:.2f}%")
        st.markdown("</div>", unsafe_allowed_html=True)
        
    else:
    st.error("❌ Aucun match trouvé
