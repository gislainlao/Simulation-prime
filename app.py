import streamlit as st
import datetime


datetime.datetime.today()
datetime.datetime(2018, 2, 13, 22, 25, 0, 693541)
dj= datetime.datetime.today().strftime("%d/%m/%Y")

c=['DECES-INVALIDITE TOTALE ET DEFINITIVE','DECES-INVALIDITE TOTALE ET DEFINITIVE ET PERTE EMPLOI']


    #Title display
html_temp = """
<div style="background-color: tomato; padding:10px; border-radius:10px">
<h1 style="color: white; text-align:center">PLATEFORM DE SIMULATION DE CREDIT</h1>
</div>
<p style="font-size: 20px; font-weight: bold; text-align:center">Calcul de la prime…</p>
"""
st.markdown(html_temp, unsafe_allow_html=True)
#Customer ID selection

st.sidebar.header("**INFORMATION GENERAL**")

dn = st.sidebar.text_input('Date de Naissance')
#Loading selectbox
date = st.sidebar.text_input('Date de demande de ret',dj)
#Montant du pret
dure = st.sidebar.text_input('Durée du pret en Année')

Mt = st.sidebar.text_input('Montant du Pret')

Garantie = st.sidebar.selectbox('Garantie',c)

check1 = st.sidebar.button("SIMULATION")
