import streamlit as st
from utils11 import commencer, afficher_questions, suivant, precedent, afficher_synthese

import os

def injecter_css():
    chemin_css = os.path.join(os.path.dirname(__file__), "styles.css")
    with open(chemin_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Quiz sur les équations différentielles", page_icon="🧠", layout="centered")
injecter_css()

# --------- Page d'accueil si le quiz n’a pas encore commencé ---------
if "questions_melangees" not in st.session_state:

    # --- CSS pour centrer le bouton ---
    st.markdown("""
    <style>
    .home-box {
        background: linear-gradient(to right, #f8fbff, #fff);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        margin-top: 4rem;
        color: #222 !important;
    }
    .home-box h1 {
        font-size: 2.8rem;
        color: #1f77b4;
    }
    .home-box p {
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .start-button {
        display: flex;
        justify-content: center;
    }
    .start-button > button {
        font-size: 1.2rem;
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 10px;
        transition: 0.3s ease-in-out;
    }
    .start-button > button:hover {
        background-color: #145a86;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Contenu d'accueil ---
    st.markdown("""
    <div class="home-box">
        <h1>🧪 Bienvenue dans le Quiz interactif</h1>
        <p>
            Teste tes connaissances avec un quiz dynamique !<br>
            Clique sur le bouton ci-dessous pour démarrer.
        </p>
    """, unsafe_allow_html=True)

    # --- Bouton démarrer centré ---
    st.markdown('<div class="start-button">', unsafe_allow_html=True)
    if st.button("🚀 Commencer le quiz", key="btn_start"):
        commencer()
        if "questions_melangees" in st.session_state:
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --------- Page quiz actif ---------
else:
    total_questions = len(st.session_state.questions_melangees)
    current = st.session_state.question

    st.title("🧠 Quiz interactif")
    st.markdown(f"### 📍 Question {current + 1} / {total_questions}")
    st.progress((current + 1) / total_questions)

    if current < total_questions:
        question_actuelle = st.session_state.questions_melangees[current]
        afficher_questions(question_actuelle)

        col_g, col_c, col_d = st.columns([1, 2, 1])

        with col_g:
            if st.button("⬅️ Précédent") and current > 0:
                precedent()
                st.rerun()

        with col_d:
            if st.button("➡️ Suivant") and current < total_questions - 1:
                suivant()
                st.rerun()
            if current == total_questions - 1 and st.session_state.reponse_donnee:
                if st.button("📊 Voir la synthèse"):
                    st.session_state["afficher_synthese"] = True
                    st.rerun()

    if st.session_state.get("afficher_synthese", False):
        afficher_synthese()
