import streamlit as st
from sap.main import SapGui
import hydralit_components as hc
from streamlit_option_menu import option_menu


st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

def pa30sayfa():
    option_data = [
    {'label':"Giriş"},
    {'label':"PA40"},
    {'label':"PA30"},
    {'label':"Deneme"},
    {'label':"PA30"}
    ]
    font_fmt = {'font-class':'h1','font-size':'100%'}
    op = hc.option_bar(option_definition=option_data,key='PrimaryOption',font_styling=font_fmt,horizontal_orientation=True)
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
    with st.form(key='girisform'):
        st.title("SAP GİRİŞ")
        kullaniciadi = st.text_input("Kullanıcı Adı")
        sifre = st.text_input("Şifre", type="password")
        girisbuton = st.form_submit_button(label="GİRİŞ")

        if girisbuton:
            mesaj = SapGui().SapLogin(kullaniciadi, sifre)
            st.success(mesaj)


with st.sidebar:
    selected = option_menu("SAP Menü", ["SAP Giriş","PA30", 'PA40'],default_index=0)

if selected == "SAP Giriş":
    sapgirisform()

if selected == "PA30":
    pa30sayfa()

if selected == "PA40":
    pa40sayfa()