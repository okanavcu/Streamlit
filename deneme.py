import streamlit as st
from streamlit_extras.switch_page_button import switch_page

x = st.slider("x", 0, 10)

if x == 1:
    switch_page("AnaSayfa.py")