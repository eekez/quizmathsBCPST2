import streamlit as st
import json
import random
import os


# --------------------- Fonctions utilitaires ---------------------

def est_latex(s):
    return s.strip().count("$") > 1

def afficher_boite(couleur_hex, titre, contenu):
    st.markdown(f"""
    <div style='background-color:{couleur_hex}; padding: 1rem; border-radius: 10px; margin: 1rem 0; color: #000000;'>
        <strong>{titre}</strong><br>
        {contenu}
    </div>
    """, unsafe_allow_html=True)


def afficher_boite_explication(titre, contenu):
    st.markdown("""
        <div class="boite-explication">
            <h4>{}</h4>
        </div>
    """.format(titre), unsafe_allow_html=True)

    st.write("- "+contenu)


def afficher_boite_solution(bonnes_reponses):
    st.markdown("""
        <div style="border-left: 6px solid #1f77b4; background-color: #e6f2ff;
                    padding: 1rem; border-radius: 12px; margin: 1.5rem 0; color: #111;">
            <h4>📘 Solution</h4>
            <p>Voici la ou les bonnes réponses :</p>
        </div>
    """, unsafe_allow_html=True)

    for rep in bonnes_reponses:
        st.write("- "+rep)



# --------------------- Chargement des questions ---------------------

def charger_questions():
    chemin = os.path.join(os.path.dirname(__file__), "questions.json")
    try:
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("❌ Fichier 'questions.json' introuvable.")
        return []


# --------------------- Initialisation ---------------------

def commencer():
    st.session_state.questions_melangees = charger_questions()
    random.shuffle(st.session_state.questions_melangees)
    st.session_state.question = 0
    st.session_state.reponses_utilisateur = []
    st.session_state.bonne_reponse_validee = False
    st.session_state.reponse_donnee = False


# --------------------- Navigation ---------------------

def suivant():
    st.session_state.question += 1
    st.session_state.bonne_reponse_validee = False
    st.session_state.reponse_donnee = False


def precedent():
    if st.session_state.question > 0:
        st.session_state.question -= 1
        st.session_state.bonne_reponse_validee = True
        st.session_state.reponse_donnee = True


# --------------------- Affichage d'une question ---------------------

def afficher_questions(q):
    # Appliquer le CSS une seule fois
    if "css_applique" not in st.session_state:
        st.markdown("""
            <style>
            .checkbox-button label {
                background-color: white !important;
                color: black !important;
                border: 2px solid #1f77b4;
                border-radius: 8px;
                padding: 0.5em 1em;
                display: block;
                margin-bottom: 0.5em;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .checkbox-button input:checked + label {
                background-color: #cce5ff !important;
                border-color: #1f77b4 !important;
            }
            </style>
        """, unsafe_allow_html=True)
        st.session_state.css_applique = True

    multi = isinstance(q["reponse"], list)
    bonnes = set(q["reponse"] if multi else [q["reponse"]])

    st.write(f"### {q['question']}")
    key_prefix = f"q_{st.session_state.question}"

    # Initialiser les états des options si jamais absent
    for i in range(len(q["options"])):
        opt_key = f"{key_prefix}_opt_{i}"
        if opt_key not in st.session_state:
            st.session_state[opt_key] = False

    # Affichage des checkboxes
    donnees = []
    for i, option in enumerate(q["options"]):
        opt_key = f"{key_prefix}_opt_{i}"
        checked = st.session_state[opt_key]
        if st.checkbox(option, key=opt_key):
            donnees.append(option)

    st.session_state.reponse_donnee = bool(donnees)

    # Bouton valider
    if st.button("✅ Valider mes réponses", key=f"{key_prefix}_valider"):
        deja_ajoute = any(d["question"] == q["question"] for d in st.session_state.reponses_utilisateur)
        if not deja_ajoute:
            st.session_state.reponses_utilisateur.append({
            "question": q["question"],
            "donnee": donnees,
            "bonne_reponse": list(bonnes),
            "explication": q.get("explication", ""),
            "explications_fautes": q.get("explications_fautes", {})
            })

        def nettoyer(texte):
                return texte.strip().replace("≥", "\\geqslant")

        donnees_nettoyees = set(nettoyer(rep) for rep in donnees)
        bonnes_nettoyees = set(nettoyer(rep) for rep in bonnes)
        if set(donnees_nettoyees) == bonnes_nettoyees:
            st.success("✅ Bonne réponse !")
            st.session_state.bonne_reponse_validee = True
            st.balloons()
        elif set(donnees).issubset(bonnes) and len(set(donnees)) < len(bonnes):
            st.warning("🟨 Ta réponse est juste mais il reste d'autres bonnes réponses à trouver.")
            st.session_state.bonne_reponse_validee = False
        else:
            st.error("❌ Mauvaise réponse")
            st.session_state.bonne_reponse_validee = False

        explications_fautes = q.get("explications_fautes", {})
        for mauvaise in set(donnees) - bonnes:
            if mauvaise in explications_fautes:
                afficher_boite_explication("💡 Explication", explications_fautes[mauvaise])


    # Si la réponse est déjà validée et fausse, réafficher explications
    elif st.session_state.get(f"{key_prefix}_valide", False):
        donnees = [opt for i, opt in enumerate(q["options"])
                   if st.session_state.get(f"{key_prefix}_opt_{i}", False)]
        explications_fautes = q.get("explications_fautes", {})
        for mauvaise in set(donnees) - bonnes:
            if mauvaise in explications_fautes:
                afficher_boite_explication("💡 Explication", explications_fautes[mauvaise])


    # Affichage du bouton "Voir la solution"
    if (
        st.session_state.reponse_donnee
        and not st.session_state.bonne_reponse_validee
    ):
        if st.button("📘 Voir la solution", key=f"{key_prefix}_voir_solution_btn"):
            st.session_state[f"voir_solution_{st.session_state.question}"] = True

    if st.session_state.get(f"voir_solution_{st.session_state.question}", False):
        afficher_boite_solution(bonnes)


# --------------------- Synthèse ---------------------




def afficher_synthese():
    st.markdown("## 📊 Synthèse de vos réponses")
    for rep in st.session_state.reponses_utilisateur:
        st.markdown("---")
        st.markdown(f"**🧩 Question :** {rep['question']}")

        # Réponses données par l'utilisateur
        st.markdown("**📝 Votre réponse :**")
        if rep["donnee"]:
            for val in rep["donnee"]:
                st.write("-> " + val)
        else:
            st.markdown("*Aucune réponse sélectionnée.*")

        # Si réponse correcte
        if set(rep["donnee"]) == set(rep["bonne_reponse"]):
            afficher_boite("#d4edda", "✅ Bonne réponse", "Vous avez bien répondu à cette question.")
        else:
            afficher_boite("#f8d7da", "❌ Mauvaise réponse", "La ou les réponse(s) donnée(s) n'étaient pas correctes.")

            # Bloc explication si erreurs
            if rep.get("explications_fautes"):
                erreurs = set(rep["donnee"]) - set(rep["bonne_reponse"])
                for err in erreurs:
                    if err in rep["explications_fautes"]:
                        afficher_boite("#fff3cd", "💡 Explication", rep["explications_fautes"][err])

            # Bloc solution
            contenu = ""
            afficher_boite("#cce5ff", "📘 Solution(s) correcte(s)", contenu)

            for val in rep["bonne_reponse"]:
                st.write("- " + val)
