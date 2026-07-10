import streamlit as st
import requests
import scipy.stats as stats
import numpy as np

# --- CONFIGURATION AUTOMATIQUE VIP ---
# Votre clé reçue par email (si vous la retrouvez, remplacez la ligne en dessous)
API_TOKEN = "80f1e0cf47e84ba2b06067b84ba68ea8" 
HEADERS = {"X-Auth-Token": API_TOKEN}

def extraire_donnees_championnat(competition_code="FL1"):
    url = f"https://football-data.org{competition_code}/standings"
    try:
        reponse = requests.get(url, headers=HEADERS).json()
        equipes = {}
        total_buts, total_matchs = 0, 0
        for table in reponse["standings"][0]["table"]:
            nom = table["team"]["name"]
            mj = table["playedGames"]
            bp = table["goalsFor"]
            bc = table["goalsAgainst"]
            if mj > 0:
                equipes[nom] = {"attaque": bp / mj, "defense": bc / mj}
                total_buts += bp
                total_matchs += mj
        moy = (total_buts / total_matchs) if total_matchs > 0 else 2.5
        return equipes, moy
    except:
        return {}, 2.5

# --- INTERFACE VIP QUANTUM ---
st.title("🏆 QUANTUM FOOT VIP AUTOMATIQUE")
st.markdown("---")

championnat = st.selectbox("🌍 Championnat", ["Ligue 1 (France)", "Premier League (Angleterre)", "La Liga (Espagne)"])
codes = {"Ligue 1 (France)": "FL1", "Premier League (Angleterre)": "PL", "La Liga (Espagne)": "PD"}

stats_equipes, moy_buts = extraire_donnees_championnat(codes[championnat])

if stats_equipes:
    liste = sorted(list(stats_equipes.keys()))
    col1, col2 = st.columns(2)
    eq_dom = col1.selectbox("🏠 Équipe Domicile", options=liste, index=0)
    eq_ext = col2.selectbox("🚀 Équipe Extérieur", options=liste, index=1)
    
    if st.button("⚡ LANCER L'ANALYSE VIP AUTOMATIQUE"):
        lambda_dom = (stats_equipes[eq_dom]["attaque"] / moy_buts) * (stats_equipes[eq_ext]["defense"] / moy_buts) * moy_buts
        lambda_ext = (stats_equipes[eq_ext]["attaque"] / moy_buts) * (stats_equipes[eq_dom]["defense"] / moy_buts) * moy_buts
        
        prob_dom = [stats.poisson.pmf(i, lambda_dom) for i in range(6)]
        prob_ext = [stats.poisson.pmf(j, lambda_ext) for j in range(6)]
        matrice = np.outer(prob_dom, prob_ext)
        
        p_1 = float(np.sum(np.tril(matrice, -1))) * 100
        p_N = float(np.sum(np.diag(matrice))) * 100
        p_2 = float(np.sum(np.triu(matrice, 1))) * 100
        
        st.markdown("### 📊 PROBABILITÉS AUTOMATIQUES")
        st.write(f"🏠 Victoire {eq_dom} : **{p_1:.1f}%**")
        st.write(f"🤝 Match Nul : **{p_N:.1f}%**")
        st.write(f"🚀 Victoire {eq_ext} : **{p_2:.1f}%**")
else:
    st.warning("⚠️ Connexion Big Data en cours... Actualisez si besoin.")
  
