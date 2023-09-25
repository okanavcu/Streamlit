import streamlit as st
import streamlit.components.v1 as stc
from streamlit_option_menu import option_menu
from database.model import Base,Bolgeler,Isyerleri,Kullanicilar,Projeler,Sirketler
from database.eylemler import Eylemler
import getpass
import time,sys
import subprocess
import win32com.client
import hydralit_components as hc

st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

option_data = [
{'icon': "bi bi-hand-thumbs-up", 'label':"Anasayfa"},
{'icon':"fa fa-question-circle",'label':"Katalog"},
{'icon': "bi bi-hand-thumbs-down", 'label':"Sipariş"},
]

font_fmt = {'font-class':'h2','font-size':'100%'}

op = hc.option_bar(option_definition=option_data,key='PrimaryOption',font_styling=font_fmt,horizontal_orientation=True)

def SapAktive():
    try:

        path = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe"
        sap = subprocess.Popen(path)
        time.sleep(10)

        SapGuiAuto = win32com.client.GetObject('SAPGUI')
        if not type(SapGuiAuto) == win32com.client.CDispatch:
            return

        application = SapGuiAuto.GetScriptingEngine
        if not type(application) == win32com.client.CDispatch:
            SapGuiAuto = None
            return
        connection = application.OpenConnection("ERP_LOGON_GRUP", True)

        if not type(connection) == win32com.client.CDispatch:
            application = None
            SapGuiAuto = None
            return

        session = connection.Children(0)
        if not type(session) == win32com.client.CDispatch:
            connection = None
            application = None
            SapGuiAuto = None
            return

        session.findById("wnd[0]/usr/txtRSYST-BNAME").text = "OAVCU"
        session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "23061994Ss*"
        session.findById("wnd[0]").sendVKey(0)
    except:
        print(sys.exc_info())
        return "Giriş Hatası !"
    
def cagır():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    # Google'a git
    driver.get("https://www.google.com.tr")

    # Arama kutusuna "okan" yaz
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("okan")

    # Enter tuşuna bas
    search_box.submit()

    deger = driver.find_element(By.CSS_SELECTOR,'#oFNiHe > div > div > div.eKPi4 > span:nth-child(2) > span.BBwThe').text
    # WebDriver'ı kapat
    driver.quit()
    return deger


if op =='Anasayfa':
    
    st.dataframe(Eylemler.vericek())


if op == "Katalog":
    
    if st.button("Selenium Deneme"):
        deger = cagır()
        st.write(deger)

if op == "Pizza Ekle":
    pass

if op == "Sipariş":
    pass