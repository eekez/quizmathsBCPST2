
import streamlit as st

questions = [
    {"question": f"Une suite qui ne converge pas tend vers $+\infty$ ou $-\infty$." ,
     "options": ["Vrai","Faux"] , 
     "reponse": "Faux" ,
     "explication": r"test"},

    {"question": r"Si $(u_{2n})$ et $(u_{2n+1})$ convergent alors $(u_n)$ converge.",
      "options": ["Vrai","Faux"],
      "reponse": "Faux",
      "explication": r"Contre-exemple : $u_n = (-1)^n$" },

     {"question": r"Seule une des méthodes suivantes permet d'affirmer que $(u_n)$ converge. Laquelle ?",
      "options": ["On montre que $(u_{2n})$ et $u_{2n + 1})$ sont des suites adjacentes","On étudie le signe de $u_{n+ 1} - u_n$ pour tout $n \in \mathbb{N}$.","On montre que $(u_n)$ est bornée","On calcule quelques valeurs de la suite, et on constate qu'elle semble se rapprocher d'une valeur"],
      "reponse": r"On montre que $(u_{2n})$ et $u_{2n + 1})$ sont des suites adjacentes",
      "explication": r"Contre-exemple : $u_n = (-1)^n$" }

 
]

def afficher_questions(dico) : 
    
    st.session_state.reponse_util = None

    st.write(dico["question"])

    cols = st.columns([1,10],vertical_alignment="center")

    for i, formula in enumerate(dico["options"]):
        if st.button(formula, key=f"btn_{i}"):  # Bouton simple
            st.session_state.reponse_util = formula

def verifier_reponse(reponse_util, bonne_reponse, question): 
    if reponse_util != bonne_reponse and reponse_util != None: 
        st.error("Essaye encore")
        st.write(question["explication"])
    elif reponse_util == bonne_reponse and reponse_util != None: 
        st.success("Bravo !")
        




def commencer():
    import streamlit as st
    st.session_state["question"] = 0

def suivant() :
    import streamlit as st 
    st.session_state.question= st.session_state.question + 1

def precedent() : 
    import streamlit as st 
    st.session_state.question= st.session_state.question- 1


    