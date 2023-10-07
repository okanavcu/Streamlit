import time
import streamlit as st
from sap.main import SapGui
import hydralit_components as hc
from streamlit_option_menu import option_menu
import locale
from streamlit_extras.grid import grid

locale.setlocale(locale.LC_ALL, '')



st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)


def clear():
    st.cache_resource.clear()

def pa30sayfa():
    SapGui().pa30()


def pa40sayfa():
    pa40Acıldımı = SapGui().pa40()
    if pa40Acıldımı != "Personel işlemleri dizisi":
        SapGui().yeniPencere()
        SapGui().pa40()


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
sidebar = st.sidebar
with sidebar:
    selected = option_menu("SAP Menü", ["SAP Giriş","PA30", 'PA40'],default_index=0)

def perbilpan():
    personelbilgileri = st.container()
    if personelbilgileri:
        if selected != "SAP Giriş":
            liste = SapGui().personelBilgi()
            with st.expander(f"{liste['İsim Soyisim']} - {liste['Personel No']} - {liste['T.C.']}",expanded=True):
                my_grid = grid([2,2,4],5, vertical_align="top")
                my_grid.text(body=f"{liste['Şireket']}")
                my_grid.text(body=f"{liste['PYP']}")
                my_grid.text(body=f"{liste['Proje Adı']}")
                my_grid.text(body=f"{liste['Proje Kodu']}")
                my_grid.text(body=f"{liste['istihdam']}")
                my_grid.text(body=f"{liste['Kanun']}")
                my_grid.text(body=f"{liste['Geçerlilik Tarihi']}")
                my_grid.text(body=f"{liste['Yaka']}")

def perislem():
    personelislemleri = st.container()
    if personelislemleri:
        if selected != "SAP Giriş":
            my_grid = grid(1,[1,1,1,1],1, vertical_align="top")
            with open(r'C:\Users\okan.avcu\Desktop\PROGRAMLAR\PYTHON\Streamlit\sap\islemler.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            options_dict = {}
            for line in lines:
                key, value = line.strip().split(':')
                options_dict[key.strip(" '")] = str(value.strip(" ,\n"))

            selected_value = my_grid.selectbox(label="Bilgi Tipi Metni", options=list(options_dict.keys()),on_change=None,index=None)
            detay = my_grid.button(label="Detay",use_container_width=True)
            sil = my_grid.button(label="Sil",use_container_width=True)
            kopyala = my_grid.button(label="Kopyala",use_container_width=True)
            düzenle = my_grid.button(label="Değiştir",use_container_width=True)
            if detay:
                df = tablogetir(options_dict[selected_value])
                df.insert(0,"Seç",0)
                st.data_editor(df,column_config={"Seç": st.column_config.CheckboxColumn(label="Seç",default=False,)},hide_index=True,)


def tablogetir(tipno):
    df = SapGui().detaygetir(tipno)
    return df

if selected == "SAP Giriş":
    sapgirisform()


if selected == "PA30":
    pa30sayfa()
    perbilpan()
    perislem()
    with sidebar:
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
                
            aramayap = st.form_submit_button(label="Ara",use_container_width=True,on_click=None)
            

        if aramayap:
            def bulunansecim():
                secilen_deger = st.session_state.secilen_deger
                aranacaksicil = secilen_deger.split(" | ")[2]
                SapGui().personelara(aranacaksicil)                
                
            SapGui().personelara(turkish_upper(arananpersonel))
            bulunanliste = SapGui().bulunanPersonel()

            if bulunanliste.empty:
                st.write("Hiçbir sonuç bulunamadı.")
            else:
                secilen_deger = st.selectbox(label="Bulunan Personeller",
                options=bulunanliste['Ad Soyad'].astype(str) +
                " | " + bulunanliste['T.C.'].astype(str) + " | " + bulunanliste['Personel Numarası'].astype(str) + " | "
                + bulunanliste['Alt Alan'].astype(str) + " | " + bulunanliste['PYP'].astype(str) + " | " +
                bulunanliste['Proje'].astype(str) + " | " + bulunanliste['Doğum Tarihi'].astype(str),
                key='secilen_deger', index=None,on_change=bulunansecim)

if selected == "PA40":
    pa40sayfa()
    perbilpan()
    with sidebar:
        with st.form(key='Perara',clear_on_submit=True):
            tab1, tab2 = st.tabs(["T.C./Per.No","Ad Soyad"])
            with tab1:
                arananpersonel = st.text_input (label="Personel Ara",placeholder="T.C. YADA PERSONEL NUMARASI")
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    ad = st.text_input (label="Personel Ara",placeholder="AD")
                with col2:
                    soyad = st.text_input (label="",placeholder="SOYAD")
                
            aramayap = st.form_submit_button(label="Ara")
            if aramayap:
                SapGui().personelara(turkish_upper(arananpersonel))
                bulunanliste = SapGui().bulunanPersonel()
                st.selectbox(label="Bulunan Personeller",options=bulunanliste['Ad Soyad'].astype(str) +
                " | " + bulunanliste['T.C.'].astype(str) + " | " + bulunanliste['Personel Numarası'].astype(str) + " | " 
                +bulunanliste['Alt Alan'].astype(str) + " | " +bulunanliste['PYP'].astype(str) + " | " +
                bulunanliste['Proje'].astype(str) + " | " +bulunanliste['Doğum Tarihi'].astype(str))

