import time
import streamlit as st
from sap.main import SapGui
import hydralit_components as hc
from streamlit_option_menu import option_menu
import locale
from streamlit_extras.grid import grid
from streamlit_extras.function_explorer import function_explorer


locale.setlocale(locale.LC_ALL, '')

st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

def clear_Resorce():
    st.cache_resource.clear()

def clear_Data():
    st.cache_data.clear()

@st.cache_data
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
                st.cache_data.clear()
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

@st.cache_data
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


@st.cache_resource(experimental_allow_widgets=True)
def perislem():
    personelislemleri = st.form(key="pa30islemform")
    personelislemleriEkran = st.container()
    with personelislemleri:
        if selected != "SAP Giriş":
            with open(r'sap\islemler.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            options_dict = {}
            for line in lines:
                key, value = line.strip().split(':')
                options_dict[key.strip(" '")] = str(value.strip(" ,\n"))

            selected_value = st.selectbox(label="Bilgi Tipi Metni", options=list(options_dict.keys()), on_change=clear_Resorce(), index=None)
            
            # Sütunları oluştur
            detay, kopyala, düzenle, sil = st.columns(4)

            @st.cache_resource
            def index():
                for row in st.session_state["data_editor"]["edited_rows"]:
                    if st.session_state["data_editor"]["edited_rows"][row]["Seç"] == True:
                        return row   

            with detay: 
                if detay.form_submit_button(label="Detay", use_container_width=True,on_click=clear_Data):
                    df = tablogetir(options_dict[selected_value])
                    df.insert(0, "Seç", 0)
                    with personelislemleri:
                        a = st.data_editor(df, column_config={"Seç": st.column_config.CheckboxColumn(label="Seç", default=False)},
                        hide_index=True,use_container_width=True,key="data_editor")
                        
            
            with sil:
                if sil.form_submit_button(label="Sil", use_container_width=True,):
                    SapGui().islemTabloSecim(options_dict[selected_value],index())
                    SapGui().pa30_sil()


            def post_data(data):
                with personelislemleriEkran:
                    personelIslemlerEkran = st.form(key="KaydetForm")

                    with personelIslemlerEkran:
                        kol1, kol2, kol3, kol4 = st.columns(4)

                        # Form içindeki tüm widget'ları bir sözlükte tut
                        widgets = {}

                        for i in range(len(data["Başlık"])):
                            baslik = data["Başlık"][i]
                            id_degeri = data["Id"][i]
                            value = data["Value"][i]
                            if i != 0:
                                if i % 4 == 0:
                                    # Her bir widget'a eşsiz bir key ver
                                    widgets[f"widget_{i}"] = kol1.text_input(baslik, value=value, key=f"widget_{i}")
                                if i % 4 == 1:
                                    widgets[f"widget_{i}"] = kol2.text_input(baslik, value=value, key=f"widget_{i}")
                                elif i % 4 == 2:
                                    widgets[f"widget_{i}"] = kol3.text_input(baslik, value=value, key=f"widget_{i}")
                                elif i % 4 == 3:
                                    widgets[f"widget_{i}"] = kol4.text_input(baslik, value=value, key=f"widget_{i}")
                            else:
                                widgets[f"widget_{i}"] = kol1.text_input(baslik, value=value, key=f"widget_{i}")

                    # Form submit edildiğinde çalışacak fonksiyonu tanımla
                    def on_form_submit():
                        # Form içindeki tüm widget'ların değerlerini ve id'lerini al
                        values = {}
                        for i in range(len(data["Başlık"])):
                            id_degeri = data["Id"][i]
                            values[id_degeri] = widgets[f"widget_{i}"]
                        # st.write(values)
                        SapGui().kaydet(**values)

                    # Form submit button'a callback fonksiyonunu ver
                    kol4.form_submit_button(label="İşle", use_container_width=True,type="primary", on_click=on_form_submit)

            with kopyala:
                if kopyala.form_submit_button(label="Kopyala", use_container_width=True):
                    SapGui().islemTabloSecim(options_dict[selected_value],index())
                    SapGui().pa30_Kopyala()
                    df = SapGui().ekranBilgileri()
                    post_data(df)
            
            with düzenle:
                if düzenle.form_submit_button(label="Değiştir", use_container_width=True):
                    SapGui().islemTabloSecim(options_dict[selected_value],index())
                    SapGui().pa30_Düzenle()
                    df = SapGui().ekranBilgileri()
                    post_data(df)

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
            SapGui().pa30()
            def bulunansecim():
                secilen_deger = st.session_state.secilen_deger
                aranacaksicil = secilen_deger.split(" | ")[2]
                SapGui().personelara(aranacaksicil)
                st.cache_data.clear()               
                
            SapGui().personelara(turkish_upper(arananpersonel))
            bulunanliste = SapGui().bulunanPersonel()

            if bulunanliste.empty:
                st.write("Hiçbir sonuç bulunamadı.")
                st.cache_data.clear()
                st.rerun()
            else:
                secilen_deger = st.selectbox(label="Bulunan Personeller",
                options=bulunanliste['Ad Soyad'].astype(str) +
                " | " + bulunanliste['T.C.'].astype(str) + " | " + bulunanliste['Personel Numarası'].astype(str) + " | "
                + bulunanliste['Alt Alan'].astype(str) + " | " + bulunanliste['PYP'].astype(str) + " | " +
                bulunanliste['Proje'].astype(str) + " | " + bulunanliste['Doğum Tarihi'].astype(str),
                key='secilen_deger', index=None,on_change=bulunansecim)

def perislem40():
    personelislemleri40 = st.container()
    with personelislemleri40:
        my_grid = grid(1,[1,1],1, vertical_align="top")
        my_grid.caption("Personel İşlemler Dizisi")
        tarih = my_grid.date_input(label="Geçerlilik Tarihi", format="DD.MM.YYYY")
        secenekler = ["İşe alma", "Organizasyonel değişiklik", "İşten ayrılma",
            "Şirkette yeniden işe giriş", "Başvuru İşe alma", "Org. değişiklik (toplu)"]
        secilen_secenek = my_grid.selectbox(label="İşlemler", options=secenekler)
        indeks = secenekler.index(secilen_secenek)
        SapGui().islemTabloSecimPa40(satir=indeks,tarih=tarih)
        
        #
        if secilen_secenek:
            ckcfrm = st.form(key='ckcfrm',clear_on_submit=True)
            with ckcfrm:
                if secilen_secenek== "İşten ayrılma":
                    with open(r'sap\çıkışnedenleri.txt', 'r', encoding='utf-8') as file:
                            lines = file.readlines()
                    options_dict = {}
                    for line in lines:
                        key, value = line.strip().split(':')
                        options_dict[key] = str(value.strip(" ,\n"))
                    options = [(f"{key} - {value}") for key, value in options_dict.items()]
                    ayrılısneden = st.selectbox(label="Ayrılış Nedeni", options=options)
                    if ayrılısneden is not None:
                        selected_option = ayrılısneden.split(' - ')
                        nedenkod = str(selected_option[0]).zfill(2)
                    isle = st.form_submit_button(label="İşle", use_container_width=True)
                    if isle:
                        SapGui().istenayrılma(nedenkod)



if selected == "PA40":
    pa40sayfa()
    perbilpan()
    perislem40()

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
            SapGui().pa30()
            def bulunansecim():
                secilen_deger = st.session_state.secilen_deger
                aranacaksicil = secilen_deger.split(" | ")[2]
                SapGui().personelara(aranacaksicil)
                st.cache_data.clear()               
                
            SapGui().personelara(turkish_upper(arananpersonel))
            bulunanliste = SapGui().bulunanPersonel()

            if bulunanliste.empty:
                st.write("Hiçbir sonuç bulunamadı.")
                st.cache_data.clear()
                st.rerun()
            else:
                secilen_deger = st.selectbox(label="Bulunan Personeller",
                options=bulunanliste['Ad Soyad'].astype(str) +
                " | " + bulunanliste['T.C.'].astype(str) + " | " + bulunanliste['Personel Numarası'].astype(str) + " | "
                + bulunanliste['Alt Alan'].astype(str) + " | " + bulunanliste['PYP'].astype(str) + " | " +
                bulunanliste['Proje'].astype(str) + " | " + bulunanliste['Doğum Tarihi'].astype(str),
                key='secilen_deger', index=None,on_change=bulunansecim)
