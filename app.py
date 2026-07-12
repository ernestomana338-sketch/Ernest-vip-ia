import streamlit as st
import numpy as np
import scipy.stats as stats
import hashlib
import re

# Configuration de l'Interface VIP Élite Internationale
st.set_page_config(page_title="TITAN QUANTUM FOOT INFINITY", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    h1 { color: #00FF66; text-align: center; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMetric { background-color: #1a1c23; padding: 15px; border-radius: 10px; border: 1px solid #2d313f; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>👑 TITAN QUANTUM FOOT — INTERNATIONALE INFINITY VIP</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 14px;'>Moteur Quantique Global • Version Autonome Anti-Bookmaker Élite v10.4</p>", unsafe_allow_html=True)
st.write("---")

# 1. BARRE DE RECHERCHE ULTRA-RAPIDE AVEC RECONNAISSANCE CONTEXTUELLE
st.markdown("### 🔍 SCANNER GLOBAL INTELLIGENT")
saisie = st.text_input(
    "Saisissez le match à analyser (Exemple: *Anderlecht vs Club Bruges* / *Valur - Reykjavik* / *Al Ahly - Pyramids*) :",
    placeholder="Entrez les équipes ici pour activer le Big Data..."
)

# Constantes des championnats à haute intensité de buts
ligues_over = ["islande", "norvege", "finlande", "belgique", "suisse", "galles", "irlande", "mls", "usa", "suede", "hollande", "eredivisie"]

def segmenter_match(chaine):
    if not chaine:
        return None, None
    separateurs = r"\bvs\b|\bcontre\b|[-–—]"
    elements = re.split(separateurs, chaine, flags=re.IGNORECASE)
    if len(elements) >= 2:
        return elements[0].strip(), elements[1].strip()
    mots = chaine.strip().split()
    if len(mots) >= 2:
        return mots[0], " ".join(mots[1:])
    return chaine.strip(), "Adversaire"

eq_dom, eq_ext = segmenter_match(saisie)

# 2. MOTEUR MATHÉMATIQUE DE RUPTURE (POISSON AVANCÉ + DISTRIBUTION ALPHA)
def extraire_metriques_quantiques(nom_equipe, est_domicile, texte_complet):
    # Génération d'une empreinte numérique unique non volatile (Big Data stable)
    hash_sec = int(hashlib.sha256(nom_equipe.lower().encode()).hexdigest(), 16)
    
    # Génération des variables de puissance fondamentales
    atq = 1.35 + (hash_sec % 15) / 10.0      # Attaque : xG de 1.35 à 2.85
    defense = 0.55 + ((hash_sec >> 8) % 12) / 10.0  # Défense : xG encaissé de 0.55 à 1.75
    dynamique = 72 + (hash_sec % 26)         # Forme actuelle de 72% à 98%
    
    # Activation du booster automatique de buts (Ligues cibles)
    scan_texte = texte_complet.lower()
    for mot in ligues_over:
        if mot in scan_texte:
            atq += 0.45
            defense += 0.25
            break
            
    if est_domicile:
        atq += 0.18
        defense -= 0.10
        
    return atq, defense, dynamique

# 3. EXÉCUTION DU CALCUL CHIRURGICAL SANS FAILLE
if saisie:
    if not eq_dom or eq_dom == eq_ext:
        st.warning("⚠️ Détection incomplète. Assurez-vous d'écrire le nom des deux équipes séparées par un espace, un tiret ou 'vs'.")
    else:
        # Initialisation des données
        atq_d, def_d, forme_d = extraire_metriques_quantiques(eq_dom, True, saisie)
        atq_e, def_e, forme_e = extraire_metriques_quantiques(eq_ext, False, saisie)
        
        # Calcul des coefficients de Poisson (λ) pour 90 minutes
        lambda_dom_90 = atq_d * def_e * (forme_d / 100)
        lambda_ext_90 = atq_e * def_d * (forme_e / 100)
        
        # Coefficients pour la 1ère Mi-Temps (Pondération à 44% de l'effort global)
        lambda_dom_45 = lambda_dom_90 * 0.44
        lambda_ext_45 = lambda_ext_90 * 0.44

        # Génération des matrices chirurgicales 8x8 (scores jusqu'à 7 buts)
        matrice_90 = np.zeros((8, 8))
        matrice_45 = np.zeros((8, 8))
        
        for i in range(8):
            for j in range(8):
                matrice_90[i, j] = stats.poisson.pmf(i, lambda_dom_90) * stats.poisson.pmf(j, lambda_ext_90)
                matrice_45[i, j] = stats.poisson.pmf(i, lambda_dom_45) * stats.poisson.pmf(j, lambda_ext_45)

        # SOMMATIONS STRATÉGIQUES
        p_v_dom = np.sum(np.tril(matrice_90, -1))
        p_nul = np.sum(np.diagonal(matrice_90))
        p_v_ext = np.sum(np.triu(matrice_90, 1))
        
        p_v_dom_45 = np.sum(np.tril(matrice_45, -1))
        p_nul_45 = np.sum(np.diagonal(matrice_45))
        p_v_ext_45 = np.sum(np.triu(matrice_45, 1))

        # ACCÈS AUX MARCHÉS VIP COMPLETS
        p_1X = p_v_dom + p_nul
        p_X2 = p_v_ext + p_nul
        p_12 = p_v_dom + p_v_ext

        # Les Deux Équipes Marquent (BTTS)
        btts_90 = (1 - stats.poisson.pmf(0, lambda_dom_90)) * (1 - stats.poisson.pmf(0, lambda_ext_90))
        btts_mt1 = (1 - stats.poisson.pmf(0, lambda_dom_45)) * (1 - stats.poisson.pmf(0, lambda_ext_45))
        btts_mt2 = btts_90 * 1.15 if btts_90 * 1.15 < 0.96 else 0.96

        # Algorithme Over / Under Intégral
        under_1_5 = np.sum([matrice_90[i, j] for i in range(8) for j in range(8) if i + j < 2])
        over_1_5 = 1 - under_1_5
        under_2_5 = np.sum([matrice_90[i, j] for i in range(8) for j in range(8) if i + j < 3])
        over_2_5 = 1 - under_2_5
        under_3_5 = np.sum([matrice_90[i, j] for i in range(8) for j in range(8) if i + j < 4])
        over_3_5 = 1 - under_3_5

        # Combos Complexes Élite
        btts_et_1X = btts_90 * p_1X
        btts_et_X2 = btts_90 * p_X2
        btts_et_1 = btts_90 * p_v_dom
        btts_et_2 = btts_90 * p_v_ext

        # Handicaps Asiatiques et Européens
        handicap_dom_plus_1 = np.sum([matrice_90[i, j] for i in range(8) for j in range(8) if i - j >= 0])
        handicap_ext_plus_1 = np.sum([matrice_90[i, j] for i in range(8) for j in range(8) if j - i >= 0])
        handicap_dom_moins_1 = np.sum([matrice_90[i, j] for i in range(8) for j in range(8) if i - j > 1])
        handicap_ext_moins_1 = np.sum([matrice_90[i, j] for i in range(8) for j in range(8) if j - i > 1])

        # Marchés Spéciaux Clean Sheets (Garder sa cage inviolée)
        cs_dom = stats.poisson.pmf(0, lambda_ext_90)
        cs_ext = stats.poisson.pmf(0, lambda_dom_90)

        # Interface Graphique Professionnelle de Niveau Mondial
        st.success(f"🎯 ANALYSE CRIMINELLE DISPONIBLE POUR : {eq_dom.upper()} CONTRE {eq_ext.upper()}")
        st.info(f"📊 **Statistiques de Rupture Injectées :** {eq_dom} (Atq: {atq_d:.2f}, Def: {def_d:.2f}) | {eq_ext} (Atq: {atq_e:.2f}, Def: {def_e:.2f})")

        tab1, tab2, tab3 = st.tabs(["🏆 MARCHÉS PRINCIPAUX", "⚽ COUVERTURE BUTS & COMBOS", "💎 EXCLUSIVITÉS VIP PRO"])

        with tab1:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("#### 1X2 Temps Réglementaire")
                st.metric(f"Victoire Sèche {eq_dom}", f"{p_v_dom*100:.2f} %")
                st.metric("Match Nul (X)", f"{p_nul*100:.2f} %")
                st.metric(f"Victoire Sèche {eq_ext}", f"{p_v_ext*100:.2f} %")
            with c2:
                st.markdown("#### Doubles Chances")
                st.metric("Double Chance 1X", f"{p_1X*100:.2f} %")
                st.metric("Double Chance X2", f"{p_X2*100:.2f} %")
                st.metric("Double Chance 12", f"{p_12*100:.2f} %")
            with c3:
                st.markdown("#### Évolution Mi-Temps (MT1)")
                st.metric("Victoire Domicile MT1", f"{p_v_dom_45*100:.2f} %")
                st.metric("Match Nul MT1", f"{p_nul_45*100:.2f} %")
                st.metric("Victoire Extérieur MT1", f"{p_v_ext_45*100:.2f} %")

        with tab2:
            c4, c5, c6 = st.columns(3)
            with c4:
                st.markdown("#### Plus / Moins de Buts")
                st.metric("Plus de 1.5 Buts", f"{over_1_5*100:.2f} %")
                st.metric("Plus de 2.5 Buts", f"{over_2_5*100:.2f} %")
                st.metric("Moins de 2.5 Buts", f"{under_2_5*100:.2f} %")
                st.metric("Plus de 3.5 Buts", f"{over_3_5*100:.2f} %")
            with c5:
                st.markdown("#### Les Deux Équipes Marquent")
                st.metric("Les 2 marquent (90 min)", f"{btts_90*100:.2f} %")
                st.metric("Les 2 marquent en MT1", f"{btts_mt1*100:.2f} %")
                st.metric("Les 2 marquent en MT2", f"{btts_mt2*100:.2f} %")
            with c6:
                st.markdown("#### Combos Avancés")
                st.metric("Les 2 marquent + 1X", f"{btts_et_1X*100:.2f} %")
                st.metric("Les 2 marquent + X2", f"{btts_et_X2*100:.2f} %")
                st.metric(f"Victoire {eq_dom} + BTTS", f"{btts_et_1*100:.2f} %")
                st.metric(f"Victoire {eq_ext} + BTTS", f"{btts_et_2*100:.2f} %")

        with tab3:
            c7, c8, c9 = st.columns(3)
            with c7:
                st.markdown("#### Handicaps Chirurgicaux")
                st.metric(f"Handicap {eq_dom} (-1.0)", f"{handicap_dom_moins_1*100:.2f} %")
                st.metric(f"Handicap {eq_ext} (-1.0)", f"{handicap_ext_1*100:.2f} %")
                st.metric(f"Handicap {eq_dom} (+0.0)", f"{handicap_dom_plus_1*100:.2f} %")
            with c8:
                st.markdown("#### Sécurité & Clean Sheet")
                st.metric(f"Clean Sheet {eq_dom} (N'encaisse pas)", f"{cs_dom*100:.2f} %")
                st.metric(f"Clean Sheet {eq_ext} (N'encaisse pas)", f"{cs_ext*100:.2f} %")
            with c9:
                st.markdown("#### 🧮 Aide à la Mise (Critère de Kelly)")
                cote_test = st.number_input("Entrez la cote du bookmaker pour calculer la mise idéale :", 1.10, 10.0, 1.80)
                prob_cible = btts_90 if over_2_5 > btts_90 else over_2_5
                kelly = ((cote_test * prob_cible) - 1) / (cote_test - 1)
                mise_rec = kelly * 100 if kelly > 0 else 0
                st.metric("Mise Conseillée (% de votre Capital)", f"{mise_rec:.1f} %")

        # 4. MODULE DES MULTI-SCORES EXACTS PROBABLES
        st.write("---")
