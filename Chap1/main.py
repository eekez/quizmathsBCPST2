import streamlit as st
from utils import commencer, afficher_questions, questions, suivant, precedent, verifier_reponse


st.set_page_config(page_title="Quiz Chapitre 1 - Les suites", layout="centered", initial_sidebar_state="collapsed")


if "question" not in st.session_state or st.session_state.question==-1:
    st.title("🧠 Chapitre 1 - Révision sur les suites")
    st.write("Ce quiz comporte plusieurs questions. Cliquez sur **Commencer** pour démarrer.")
    st.button("➡️ Commencer", on_click=commencer())

elif  st.session_state.question< len(questions)-1: 
    
    afficher_questions(questions[st.session_state.question])
    verifier_reponse(st.session_state.reponse_util, questions[st.session_state.question]["reponse"],questions[st.session_state.question])
    
    st.button("Suivant",on_click=suivant)
    st.button("Précédent",on_click=precedent)

elif st.session_state.question==len(questions)-1: 
    afficher_questions(questions[st.session_state.question])
    verifier_reponse(st.session_state.reponse_util, questions[st.session_state.question]["reponse"],questions[st.session_state.question])
    
    st.button("Terminer", on_click=suivant) 
    st.button("Précédent", on_click=precedent)
    

else: 
    st.write("Bravo d'avoir terminé ce quiz")
