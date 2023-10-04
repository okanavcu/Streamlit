import os
import pandas as pd
import win32com.client
import sys
import subprocess
import time
import pythoncom

class SapGui():

    def __init__(self):
        try:
            # COM altyapısını başlat
            pythoncom.CoInitialize()

            self.SapGuiAuto = win32com.client.GetObject("SAPGUI")
            if not type(self.SapGuiAuto) == win32com.client.CDispatch:
                return

            self.application = self.SapGuiAuto.GetScriptingEngine
            if not type(self.application) == win32com.client.CDispatch:
                self.SapGuiAuto = None
                return

            self.application.HistoryEnabled = True

            self.connection = self.application.Children(0)
            if not type(self.connection) == win32com.client.CDispatch:
                self.application = None
                self.SapGuiAuto = None
                return

            if self.connection.DisabledByServer == True:
                self.connection = None
                self.application = None
                self.SapGuiAuto = None
                return

            self.session = self.connection.Children(0)
            if not type(self.session) == win32com.client.CDispatch:
                self.connection = None
                self.application = None
                self.SapGuiAuto = None
                return

            if self.session.Busy == True:
                self.session = None
                self.connection = None
                self.application = None
                self.SapGuiAuto = None
                return

            if self.session.Info.IsLowSpeedConnection == True:
                self.session = None
                self.connection = None
                self.application = None
                self.SapGuiAuto = None
                return
        except:
            print(sys.exc_info()[0])


    def __del__(self):
        # COM altyapısını serbest bırak
        pythoncom.CoUninitialize()

    def personelara(self,ara):    
        self.session.findById("wnd[0]").maximize
        self.session.findById("wnd[0]/usr/ctxtRP50G-PERNR").text = ara
        self.session.findById("wnd[0]").sendVKey (0)

    def personelarapa40(self,ara):    
        self.session.findById("wnd[0]").maximize
        self.session.findById("wnd[0]").sendVKey(4)
        self.session.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB005/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = "avcu"
        self.session.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB005/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[1,24]").text = "okan"
        self.session.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB005/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[2,24]").text = "17792564146"
        self.session.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB005/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[2,24]").setFocus
        self.session.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB005/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[2,24]").caretPosition = 11
        self.session.findById("wnd[1]").sendVKey (0)
        self.session.findById("wnd[0]").sendVKey (0)
        
    def SapLogin(self,kullaniciadi,sifre):

        if kullaniciadi == "" or sifre == "":
            return
        try:
            
            try:
                self.SapGuiAuto = win32com.client.GetObject("SAPGUI")
                if not type(self.SapGuiAuto) == win32com.client.CDispatch:
                    return
            except:
                path = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe"
                subprocess.Popen(path)
                time.sleep(5)
                self.SapGuiAuto = win32com.client.GetObject("SAPGUI")
                if not type(self.SapGuiAuto) == win32com.client.CDispatch:
                    return

            try:
                assert self.application
            except:
                self.application = self.SapGuiAuto.GetScriptingEngine
                if not type(self.application) == win32com.client.CDispatch:
                    self.SapGuiAuto = None
                    return
            try:
                assert self.session.ActiveWindow.SystemFocus
            except:        
                try:
                    assert self.connection
                except:
                    self.connection = self.application.OpenConnection("ERP_LOGON_GRUP", True)
                    if not type(self.connection) == win32com.client.CDispatch:
                        self.application = None
                        self.SapGuiAuto = None
                        return

                try:
                    assert self.session
                except:
                    self.session = self.connection.Children(0)
                    if not type(self.session) == win32com.client.CDispatch:
                        self.connection = None
                        self.application = None
                        self.SapGuiAuto = None
                        return
                try:
                    self.session.findById("wnd[0]/usr/txtRSYST-BNAME").text = kullaniciadi
                    self.session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = sifre
                    self.session.findById("wnd[0]").sendVKey(0)
                    sapmsg=self.session.findById("wnd[0]/sbar").text
                    return sapmsg
                except:
                    pass
        except:
            print(sys.exc_info()[0])
            return "Giriş Hatası !"
        
    def sapKapat(self):
        os.system("taskkill /f /im saplogon.exe")

    def acıkmı(self):
            try:
                self.SapGuiAuto = win32com.client.GetObject("SAPGUI")
                if not type(self.SapGuiAuto) == win32com.client.CDispatch:
                    return
                Durum = {"Durum":"Açık.","Mesaj":"SAP Uygulaması Açık."}
                return Durum 
            except:
                Durum ={"Durum":"Kapalı.","Mesaj":"SAP Uygulaması Kapalı."}
                return Durum
    
    def baglımı(self):
            try:
                self.connection = self.application.Children(0)
                if not type(self.connection) == win32com.client.CDispatch:
                    self.application = None
                    self.SapGuiAuto = None
                    return
                Durum = {"Durum":"Bağlı.","Mesaj":"Kullanıcı Girişi Yapıldı."}
                return Durum 
            except:
                Durum ={"Durum":"Bağlı Değil.","Mesaj":"Kullanıcı Girişi Yapılmadı."}
                return Durum 
    
    def girisyapıldımı(self):
            if self.session.ActiveWindow.text == "SAP":
                if self.session.ActiveWindow.text == "Bilgi":
                    self.session.findById("wnd[1]").sendVKey (0)
                    return 1
                else:
                    sapmsg=self.session.findById("wnd[0]/sbar").text
                    return sapmsg
            else:
                return 1

    def pa40(self):
        if self.session.ActiveWindow.text != "Personel işlemleri dizisi":
            self.session.findById("wnd[0]/tbar[0]/okcd").text = "pa40"
            self.session.findById("wnd[0]").sendVKey(0)
        return self.session.ActiveWindow.text
    
    def pa30(self):
        if self.session.ActiveWindow.text != "Personel ana verilerinin bkm.yap":
            self.session.findById("wnd[0]/tbar[0]/okcd").text = "pa30"
            self.session.findById("wnd[0]").sendVKey(0)
        return self.session.ActiveWindow.text
    
    def yeniPencere(self):
        self.session.createSession()
        self.session.findById("wnd[0]").maximize
        self.session.findById("wnd[0]").close()
        time.sleep(1)

    def bulunanPersonel(self):
        personeller ={"Personel Numarası":[],"Ad Soyad":[],"T.C.":[],"Doğum Tarihi":[],"Alt Alan":[],"PYP":[],"Proje":[]}
        
        try:
            toplambulunan = int(self.session.findById("wnd[1]").text.split()[2])

            a = 1
            i = 3
            for _ in range(toplambulunan):
                personeller["Personel Numarası"].append(self.session.findById(f"wnd[1]/usr/lbl[1,{i}]").text)
                personeller["Ad Soyad"].append(self.session.findById(f"wnd[1]/usr/lbl[10,{i}]").text)
                personeller["T.C."].append(self.session.findById(f"wnd[1]/usr/lbl[51,{i}]").text)
                personeller["Doğum Tarihi"].append(self.session.findById(f"wnd[1]/usr/lbl[80,{i}]").text)
                personeller["Alt Alan"].append(self.session.findById(f"wnd[1]/usr/lbl[91,{i}]").text)
                personeller["PYP"].append(self.session.findById(f"wnd[1]/usr/lbl[116,{i}]").text)
                personeller["Proje"].append(self.session.findById(f"wnd[1]/usr/lbl[100,{i}]").text)
                
                if i % 34 == 0:
                    self.session.findById("wnd[1]/usr").verticalScrollbar.position = (i-2)*a
                    a = a+1
                    i = 2
                i += 1
            self.session.findById("wnd[1]").close()   
        except:
            pass
        personeller_df = pd.DataFrame(personeller)
        return personeller_df

    def personelBilgi(self):
        try:
            pyp=""
            self.session.findById("wnd[0]").maximize
            ad = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG01_200A47_DAT_P0001_ENAME").text
            istihdam = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG03_200A47_DTX_P0000_STAT2").text
            kanun = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG08_200A47_DTX_P0001_PERSG").text
            sirket = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG10_200A47_DTX_P0001_WERKS").text
            projead = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG12_200A47_DTX_P0001_BTRTL").text
            projekod = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG11_200A47_DAT_P0001_BTRTL").text
            tc = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG16_200A47_DAT_P0770_MERNI").text
            gectar = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG15_200A47_DAT_P0000_BEGDA").text
            yaka = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG14_200A47_DTX_P0001_PERSK").text
            pn = self.session.findById("wnd[0]/usr/ctxtRP50G-PERNR").text
            try:
                pyp = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG04_200A47_DAT_P0001_ZZPYP").text
            except:
                pass
            liste = {"İsim Soyisim" : ad,
                "Personel No":pn,
                "istihdam":istihdam,
                "Kanun":kanun,
                "Şireket":sirket,
                "Proje Adı":projead,
                "Proje Kodu":projekod,
                "T.C.":tc,
                "Geçerlilik Tarihi":gectar,
                "Yaka":yaka,
                "PYP":pyp}
        except:
            liste = {"İsim Soyisim" : "",
                "Personel No":"",
                "istihdam":'Durum',
                "Kanun":"Kanun",
                "Şireket":"Şirket",
                "Proje Adı":"Proje Adı",
                "Proje Kodu":"SAP Kodu",
                "T.C.":"",
                "Geçerlilik Tarihi":"Geçerlilik Tarihi",
                "Yaka":"Yaka Durumu",
                "PYP":"PYP Öğesi"}
            
        return liste

    def detaygetir(self,tipno):
        try:
            self.session.findById("wnd[0]/usr/tabsMENU_TABSTRIP/tabpTAB01/ssubSUBSCR_MENU:SAPMP50A:0400/subSUBSCR_ITKEYS:SAPMP50A:0350/ctxtRP50G-CHOIC").text = tipno
        except:
            self.yeniPencere()
            self.pa30()
            self.session.findById("wnd[0]/usr/tabsMENU_TABSTRIP/tabpTAB01/ssubSUBSCR_MENU:SAPMP50A:0400/subSUBSCR_ITKEYS:SAPMP50A:0350/ctxtRP50G-CHOIC").text = tipno
        self.session.findById("wnd[0]/tbar[1]/btn[20]").press()

        col_count = self.session.findById(f"wnd[0]/usr/tblMP{tipno}00TC3000").Columns.Count
        columns = [self.session.findById(f"wnd[0]/usr/tblMP{tipno}00TC3000").Columns.ElementAt(i).Title for i in range(col_count)]
        df = pd.DataFrame(columns=columns)
        row_count = int(self.session.findById("wnd[0]/usr/txtRP50M-PAGEC").text)

        for i in range(col_count):  # Toplam 10 sütun olduğunu varsayıyorum, isteğe bağlı olarak değiştirin
            column_data = [self.session.findById(f"wnd[0]/usr/tblMP{tipno}00TC3000").GetCell(j, i).text for j in range(row_count)]
            df[columns[i]] = column_data
        return df


if __name__ == "__main__":
    a = SapGui()
    a.detaygetir("0000")