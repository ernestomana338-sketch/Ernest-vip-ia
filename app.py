import numpy as np
from scipy.stats import poisson
import streamlit as st

st.set_page_config(page_title="QUANTUM FOOT", page_icon="🏆")
st.title("🏆 QUANTUM FOOT VIP PREMIUM")
st.markdown("---")

# ==========================================
# INPUTS : LES DONNÉES DU MATCH
# ==========================================
st.header("📊 Données Statistiques")

moy_generale = st.number_input("Moyenne Buts Championnat", value=2.6)

st.subheader("🏠 Équipe Domicile")
atq_dom = st.number_input("Attaque Domicile", value=1.5)
def_dom = st.number_input("Défense Domicile", value=0.8)
forme_dom = st.slider("Forme Domicile (%)", 50, 150, 110)

st.subheader("🚀 Équipe Extérieur")
atq_ext = st.number_input("Attaque Extérieur", value=1.1)
def_ext = st.number_input("Défense Extérieur", value=1.3)
forme_ext = st.slider("Forme Extérieur (%)", 50, 150, 90)

st.subheader("🎲 Cotes Bookmaker")
cote_1 = st.number_input("Cote Domicile (1)", value=1.85)
cote_N = st.number_input("Cote Nul (N)", value=3.60)
cote_2 = st.number_input("Cote Extérieur (2)", value=4.20)

# ==========================================
# CALCULS MATHÉMATIQUES VIP
# ==========================================
if st.button("⚡ LANCER L'ANALYSE VIP"):

    # Espérance de buts ajustée par la forme
    lambda_dom = atq_dom * def_ext * moy_generale * (forme_dom / 100)
    lambda_ext = atq_ext * def_dom * moy_generale * (forme_ext / 100)

    # Génération de la matrice des scores
    matrice = np.zeros((6, 6))
    for i in range(6):
        for j in range(6):
            prob = poisson.pmf(i, lambda_dom) * poisson.pmf(j, lambda_ext)
            if i == 0 and j == 0:
                prob *= (1.0 - lambda_dom * lambda_ext * -0.05)
            elif i == 0 and j == 1:
                prob *= (1.0 + lambda_dom * -0.05)
            elif i == 1 and j == 0:
                prob *= (1.0 + lambda_ext * -0.05)
            elif i == 1 and j == 1:
                prob *= (1.0 - -0.05)
            matrice[i, j] = prob

    matrice /= np.sum(matrice)

    # Calcul des issues principales
    p_1 = float(np.sum(np.tril(matrice, -1)))
    p_N = float(np.sum(np.diag(matrice)))
    p_2 = float(np.sum(np.triu(matrice, 1)))

    # Affichage des probabilités
    st.markdown("### 📈 PROBABILITÉS DES ISSUES")
    st.write(f"🏠 Victoire Domicile (1) : **{p_1:.1%}**")
    st.write(f"🤝 Match Nul (N) : **{p_N:.1%}**")
    st.write(f"🚀 Victoire Extérieur (2) : **{p_2:.1%}**")

    # Calcul des Multi-Scores
    st.markdown("---")
    st.markdown("### 🧬 MULTI-SCORES LOGIQUES")
    score_securise = matrice + matrice + matrice
    score_attaque = matrice + matrice + matrice
    score_nul = matrice + matrice
    
    st.write(f"⬜ **Multi-Score [1-0, 2-0, 2-1]** : **{score_securise:.1%}**")
    st.write(f"⬜ **Multi-Score [2-1, 3-1, 3-2]** : **{score_attaque:.1%}**")
    st.write(f"⬜ **Multi-Score Nul [1-1 ou 2-2]** : **{score_nul:.1%}**")

    # Top 5 des Scores Exacts
    st.markdown("---")
    st.markdown("### 🏆 TOP 5 SCORES EXACTS")
    
    scores_liste = []
    for i in range(6):
        for j in range(6):
            scores_liste.append((f"{i} - {j}", matrice[i, j]))
            
    scores_liste.sort(key=lambda x: x[1], reverse=True)

    for rang in range(5):
        nom_score, valeur_prob = scores_liste[rang]
        st.info(f"🏅 **Position {rang+1}** → Score Exact **[{nom_score}]** : **{valeur_prob:.1%}**")

    # Scanner de Value Bets Financier
    st.markdown("---")
    st.markdown("### 💎 SCANNER DE VALUE BETS")

    # Test Domicile
    if p_1 > (1 / cote_1):
        roi = (p_1 * cote_1) - 1
        st.success(f"🎯 **VALUE : Victoire Domicile** | ROI attendu : **+{roi:.1%}**")
    
    # Test Nul
    if p_N > (1 / cote_N):
        roi = (p_N * cote_N) - 1
        st.success(f"🎯 **VALUE : Match Nul** | ROI attendu : **+{roi:.1%}**")
        
    # Test Extérieur
    if p_2 > (1 / cote_2):
        roi = (p_2 * cote_2) - 1
        st.success(f"🎯 **VALUE : Victoire 
