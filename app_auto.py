import streamlit as st
import numpy as np
import scipy.stats as stats
import requests
from datetime import datetime

# 1. CONFIGURATION DE L'APPLICATION
st.set_page_config(page_title="TITAN QUANTUM FOOT VIP", page_icon="⚡", layout="wide")

# Interface UI Premium (Style Sombre et Or)
st.markdown("""
    <style>
    .reportview-container { background: #0b0f19; }
    .vip-title { text-align: center; color: #FFD700; font-family: 'Arial Black', sans-serif; font-size: 40px; margin-bottom: 20px; text-shadow: 0px 0px 10px rgba(255,215,0,0.5); }
    .card-vip { background-color: #121826; border: 1px solid #FFD700; border-radius: 12px; padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .metric-val { color: #00FFCC; font-size: 24px; font-weight: bold; }
    .value-bet { background-color: #1b2e24; border: 1px solid #00FF88; color: #00FF88; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='vip-title'>👑 TITAN QUANTUM FOOT - VERSION VIP PREMIUM</h1>", unsafe_allow_html=True)

# CONFIGURATION API (Remplacez par votre clé)
API_KEY = "94fa330885215e500b135dd2e77486a8
BASE_URL = "https://api-sports.io"
HEADERS = {
    'x-rapidapi-host': 'v3.football.api-sports.io',
    'x-rapidapi-key': API_KEY
}

# 2. COLLECTE DU BIG DATA EN TEMPS RÉEL
def extraire_donnees_api(endpoint, params=None):
    try:
        url = f"{BASE_URL}/{endpoint}"
        response = requests.get(url, headers=HEADERS, params=params, timeout=12)
        if response.status_code == 200:
            return response.json().get("response", [])
        return []
    except Exception:
        return []

def chercher_match_mondial(nom_equipe):
    """Cherche un match aujourd'hui dans n'importe quelle compétition mondiale (Live ou À venir)"""
    if not nom_equipe:
        return None
    aujourdhui = datetime.today().strftime('%Y-%m-%d')
    
    matchs = extraire_donnees_api("fixtures", params={"date": aujourdhui})
    
    recherche = nom_equipe.strip().lower()
    for m in matchs:
        eq_dom = m["teams"]["home"]["name"].lower()
        eq_ext = m["teams"]["away"]["name"].lower()
        if recherche in eq_dom or recherche in eq_ext:
            return m
    return None

# 3. CALCUL CHIRURGICAL DES MOYENNES (FORCE ATTAQUE / DÉFENSE)
def calculer_lambdas_chirurgicaux(league_id, team_home_id, team_away_id):
    saison_actuelle = datetime.today().year
    
    stats_home = extraire_donnees_api("teams/statistics", params={"league": league_id, "season": saison_actuelle, "team": team_home_id})
    stats_away = extraire_donnees_api("teams/statistics", params={"league": league_id, "season": saison_actuelle, "team": team_away_id})
    
    lambda_home = 1.45
    lambda_away = 1.15
    
    if stats_home and stats_away:
        try:
            home_goals_for = stats_home.get("goals", {}).get("for", {}).get("average", {}).get("home", 1.5)
            away_goals_against = stats_away.get("goals", {}).get("against", {}).get("average", {}).get("away", 1.2)
            away_goals_for = stats_away.get("goals", {}).get("for", {}).get("average", {}).get("away", 1.1)
            home_goals_against = stats_home.get("goals", {}).get("against", {}).get("average", {}).get("home", 1.3)
            
            lambda_home = (float(home_goals_for) + float(away_goals_against)) / 2
            lambda_away = (float(away_goals_for) + float(home_goals_against)) / 2
        except (ValueError, TypeError):
            pass
            
    return max(lambda_home, 0.1), max(lambda_away, 0.1)

# 4. RÉCUPÉRATION DES COTES EN TEMPS RÉEL (ODDS)
def obtenir_cotes_temps_reel(fixture_id):
    cotes_data = extraire_donnees_api("odds", params={"fixture": fixture_id})
    if cotes_data:
        bookmakers = cotes_data.get("bookmakers", [])
        if bookmakers:
            bets = bookmakers[0].get("bets", [])
            for b in bets:
                if b.get("name") == "Match Winner" or b.get("id") == 1:
                    odds_list = b.get("values", [])
                    cote_1, cote_X, cote_2 = None, None, None
                    for o in odds_list:
                        if o["value"] == "Home": cote_1 = float(o["odd"])
                        elif o["value"] == "Draw": cote_X = float(o["odd"])
                        elif o["value"] == "Away": cote_2 = float(o["odd"])
                    return cote_1, cote_X, cote_2
    return None, None, None

# 5. ALGORITHME MATHÉMATIQUE DE POISSON & ANALYSE MATRICIELLE
def executer_loi_poisson_vip(lambda_dom, lambda_ext):
    matrice = np.zeros((7, 7))
    for i in range(7):
        for j in range(7):
            matrice[i, j] = stats.poisson.pmf(i, lambda_dom) * stats.poisson.pmf(j, lambda_ext)
            
    p_1 = np.sum(np.tril(matrice, -1)) * 100
    p_X = np.sum(np.diag(matrice)) * 100
    p_2 = np.sum(np.triu(matrice, 1)) * 100
    return p_1, p_X, p_2, matrice

# 6. INTERFACE DE RECHERCHE STREAMLIT
saisie_equipe = st.text_input("📊 SCANNER DE COMPÉTITION MONDIALE (Entrez le nom d'un club ou pays)", placeholder="Ex: Real Madrid, PSG, Arsenal, Brésil...")

if saisie_equipe:
    with st.spinner("Analyse des bases de données mondiales en cours..."):
        match_trouve = chercher_match_mondial(saisie_equipe)
        
        if match_trouve:
            fixture_id = match_trouve["fixture"]["id"]
            league_name = match_trouve["league"]["name"]
            league_country = match_trouve["league"]["country"]
            eq_dom_name = match_trouve["teams"]["home"]["name"]
            eq_ext_name = match_trouve["teams"]["away"]["name"]
            
            id_dom = match_match_trouve = match_trouve["teams"]["home"]["id"]
            id_ext = match_trouve["teams"]["away"]["id"]
            id_ligue = match_trouve["league"]["id"]
            
            lambda_dom, lambda_ext = calculer_lambdas_chirurgicaux(id_ligue, id_dom, id_ext)
            p_1, p_X, p_2, matrice_scores = executer_loi_poisson_vip(lambda_dom, lambda_ext)
            cote_1, cote_X, cote_2 = obtenir_cotes_temps_reel(fixture_id)
            
            max_idx = np.unravel_index(np.argmax(matrice_scores), matrice_scores.shape)
            
            st.markdown(f"""
                <div class='card-vip'>
                    <h3 style='color:#FFD700; margin-top:0;'>🏆 {league_name.upper()} ({league_country})</h3>
                    <h2 style='color:#ffffff; margin-bottom:20px;'>{eq_dom_name} 🆚 {eq_ext_name}</h2>
                    <p style='color:#a0aec0;'>Données algorithmiques injectées : λ Dom: <b>{lambda_dom:.2f}</b> | λ Ext: <b>{lambda_ext:.2f}</b></p>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<div class='card-vip'>🏠 Victoire Domicile<br><span class='metric-val'>{p_1:.2f} %</span></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='card-vip'>🤝 Match Nul<br><span class='metric-val'>{p_X:.2f} %</span></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='card-vip'>🚀 Victoire Extérieur<br><span class='metric-val'>{p_2:.2f} %</span></div>", unsafe_allow_html=True)
                
            st.markdown(f"""
                <div class='card-vip' style='text-align:center;'>
                    <span style='color:#a0aec0; font-size:14px;'>🎯 PRÉDICTION DU SCORE EXACT OPTIMAL</span><br>
                    <span style='font-size:32px; color:#FFD700; font-weight:bold;'>{max_idx[0]} - {max_idx[1]}</span><br>
                    <span style='color:#00FFCC; font-size:14px;'>Confiance statistique : {(matrice_scores[max_idx]*100):.2f}%</span>
                </div>
            """, unsafe_allow_html=True)
            
            if cote_1 and cote_X and cote_2:
                st.markdown("<h3 style='color:#ffffff; margin-top:30px;'>📈 Analyse des Écarts du Marché (Value Bets)</h3>", unsafe_allow_html=True)
                col_o1, col_oX, col_o2 = st.columns(3)
                
                with col_o1:
                    st.metric(label=f"Cote {eq_dom_name}", value=f"{cote_1:.2f}")
                    if p_1 > (100 / cote_1):
                        st.markdown("<div class='value-bet'>🔥 VALUE BET DETECTÉ (1)</div>", unsafe_allow_html=True)
                        
                with col_oX:
                    st.metric(label="Cote Match Nul", value=f"{cote_X:.2f}")
                    if p_X > (100 / cote_X):
                        st.markdown("<div class='value-bet'>🔥 VALUE BET DETECTÉ (X)</div>", unsafe_allow_html=True)
                        
                with col_o2:
                    st.metric(label=f"Cote {eq_ext_name}", value=f"{cote_2:.2f}")
                    if p_2 > (100 / cote_2):
                        st.markdown("<div class='value-bet'>🔥 VALUE BET DETECTÉ (2)</div>", unsafe_allow_html=True)
            else:
                st.info("💡 Les cotes en direct ne sont pas encore ouvertes pour ce match.")
        else:
            st.error("❌ Aucun match trouvé aujourd'hui pour cette équipe.")
