
import streamlit as st
import datetime
import pandas as pd

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Simulateur de primes d'assurance",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# CHARGEMENT DES DONNEES EXCEL
# --------------------------------------------------

@st.cache_data
def charger_donnees():
    df1 = pd.read_excel(
        "Taux.xlsx",
        sheet_name="TAUX DE PRIMES UNIQUES"
    )

    df2 = pd.read_excel(
        "Taux.xlsx",
        sheet_name="TAUX DE PRIMES UNIQUES AVEC PE"
    )

    return df1, df2


try:
    df1, df2 = charger_donnees()
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier Excel : {e}")
    st.stop()


# --------------------------------------------------
# PARAMETRES
# --------------------------------------------------

garanties = [
    "DECES-INVALIDITE TOTALE ET DEFINITIVE",
    "DECES-INVALIDITE TOTALE ET DEFINITIVE ET PERTE EMPLOI"
]

# --------------------------------------------------
# FONCTION DE CALCUL DU TAUX
# --------------------------------------------------

def Taux(data, age, duree):

    if age < 18 or age > 64:
        raise ValueError("L'âge doit être compris entre 18 et 64 ans.")

    if duree < 1 or duree > 9:
        raise ValueError("Durée non prise en charge.")

    # Détermination de la tranche d'âge
    tranche = (age - 18) // 5

    # Correspondance avec les colonnes Excel
    colonne = tranche + 1

    # Recherche du taux correspondant à la durée
    ligne = data[data.iloc[:, 0] == duree]

    if ligne.empty:
        raise ValueError(
            f"Aucun taux trouvé pour une durée de {duree} ans."
        )

    taux = ligne.iloc[0, colonne]

    if pd.isna(taux):
        raise ValueError("Le taux correspondant est indisponible.")

    return float(taux)


# --------------------------------------------------
# INTERFACE
# --------------------------------------------------

st.markdown("""
<div style="
    background-color: tomato;
    padding: 15px;
    border-radius: 10px;
">
<h1 style="color:white; text-align:center;">
PLATEFORME DE SIMULATION DE PRIME D'ASSURANCE
</h1>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;font-size:20px;font-weight:bold;'>"
    "Calcul de la prime d'assurance</p>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# FORMULAIRE CLIENT
# --------------------------------------------------

st.sidebar.header("INFORMATIONS GENERALES")

with st.sidebar.form("formulaire_simulation"):

    date_naissance = st.date_input(
        "Date de naissance",
        value=datetime.date(1995, 1, 1),
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date.today(),
        format="DD/MM/YYYY"
    )

    date_demande = st.date_input(
        "Date de demande de prêt",
        value=datetime.date.today(),
        format="DD/MM/YYYY"
    )

    duree = st.number_input(
        "Durée du prêt (en années)",
        min_value=1,
        max_value=50,
        value=10,
        step=1
    )

    montant = st.number_input(
        "Montant du prêt (FCFA)",
        min_value=1,
        value=1000000,
        step=100000
    )

    garantie = st.selectbox(
        "Garantie",
        garanties
    )

    submit = st.form_submit_button(
        "SIMULER LA PRIME",
        use_container_width=True
    )


# --------------------------------------------------
# CALCUL DE LA SIMULATION
# --------------------------------------------------

if submit:

    try:

        # Calcul de l'âge exact
        age = (
            date_demande.year - date_naissance.year
            - (
                (date_demande.month, date_demande.day)
                < (date_naissance.month, date_naissance.day)
            )
        )

        # Date d'échéance
        date_echeance = (
            date_demande
            + datetime.timedelta(days=int(duree * 365.25))
        )

        # Choix du fichier de taux
        if garantie == garanties[0]:
            data = df1
        else:
            data = df2

        # Recherche du taux
        tx = Taux(data, age, int(duree))

        # Calcul des primes
        prime_nette = montant * tx
        cout_police = 500
        taxe = (prime_nette + cout_police) * 0.03
        prime_ttc = prime_nette + cout_police + taxe

        # --------------------------------------------------
        # AFFICHAGE DES RESULTATS
        # --------------------------------------------------

        st.success("Simulation réalisée avec succès !")

        st.header("INFORMATIONS DU CLIENT")

        col1, col2, col3 = st.columns(3)

        col1.metric("Âge du client", f"{age} ans")
        col2.metric("Montant du prêt", f"{montant:,.0f} FCFA")
        col3.metric("Durée du prêt", f"{int(duree)} ans")

        st.write("**Date d'effet :**", date_demande.strftime("%d/%m/%Y"))

        st.write(
            "**Date d'échéance :**",
            date_echeance.strftime("%d/%m/%Y")
        )

        st.write("**Garantie choisie :**", garantie)

        st.divider()

        st.header("DÉTAILS DU CALCUL DE LA PRIME")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Prime nette",
                f"{prime_nette:,.0f} FCFA"
            )

            st.metric(
                "Coût de police",
                f"{cout_police:,.0f} FCFA"
            )

        with col2:
            st.metric(
                "Taxe (3 %)",
                f"{taxe:,.0f} FCFA"
            )

            st.metric(
                "Prime TTC",
                f"{prime_ttc:,.0f} FCFA"
            )

        st.markdown("---")

        st.markdown(
            "Merci d'avoir utilisé cette application ! "
            "[Me contacter sur LinkedIn](https://www.linkedin.com/in/essohanam-laokpezi/)"
        )

    except Exception as e:
        st.error(f"Impossible de réaliser la simulation : {e}")
