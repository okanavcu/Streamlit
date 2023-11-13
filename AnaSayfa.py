import streamlit as st
from streamlit_option_menu import option_menu
import win32com.client as win32
from database.supabaseConnect import Eylemler
from streamlit_extras.switch_page_button import switch_page
import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

try:
    if 'session' in st.session_state:
        switch_page("sgk")
except:
    pass


def kayıtMail():
    outlook = win32.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)
    mail.Importance = 2
    mail.To = "oavcu@bilkentohm.com.tr"
    mail.Subject = "SGK SİSTEM UYGULAMASI KULLANICI KAYDI HK."
    html_body = f"""
                <br><strong>Sn. İlgili,</strong></br><br></br>
                <br>SGK Sistem uygulamasına kullanıcı kaydımın yapılmaısı konusunda desteklerinizi beklerim.</br><br></br>
                <br>Şirket Kodu: {sirketler}</br>
                <br>Bölge: {bolgeler}</br>
                <p>İyi çalışmalar dilerim.</p>
                """   
    mail.HTMLBody = html_body
    mail.Send()
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
    sirketler = kayitForm.multiselect(label="Sirketleri yazınız.",placeholder="Bu alan admin tarafından girilecek ve size mail ile bildirilecektir.",
    options=["TEPE İŞ SAĞLIĞI VE GÜVENLİĞİ A.Ş.",
            "TEPE SAVUNMA VE GÜVENLİK SİSTEMLERİ A.Ş.",
            "TEPE SERVİS VE YÖNETİM A.Ş.",
            "ADONİS ENDÜSTRİYEL TEMİZLİK ÜRÜNLERİ A.Ş.",
            "TEPE SERVİS KART HİZMETLERİ A.Ş.",
            "BCC TOPLU YEMEK A.Ş.",
            "TEPE DESTEK HİZMETLERİ A.Ş.",
            "BİLKENT OHM DANIŞMANLIK HİZMETLERİ A.Ş."])
    bolgeler = kayitForm.multiselect("Bölgenizi yazınız.",placeholder="Bu alan admin tarafından girilecek ve size mail ile bildirilecektir.",
    options=["AKDENİZ","İDARİ İŞYERİ","ÇUKUROVA","MERKEZ","MARMARA","BURSA","EGE"])
    kayitButon = kayitForm.form_submit_button("Kayıt Ol",use_container_width=True,type="primary")
    if kayitButon:
        session = sessionKaydol()
        kayıtMail()
        if st.session_state.session != None:
            st.success(body="Kaydınız Gerçekleştirldi. Yrkki ayarlarınız admin tarafından yapıldıktan sonra uygulamayı kullanabilirsiniz. İyi çalışmalar.")
        else:
            st.error("Kayıt işlemi başarısız. Tekrar deneyiniz.")


