import streamlit as st
import datetime
import pandas as pd

df1 = pd.read_excel("Taux.xlsx",sheet_name="TAUX DE PRIMES UNIQUES")

df2 = pd.read_excel("Taux.xlsx",sheet_name="TAUX DE PRIMES UNIQUES AVEC PE")

datetime.datetime.today()
datetime.datetime(2018, 2, 13, 22, 25, 0, 693541)
dj= datetime.datetime.today().strftime("%d/%m/%Y")

c=['DECES-INVALIDITE TOTALE ET DEFINITIVE','DECES-INVALIDITE TOTALE ET DEFINITIVE ET PERTE EMPLOI']

def Taux(data, age, dr):
    c=len(data)
#for i in range(c):
    if age >=18 and age <= 24:
        for i in range(c):
            if data.iloc[i, 0] == dr:
                T=data.iloc[i, 1]
                return T
    else:
        if age >=25 and age <= 29:
             for i in range(c):
                if data.iloc[i, 0] == dr:
                    T=data.iloc[i, 2]
                    return T
        else:
            if age >=30 and age <= 34:
                for i in range(c):
                    if data.iloc[i, 0] == dr:
                        T=data.iloc[i, 3]
                        return T
            else:
                if age >=35 and age <= 39:
                    for i in range(c):
                        if data.iloc[i, 0] == dr:
                            T=data.iloc[i, 4] 
                            return T
                else:
                    if age >=40 and age <= 44:
                        for i in range(c):
                            if data.iloc[i, 0] == dr:
                                T=data.iloc[i, 5]
                                return T
                    else:
                        if age >=45 and age <= 49:
                            for i in range(c):
                                if data.iloc[i, 0] == dr:
                                    T=data.iloc[i, 6]
                                    return T
                        else:
                            if age >=50 and age <= 54:
                                for i in range(c):
                                    if data.iloc[i, 0] == dr:
                                        T=data.iloc[i, 7]
                                        return T
                            else:
                                if age >=55 and age <= 59:
                                    for i in range(c):
                                        if data.iloc[i, 0] == dr:
                                            T=data.iloc[i, 8]
                                            return T
                                else:
                                    if age >=60 and age <= 64:
                                        for i in range(c):
                                            if data.iloc[i, 0] == dr:
                                                T=data.iloc[i, 9] 
                                                return T

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
date = st.sidebar.text_input('Date de demande de pret',dj)
#Montant du pret
dure = st.sidebar.text_input('Durée du pret en Année')

Mt = st.sidebar.text_input('Montant du Pret')

Garantie = st.sidebar.selectbox('Garantie',c)

st.markdown("""<style>
    
    div:nth-child(7) > [class^="css-"] > div:nth-child(1) > div > div > div > button {
        background-color: #DD3300;
        color:#eeffee;
        border-radius: 0.75rem;
        }

    div[id^="bui-"] > button:nth-child(1) {
    background-color: #33DD00;
    color: #EEFFFF;
    }
    </style>""", unsafe_allow_html=True)
    
col1, col2, col3  = st.sidebar.columns(3)

with col1:
    pass
with col3:
    pass
with col2:
    check1 = st.button('SUBMIT')

if check1:
    st.header("**INFORMATION DU CLIENT**")
    
    Age= round((datetime.datetime.strptime(date, "%d/%m/%Y")-datetime.datetime.strptime(dn, "%d/%m/%Y")).days/365,0)
    st.write("**Age du Client : **{:.0f} ans".format(Age))
    st.write("**Montant du Pret : ",(Mt))
    st.write("**Date de D'effet : ",date)
    from datetime import date, timedelta
    #import locale
    today = date.today()
    delta = timedelta(days = int(dure)*365)
    nextWeek = today + delta
    #locale.setlocale(locale.LC_ALL, locale = "fr_FR.UTF-8")
    st.write("**Date d'échéance : ",nextWeek.strftime("%d/%m/%Y"))
    st.write("**Garantie Choisie : ",Garantie)
   
    st.header("**DETAIL DU CALCULE DE LA PRIME**")
    if Garantie=='DECES-INVALIDITE TOTALE ET DEFINITIVE':
        tx=Taux(df1,int(Age),int(dure))
        st.write("**Prime Net a payer : **{:.0f} FCFA".format((int(Mt)*tx)))
        st.write("**Prime Net avec Frais : **{:.0f} FCFA".format((int(Mt)*tx)+500))
        st.write("**Prime TTC : **{:.0f} FCFA".format(((int(Mt)*tx)+500)*1.03))
    else:
        tx=Taux(df2,int(Age),int(dure))
        st.write("**Prime Net a payer : **{:.0f} FCFA".format((int(Mt)*tx)))
        st.write("**Prime Net avec Frais : **{:.0f} FCFA".format((int(Mt)*tx)+500))
        st.write("**Prime TTC : **{:.0f} FCFA".format(((int(Mt)*tx)+500)*1.03))

st.markdown('***')
st.markdown("Merci d'avoir parcouru cette application Web !! ❤️")
