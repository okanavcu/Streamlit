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

    def personelara(self):    
        self.session.findById("wnd[0]").maximize
        self.session.findById("wnd[0]/usr/ctxtRP50G-PERNR").text = "=...17792564146"
        self.session.findById("wnd[0]").sendVKey (0)
        try:
            assert self.session.ActiveWindow.Text.startswith("Personel numarası")
        except:
            pass
        
    def SapLogin(self,kullaniciadi,sifre): 
        try:
            
            try:
                self.SapGuiAuto = win32com.client.GetObject("SAPGUI")
                if not type(self.SapGuiAuto) == win32com.client.CDispatch:
                    return
            except:
                path = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe"
                subprocess.Popen(path)
                time.sleep(10)
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
                    return "Giriş Yapıldı."
                except:
                    return "Giriş Yapıldı."

        except:
            print(sys.exc_info()[0])
            return "Giriş Hatası !"


    def pa40(self):
        self.session.findById("wnd[0]/tbar[0]/okcd").text = "pa40"
        self.session.findById("wnd[0]").sendVKey (0)
        self.session.findById("wnd[0]/usr/ctxtRP50G-PERNR").text = "60067859"
        self.session.findById("wnd[0]/usr/ctxtRP50G-PERNR").caretPosition = (8)
        self.session.findById("wnd[0]").sendVKey (0)
        msg1 = self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG01_200A47_DAT_P0001_ENAME").text
        self.session.findById("wnd[0]").sendVKey (2)
        msg2=self.session.findById("wnd[0]/usr/subSUBSCR_HEADER:/1PAPAXX/HDR_20047A:0100/txt$_DG16_200A47_DAT_P0770_MERNI").text
        self.session.findById("wnd[0]").sendVKey (2)
        mesajlar = [msg1,msg2]
        return mesajlar
    
if __name__ == "__main__":
    a = SapGui()
    a.personelara()