import sys
import time
import streamlit as st
import hydralit_components as hc
from database.eylemler import Eylemler, mail
from st_aggrid import AgGrid,GridUpdateMode,ColumnsAutoSizeMode,DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from datetime import datetime
from webotomasion.main import SeleniumSgk
import win32com.client as win32

st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

@st.cache_data
def tablom():
   data = Eylemler.vericek()
   return data

def sifrebilgisi():
   bulunan = tablo_data[tablo_data['PYP ÖĞESİ'].str.contains(pyp_ogesi)]
   return bulunan

def sgkTescil():
   sifre_subset = sifrebilgisi()
   if len(sifre_subset) == 1:
         sifre = sifre_subset[["KULLANICI ADI", "KULLANICI KODU", "SİSTEM ŞİFRESİ", "İŞ YERİ ŞİFRESİ"]]
         selenium_instance = SeleniumSgk()
         selenium_instance.sgkTescil(sifre.iloc[0,0],sifre.iloc[0,1],sifre.iloc[0,2],sifre.iloc[0,3])

def sgkSistem():
   sifre_subset = sifrebilgisi()
   if len(sifre_subset) == 1:
         sifre = sifre_subset[["KULLANICI ADI", "KULLANICI KODU", "SİSTEM ŞİFRESİ", "İŞ YERİ ŞİFRESİ"]]
         selenium_instance = SeleniumSgk()
         selenium_instance.sgkSistem(sifre.iloc[0,0],sifre.iloc[0,1],sifre.iloc[0,2],sifre.iloc[0,3])

def isKazasi():
   sifre_subset = sifrebilgisi()
   if len(sifre_subset) == 1:
         sifre = sifre_subset[["KULLANICI ADI", "KULLANICI KODU", "SİSTEM ŞİFRESİ", "İŞ YERİ ŞİFRESİ"]]
         selenium_instance = SeleniumSgk()
         selenium_instance.isKazasi(sifre.iloc[0,0],sifre.iloc[0,1],sifre.iloc[0,2],sifre.iloc[0,3])

def vizite():
   sifre_subset = sifrebilgisi()
   if len(sifre_subset) == 1:
         sifre = sifre_subset[["KULLANICI ADI", "KULLANICI KODU", "SİSTEM ŞİFRESİ", "İŞ YERİ ŞİFRESİ"]]
         selenium_instance = SeleniumSgk()
         selenium_instance.vizite(sifre.iloc[0,0],sifre.iloc[0,1],sifre.iloc[0,2],sifre.iloc[0,3])

def eBildirge():
   sifre_subset = sifrebilgisi()
   if len(sifre_subset) == 1:
         sifre = sifre_subset[["KULLANICI ADI", "KULLANICI KODU", "SİSTEM ŞİFRESİ", "İŞ YERİ ŞİFRESİ"]]
         selenium_instance = SeleniumSgk()
         selenium_instance.eBildirge(sifre.iloc[0,0],sifre.iloc[0,1],sifre.iloc[0,2],sifre.iloc[0,3])

def eBildirgeV2():
   sifre_subset = sifrebilgisi()
   if len(sifre_subset) == 1:
         sifre = sifre_subset[["KULLANICI ADI", "KULLANICI KODU", "SİSTEM ŞİFRESİ", "İŞ YERİ ŞİFRESİ"]]
         selenium_instance = SeleniumSgk()
         selenium_instance.eBildirgeV2(sifre.iloc[0,0],sifre.iloc[0,1],sifre.iloc[0,2],sifre.iloc[0,3])

def topluGris():
   sifre_subset = sifrebilgisi()
   if len(sifre_subset) == 1:
         sifre = sifre_subset[["KULLANICI ADI", "KULLANICI KODU", "SİSTEM ŞİFRESİ", "İŞ YERİ ŞİFRESİ"]]
         selenium_instance = SeleniumSgk()
         selenium_instance.topluGiris(sifre.iloc[0,0],sifre.iloc[0,1],sifre.iloc[0,2],sifre.iloc[0,3]) 

