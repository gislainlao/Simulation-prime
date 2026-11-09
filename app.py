import streamlit as st
import datetime
import calendar
import pandas as pd


# ==========================================================
# 1. CONFIGURATION DE L'APPLICATION
# ==========================================================

st.set_page_config(
    page_title="Simulateur de primes d'assurance",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# 2. CHARGEMENT DU FICHIER EXCEL
# ==========================================================

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
    st.error(
        f"Erreur lors du chargement du fichier Taux.xlsx : {e}"
    )
    st.stop()


# ==========================================================
# 3. PARAMETRES DE TARIFICATION
# ==========================================================

garanties = [
    "DECES-INVALIDITE TOTALE ET DEFINITIVE",
    "DECES-INVALIDITE TOTALE ET DEFINITIVE ET PERTE EMPLOI"
]

tranches_age = [
    (18, 24),
    (25, 29),
    (30, 34),
    (35, 39),
    (40, 44),
    (45, 49),
    (50, 54),
    (55, 59),
    (60, 64)
]


# ==========================================================
# 4. FONCTION DE CALCUL DU TAUX
# ==========================================================

def Taux(data, age, duree):

    # Vérification de l'âge
    if age < 18 or age > 64:
        raise ValueError(
            "L'âge du client doit être compris entre 18 et 64 ans."
        )

    # Vérification de la durée
    if duree < 1 or duree > 15:
        raise ValueError(
            "La durée du prêt doit être comprise entre 1 et 15 ans."
        )

    # Identification de la tranche d'âge
    colonne = None

    for i, (minimum, maximum) in enumerate(tranches_age):

        if minimum <= age <= maximum:
            colonne = i + 1
            break

    # Vérification de la disponibilité de la tranche
    if colonne is None or colonne >= data.shape[1]:

        raise ValueError(
            "Tranche d'âge non disponible pour cette garantie."
        )

    # Recherche de la durée dans la première colonne
    durees = pd.to_numeric(
        data.iloc[:, 0],
        errors="coerce"
    )

    ligne = data[durees == duree]

    if ligne.empty:

        raise ValueError(
            "Durée non disponible dans le fichier de tarification."
        )

    # Extraction du taux
    taux = pd.to_numeric(
        ligne.iloc[0, colonne],
        errors="coerce"
    )

    # Vérification de la disponibilité du taux
    if pd.isna(taux):

        raise ValueError(
            "Aucun taux disponible pour cette combinaison "
            "âge / durée / garantie."
        )

    return float(taux)


# ==========================================================
# 5. FONCTIONS COMPLEMENTAIRES
# ==========================================================

def calcul_age(date_naissance, date_effet):

    age = (
        date_effet.year - date_naissance.year
        - (
            (date_effet.month, date_effet.day)
            < (date_naissance.month, date_naissance.day)
        )
    )

    return age


def calcul_date_echeance(date_effet, duree):

    annee = date_effet.year + duree

    jour = min(
        date_effet.day,
        calendar.monthrange(annee, date_effet.month)[1]
    )

    return datetime.date(
        annee,
        date_effet.month,
        jour
    )


def format_fcfa(montant):

    return f"{montant:,.0f}".replace(",", " ") + " FCFA"


# ==========================================================
# 6. PERSONNALISATION DE L'INTERFACE
# ==========================================================

st.markdown("""
<style>

.main-title {
    background-color: tomato;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-size: 27px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


st.markdown(
    """
    <div class="main-title">
        PLATEFORME DE SIMULATION DE PRIME D'ASSURANCE
    </div>
    <div class="subtitle">
        Calcul de la prime d'assurance emprunteur
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# 7. FORMULAIRE DE SAISIE
# ==========================================================

st.sidebar.header("INFORMATIONS GENERALES")

with st.sidebar.form("formulaire_simulation"):

    st.subheader("Informations du client")

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

    dure = st.number_input(
        "Durée du prêt en année",
        min_value=1,
        max_value=15,
        value=5,
        step=1
    )

    Mt = st.number_input(
        "Montant du prêt (FCFA)",
        min_value=1,
        value=1000000,
        step=100000
    )

    Garantie = st.selectbox(
        "Garantie",
        garanties
    )

    st.markdown("---")

    check1 = st.form_submit_button(
        "SIMULER LA PRIME",
        use_container_width=True
    )


# ==========================================================
# 8. CALCUL ET AFFICHAGE DES RESULTATS
# ==========================================================

if check1:

    try:

        # --------------------------------------------------
        # Calcul de l'âge du client
        # --------------------------------------------------

        Age = calcul_age(
            date_naissance,
            date_demande
        )

        if date_demande < date_naissance:

            raise ValueError(
                "La date de demande de prêt ne peut pas "
                "être antérieure à la date de naissance."
            )

        # --------------------------------------------------
        # Calcul de la date d'échéance
        # --------------------------------------------------

        date_echeance = calcul_date_echeance(
            date_demande,
            int(dure)
        )

        # --------------------------------------------------
        # Choix de la table de tarification
        # --------------------------------------------------

        if Garantie == garanties[0]:

            data = df1

        else:

            data = df2

        # --------------------------------------------------
        # Extraction du taux
        # --------------------------------------------------

        tx = Taux(
            data,
            Age,
            int(dure)
        )

        # --------------------------------------------------
        # Calcul de la prime
        # --------------------------------------------------

        prime_nette = Mt * tx

        cout_police = 500

        taxe = (
            prime_nette + cout_police
        ) * 0.03

        prime_ttc = (
            prime_nette
            + cout_police
            + taxe
        )

        # ==================================================
        # 9. AFFICHAGE DES INFORMATIONS CLIENT
        # ==================================================

        st.success("Simulation réalisée avec succès !")

        st.header("INFORMATIONS DU CLIENT")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Âge du client",
                f"{Age} ans"
            )

        with col2:

            st.metric(
                "Montant du prêt",
                format_fcfa(Mt)
            )

        with col3:

            st.metric(
                "Durée du prêt",
                f"{int(dure)} ans"
            )

        st.write(
            "**Date de naissance :**",
            date_naissance.strftime("%d/%m/%Y")
        )

        st.write(
            "**Date de demande de prêt :**",
            date_demande.strftime("%d/%m/%Y")
        )

        st.write(
            "**Date d'échéance :**",
            date_echeance.strftime("%d/%m/%Y")
        )

        st.write(
            "**Garantie choisie :**",
            Garantie
        )

        # ==================================================
        # 10. DETAIL DU CALCUL DE LA PRIME
        # ==================================================

        st.markdown("---")

        st.header("DÉTAILS DU CALCUL DE LA PRIME")

        st.write(
            f"**Taux appliqué :** {tx:.6%}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Prime nette à payer",
                format_fcfa(prime_nette)
            )

            st.metric(
                "Coût de police",
                format_fcfa(cout_police)
            )

        with col2:

            st.metric(
                "Taxe (3 %)",
                format_fcfa(taxe)
            )

            st.metric(
                "Prime TTC",
                format_fcfa(prime_ttc)
            )

        # ==================================================
        # 11. RECAPITULATIF
        # ==================================================

        st.markdown("---")

        st.subheader("RÉCAPITULATIF DE LA SIMULATION")

        recap = pd.DataFrame({

            "Désignation": [
                "Prime nette",
                "Coût de police",
                "Taxe",
                "Prime TTC"
            ],

            "Montant (FCFA)": [
                prime_nette,
                cout_police,
                taxe,
                prime_ttc
            ]

        })

        recap["Montant (FCFA)"] = recap[
            "Montant (FCFA)"
        ].apply(lambda x: f"{x:,.0f}".replace(",", " "))

        st.table(recap)

        # ==================================================
        # 12. EXPORT EXCEL DU RESULTAT
        # ==================================================

        export = pd.DataFrame({

            "Informations": [
                "Date de naissance",
                "Âge",
                "Montant du prêt",
                "Durée du prêt",
                "Date d'effet",
                "Date d'échéance",
                "Garantie",
                "Taux appliqué",
                "Prime nette",
                "Coût de police",
                "Taxe",
                "Prime TTC"
            ],

            "Valeurs": [
                date_naissance.strftime("%d/%m/%Y"),
                Age,
                Mt,
                int(dure),
                date_demande.strftime("%d/%m/%Y"),
                date_echeance.strftime("%d/%m/%Y"),
                Garantie,
                tx,
                prime_nette,
                cout_police,
                taxe,
                prime_ttc
            ]

        })

        fichier_excel = None

        import io

        fichier_excel = io.BytesIO()

        with pd.ExcelWriter(
            fichier_excel,
            engine="openpyxl"
        ) as writer:

            export.to_excel(
                writer,
                index=False,
                sheet_name="Simulation"
            )

        st.download_button(
            label="📥 Télécharger la simulation Excel",
            data=fichier_excel.getvalue(),
            file_name="Simulation_Prime.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

        # ==================================================
        # 13. MESSAGE DE FIN
        # ==================================================

        st.markdown("---")

        st.markdown(
            """
            Merci d'avoir utilisé cette application !

            Pour me contacter, retrouvez-moi sur
            [LinkedIn](https://www.linkedin.com/in/essohanam-laokpezi/)
            ❤️
            """
        )

    except Exception as e:

        st.error(
            f"Impossible de réaliser la simulation : {e}"
        )
