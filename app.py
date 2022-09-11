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

if check1:
    st.header("**INFORMATION DU CLIENT**")
    
    Age= round((datetime.strptime(date, "%d/%m/%Y")-datetime.strptime(dn, "%d/%m/%Y")).days/365,0)
    st.write("**Age du Client : **{:.0f} ans".format(Age))
    st.write("**Montant du Pret : ",(Mt))
    st.write("**Date de D'effet : ",date)
    from datetime import date, timedelta
    import locale
    today = date.today()
    delta = timedelta(days = int(dure)*365)
    nextWeek = today + delta
    locale.setlocale(locale.LC_ALL, locale = "FR_fr")
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
