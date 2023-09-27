import requests
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