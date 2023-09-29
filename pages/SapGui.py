import streamlit as st
from sap.main import SapGui
import hydralit_components as hc
from streamlit_option_menu import option_menu
import locale

locale.setlocale(locale.LC_ALL, '')

st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

def pa30sayfa():
    pass

def pa40sayfa():
    option_data = [
    {'label':"Giriş"},
    {'label':"PA40"},
    {'label':"PA30"},
    {'label':"Deneme"},
    {'label':"PA30"}
    ]
    font_fmt = {'font-class':'h1','font-size':'100%'}
    op = hc.option_bar(option_definition=option_data,key='PrimaryOption',font_styling=font_fmt,horizontal_orientation=True)
    Durum = SapGui().acıkmı()
    if Durum["Durum"] == "Kapalı.":
        if op == "Giriş":
            if st.button("Giriş"):
                mesaj = SapGui().SapLogin()
                st.info(mesaj)
    
    if op == "PA40":
        if st.button("PA40 Deneme"):
            mesaj = SapGui().pa40()
            st.info(f"{mesaj[0]} adlı persınelin T.C. Kimlik Numarası: {mesaj[1]}")
    if op == "PA30":
        pass

def sapgirisform():

    uygulama = SapGui().acıkmı()
    baglanti = SapGui().baglımı()

    if uygulama["Durum"] == "Kapalı." or baglanti["Durum"] == "Bağlı Değil.":
        with st.form(key='girisform'):
            st.title("SAP GİRİŞ")
            kullaniciadi = st.text_input("Kullanıcı Adı")
            sifre = st.text_input("Şifre", type="password")
            girisbuton = st.form_submit_button(label="GİRİŞ")

            if girisbuton:
                SapGui().SapLogin(kullaniciadi, sifre)
                st.rerun()
        if uygulama["Durum"] == "Kapalı.":
            st.error(uygulama["Mesaj"])
        else:
            col1,col2 = st.columns(2)
            with col1:
                st.warning(uygulama["Mesaj"])
            with col2:
                st.error(baglanti["Mesaj"])
    else:
        giriskontrol = SapGui().girisyapıldımı()
        if giriskontrol == 1:
            st.success(baglanti["Mesaj"])
            kapat = st.button("SAP Uygulamasını Kapat")
            if kapat:
                SapGui().sapKapat()
                st.rerun()
        else:
            st.warning(giriskontrol)
            SapGui().sapKapat()
            Tekrarla = st.button(label="Tekrarla")
            if Tekrarla:
                st.rerun()

def turkish_upper (text):
  upper_map = {
    ord (u'ı'): u'I',
    ord (u'i'): u'İ',
  }
  return text.translate (upper_map).upper ()

def personelArama():
    with st.form(key='Personelara'):
        st.title("Personel Ara")

with st.sidebar:
    selected = option_menu("SAP Menü", ["SAP Giriş","PA30", 'PA40'],default_index=0)
    if selected == "PA30":
        with st.form(key='Perara',clear_on_submit=True):
            tab1, tab2 = st.tabs(["T.C./Per.No","Ad Soyad"])
            with tab1:
                arananpersonel = st.text_input (label="Personel Ara",placeholder="T.C. YADA PERSONEL NUMARASI")
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    ad = st.text_input (label="Personel Ara",placeholder="AD")
                    if ad == "":
                        ad = "."
                with col2:
                    soyad = st.text_input (label="",placeholder="SOYAD")
                    if soyad == "":
                        soyad = "."

            if arananpersonel.isnumeric():            
                if len(arananpersonel) == 11:
                    arananpersonel = "=..." + arananpersonel
            else:
                arananpersonel = "="+soyad+"."+ad
                
            aramayap = st.form_submit_button(label="Ara")
            if aramayap:
                SapGui().personelara(turkish_upper(arananpersonel))

        
if selected == "SAP Giriş":
    sapgirisform()

if selected == "PA30":
    pa30sayfa()

if selected == "PA40":
    pa40sayfa()