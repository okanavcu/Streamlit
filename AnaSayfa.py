import streamlit as st
from streamlit_option_menu import option_menu
from database.supabaseConnect import Eylemler
from streamlit_extras.switch_page_button import switch_page
import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                display: none
            }

            [data-testid="collapsedControl"] {
                display: none
            }
            </style>
            """, unsafe_allow_html=True)

def sessionAl():
    st.session_state.session = Eylemler.giris(mail=mail,sifre=parola)

def sessionKaydol():
    st.session_state.session = Eylemler.kayitOl(mail=mail,sifre=parola,ad=ad,soyad=soyad,bolge=bolgeler,sirket=sirketler)

tab1, tab2 = st.tabs(["GİRİŞ", "KAYIT OL"])

with tab1:
    girisForm = st.form("GİRİŞ",clear_on_submit=True)
    girisForm.title("Giriş")
    mail = girisForm.text_input("Mail",placeholder="E-mailinizi giriniz.")
    parola = girisForm.text_input("Şifre",placeholder="Şifrenizi giriniz.",type="password")
    girisButon = girisForm.form_submit_button("Giri Yap.",use_container_width=True,type="primary")
    if girisButon:
        session = sessionAl()
        if st.session_state.session != None:
            switch_page("sgk")
with tab2:
    kayitForm = st.form("KAYIT OL.",clear_on_submit=True)
    kayitForm.title("Kayıt ol")
    mail = kayitForm.text_input("Mail",placeholder="E-mailinizi giriniz.")
    parola = kayitForm.text_input("Şifre",placeholder="Şifrenizi giriniz.",type="password")
    ad = kayitForm.text_input("Adınız.",placeholder="Adınızı giriniz")
    soyad = kayitForm.text_input("Soyadınız.",placeholder="Soyadınızı giriniz")
    sirketler = kayitForm.text_area("Sirketleri yazınız.",placeholder=("Bu alan admin tarafından girilecek ve size mail ile bildirilecektir."))
    bolgeler = kayitForm.text_area("Bölgenizi yazınız.",placeholder=("Bu alan admin tarafından girilecek ve size mail ile bildirilecektir."))
    kayitButon = kayitForm.form_submit_button("Giri Yap.",use_container_width=True,type="primary")
    if kayitButon:
        session = sessionKaydol()
        if st.session_state.session != None:
            switch_page("sgk")