tablo_data = tablom()
if type(tablo_data) != str:

   option_data = [
      {'label':"SGK Sistem"},
      {'label':"Şifre Paneli"},
   ]

   font_fmt = {'font-class':'h1','font-size':'100%'}

   op = hc.option_bar(option_definition=option_data,key='PrimaryOption',font_styling=font_fmt,horizontal_orientation=True)
   if op == "Şifre Paneli":
      gb = GridOptionsBuilder.from_dataframe(tablom())
      gb.configure_pagination(enabled=True)
      gb.configure_default_column(editable=True,groupable=True)
      gb.configure_selection(selection_mode="multiple")

      # makes columns resizable, sortable and filterable by default
      gb.configure_default_column(
         resizable=True,
         filterable=True,
         sortable=True,
         editable=True,
         groupable=True,
         sorteable=True,
      )

      gb.configure_column(
         field="ŞİRKET ADI",
         hide=True,
         header_name="ŞİRKET ADI",
         width=150,  # set width as per your requirement
         rowGroup=True,  # enables row grouping for this column
         filterable=True,
      )

      gb.configure_column(
         field="BÖLGE",
         header_name="BÖLGE",
         hide=True,
         rowGroup=True,  # enables row grouping for this column
         filterable=True,
      )

      gb.configure_column(
         field="SAP KODU",
         header_name="SAP KODU",
         pinned="left",
         width=150,  # set width as per your requirement
         rowGroup=True,
         filterable=True,
      )

      gb.configure_grid_options(
         groupDefaultExpanded=1,  # Gruplar başlangıçta kapalı olacak
         suppressColumnVirtualisation=True,
         reload_data=True,
         groupDisplayType="groupRows",
         autoGroupColumnDef=dict(
            minWidth=150,
            pinned="left",
            cellRendererParams=dict(suppressCount=True),
         ),
      )

      gridOptions = gb.build()


      tablo = AgGrid(
         tablom(),
         editable=True,
         gridOptions=gridOptions,
         height=500,
         theme="alpine",
         data_return_mode=DataReturnMode.AS_INPUT,
         update_on='MODEL_CHANGED',
         update_mode=GridUpdateMode.SELECTION_CHANGED,
         columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
         allow_unsafe_jscode=True,
         enable_quicksearch=True,)


      secilisatir = tablo["selected_rows"]

      
      if Eylemler.Admin_sorgu():
         with st.sidebar:
            with st.form("Ekle",clear_on_submit=True):
               st.header("İş Yeri Bilgileri")
               SirketId = st.selectbox("ŞİRKET KOD", options=tablo_data["ŞİRKET KOD"].unique().tolist()if not secilisatir else tablo_data["ŞİRKET KOD"].unique().tolist(),label_visibility="visible",placeholder="Şirket Kod",
                                       index=tablo_data["ŞİRKET KOD"].unique().tolist().index(secilisatir[0]["ŞİRKET KOD"]) if secilisatir else None)
               BolgeId = st.selectbox("BÖLGE",options=tablo_data["BÖLGE"].unique().tolist() if not secilisatir else tablo_data["BÖLGE"].unique().tolist(),label_visibility="visible",placeholder="Bölge",
                                       index=tablo_data["BÖLGE"].unique().tolist().index(secilisatir[0]["BÖLGE"]) if secilisatir else None)
               SAPKodu = st.text_input("SAP Kodu",placeholder="SAP Kodu",value=secilisatir[0].get("SAP KODU") if secilisatir else None)
               IsYeriAdi = st.text_input("İŞ YERİ ADI",placeholder="İş Yeri Adı",value=secilisatir[0].get('İŞ YERİ ADI') if secilisatir else None)
               KullaniciAdi = st.text_input("KULLANICI ADI",placeholder="Kullanıcı Adı",value=secilisatir[0].get("KULLANICI ADI") if secilisatir else None)
               KullaniciKodu = st.text_input("KULLANICI KODU",placeholder="Kullanıcı Kodu",value=secilisatir[0].get("KULLANICI KODU") if secilisatir else None)
               SistemSifresi = st.text_input("SİSTEM ŞİFRESİ",placeholder="Sistem Şifresi",value=secilisatir[0].get("SİSTEM ŞİFRESİ") if secilisatir else None)
               IsYeriSifresi = st.text_input("İŞ YERİ ŞİFRESİ",placeholder="İş Yeri Şifresi",value=secilisatir[0].get("İŞ YERİ ŞİFRESİ") if secilisatir else None) 
               SGKSicilNo = st.text_input("SGK SİCİL NO",placeholder="SGK Sicil No",value=secilisatir[0].get("SGK SİCİL NO") if secilisatir else None)
               IsYeriAdresi = st.text_input("İŞYERİ ADRESİ",placeholder="İş Yeri Adresi",value=secilisatir[0].get("İŞYERİ ADRESİ") if secilisatir else None)
               PYPOgesi = st.text_input("PYP ÖĞESİ",placeholder="PYP Öğesi",value=secilisatir[0].get("PYP ÖĞESİ") if secilisatir else None)
               try:
                  AcilisTarihi = st.date_input("Açılış Tarihi",format="DD/MM/YYYY",value=datetime.strptime(secilisatir[0].get("AÇILIŞ TARİHİ"), "%d.%m.%Y") if secilisatir else None)
               except:
                  AcilisTarihi = st.date_input("Açılış Tarihi",format="DD/MM/YYYY",value=None)
               try:
                  KapanisTarihi = st.date_input("Kapanış Tarihi",format="DD/MM/YYYY",value=datetime.strptime(secilisatir[0].get("KAPANIŞ TARİHİ"), "%d.%m.%Y") if secilisatir else None)
               except:
                  KapanisTarihi = st.date_input("Kapanış Tarihi",format="DD/MM/YYYY",value=None)
               # Kullanıcı formu gönderdiğinde
               col1,col2,col3 = st.columns(3)
               with col1:
                  Ekle = st.form_submit_button("Ekle",use_container_width=True)
                  if Ekle:
                     form_data = {  "SirketKodu": SirketId,
                                    "bolge": BolgeId,
                                    "SAPKodu": SAPKodu,
                                    "IsYeriAdi": IsYeriAdi,
                                    "KullaniciAdi": KullaniciAdi,
                                    "KullaniciKodu": KullaniciKodu,
                                    "SistemSifresi": SistemSifresi,
                                    "IsYeriSifresi": IsYeriSifresi,
                                    "SGKSicilNo": SGKSicilNo,
                                    "IsYeriAdresi": IsYeriAdresi,
                                    "PYPOgesi": PYPOgesi,
                                    "AcilişTarihi": AcilisTarihi.strftime("%d.%m.%Y")if AcilisTarihi else None,
                                    "KapanisTarihi": KapanisTarihi.strftime("%d.%m.%Y")if KapanisTarihi else None,
                                 }
                     Eylemler.ekle(form_data)
                     st.cache_data.clear()
                     st.toast(body=(f"{PYPOgesi} {SAPKodu} {IsYeriAdi} Eklendi."))
                     time.sleep(3)
                     st.rerun()
               with col2:
                  guncelle = st.form_submit_button("Güncelle",use_container_width=True)
                  if guncelle:
                     form_data = {  "SirketKodu": SirketId,
                                    "bolge": BolgeId,
                                    "SAPKodu": SAPKodu,
                                    "IsYeriAdi": IsYeriAdi,
                                    "KullaniciAdi": KullaniciAdi,
                                    "KullaniciKodu": KullaniciKodu,
                                    "SistemSifresi": SistemSifresi,
                                    "IsYeriSifresi": IsYeriSifresi,
                                    "SGKSicilNo": SGKSicilNo,
                                    "IsYeriAdresi": IsYeriAdresi,
                                    "PYPOgesi": PYPOgesi,
                                    "AcilişTarihi": AcilisTarihi.strftime("%d.%m.%Y")if AcilisTarihi else None,
                                    "KapanisTarihi": KapanisTarihi.strftime("%d.%m.%Y")if KapanisTarihi else None,
                                 }
                     Eylemler.guncelle(form_data)
                     st.cache_data.clear()
                     st.toast(body=(f"{PYPOgesi} {SAPKodu} {IsYeriAdi} GÜNCELLENDİ."))
                     time.sleep(3)
                     st.rerun()
               
               with col3:
                  Sil = st.form_submit_button("Sil",use_container_width=True)
                  if Sil:
                     form_data = {  "SirketKodu": SirketId,
                                    "bolge": BolgeId,
                                    "SAPKodu": SAPKodu,
                                    "IsYeriAdi": IsYeriAdi,
                                    "KullaniciAdi": KullaniciAdi,
                                    "KullaniciKodu": KullaniciKodu,
                                    "SistemSifresi": SistemSifresi,
                                    "IsYeriSifresi": IsYeriSifresi,
                                    "SGKSicilNo": SGKSicilNo,
                                    "IsYeriAdresi": IsYeriAdresi,
                                    "PYPOgesi": PYPOgesi,
                                    "AcilişTarihi": AcilisTarihi.strftime("%d.%m.%Y")if AcilisTarihi else None,
                                    "KapanisTarihi": KapanisTarihi.strftime("%d.%m.%Y")if KapanisTarihi else None,
                                 }
                     Eylemler.sil(form_data)
                     st.cache_data.clear()
                     st.toast(body=(f"{PYPOgesi} {SAPKodu} {IsYeriAdi} SİLİNDİ."))
                     time.sleep(3)
                     st.rerun()

   if op == "SGK Sistem":
      with st.form("SGKSistem"):
               st.header("İş Yeri Bilgileri")
               tablo_data = tablom()
               isyeriara = st.selectbox("İş Yeri Ara", options=tablo_data['SAP KODU'].astype(str) + " - " + tablo_data['İŞ YERİ ADI'].astype(str) + " - " + tablo_data['PYP ÖĞESİ'].astype(str),)
               pyp_ogesi = isyeriara.split('-')[-1].strip()  # Son sütunun değerini al
               col1,col2 = st.columns(2)
               with col1:
                  sigortalıtescil = st.form_submit_button("Sigortalı Tescil",type="secondary",use_container_width=True,on_click=sgkTescil)
                  vizite = st.form_submit_button("Vizite",type="secondary",use_container_width=True,on_click=vizite)
                  ebildirge = st.form_submit_button("E-Bildirge",type="secondary",use_container_width=True,on_click=eBildirge)
                  toplugiris = st.form_submit_button("Toplu Giriş-Çıkış",type="secondary",use_container_width=True,on_click=topluGris)
               with col2:
                  sgksistem = st.form_submit_button("SGK Sistem",type="secondary",use_container_width=True,on_click=sgkSistem)
                  iskazasi = st.form_submit_button("İş Kazası",type="secondary",use_container_width=True,on_click=isKazasi)
                  ebildirgev2 = st.form_submit_button("E-Bildirge V2",type="secondary",use_container_width=True,on_click=eBildirgeV2)
else:
   with st.form(key="Kayit", clear_on_submit=True):
      st.title(body="KAYIT İÇİN MAİL AT")
      kullanici_adi = st.text_input("PC Kullanıcı Adınız", placeholder="Kullanıcı Adı")
      secilen_sirketler = st.multiselect(label="Şirket seçiniz", placeholder="Şirket seçiniz", options=Eylemler.sirketliste(), key="sirketliste")
      secilen_bolge = st.multiselect(label="Bölge seçiniz", placeholder="Bölge seçiniz", options=Eylemler.bolgeliste(), key="bolgeliste")
      submitted = st.form_submit_button(label="Mail Gönder", use_container_width=True)

      # Eğer form gönderildiyse
      if submitted:
         # Değerleri mail fonksiyonuna geçir
         mail(kullanici_adi, secilen_sirketler, secilen_bolge)
         st.cache_data.clear()
         st.rerun()

