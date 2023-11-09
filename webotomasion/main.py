import time
import pytesseract
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import shutil
import os

class SeleniumSgk:
    
    def drivers(self):
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--incognito")
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])   
        path = os.path.dirname(os.path.abspath(__file__))
        try:
            self.driver = webdriver.Chrome(service=Service(path + "/chromedriver.exe"), options=self.options)
        except:
            driver_path = ChromeDriverManager().install()
            self.driver = webdriver.Chrome(service=Service(driver_path), options=self.options)
            target_path = os.path.join(path, "chromedriver.exe")
            shutil.move(driver_path, target_path)
        return self.driver
    
    def ocr(self):
        pytesseract.pytesseract.tesseract_cmd = r"webotomasion\Tesseract-OCR\tesseract.exe"
        resim = cv2.imread(r"captcha.png")
        metin = pytesseract.image_to_string(resim)
        return metin
    
    def sgkTescil(self,kullaniciAdi,kullaniciKodu,sistemSifresi,isyeriSifresi):
        driver = self.drivers()
        driver.get("https://uyg.sgk.gov.tr/SigortaliTescil/amp/loginldap")
        driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td > img").screenshot(r"captcha.png")
        driver.find_element(By.NAME, "j_username").send_keys(kullaniciAdi)
        driver.find_element(By.NAME, "isyeri_kod").send_keys(kullaniciKodu)
        driver.find_element(By.NAME, "j_password").send_keys(sistemSifresi)
        driver.find_element(By.NAME, "isyeri_sifre").send_keys(isyeriSifresi)
        driver.find_element(By.ID, "isyeri_guvenlik").send_keys(self.ocr())
    
    def sgkSistem(self,kullaniciAdi, kullaniciKodu, sistemSifresi, isyeriSifresi):
        driver = self.drivers()
        driver.get("https://uyg.sgk.gov.tr/IsverenSistemi")
        driver.find_element(By.XPATH, "//*[@id='guvenlik_kod']").screenshot(r"captcha.png")
        driver.find_element(By.ID, "kullaniciIlkKontrollerGiris_username").send_keys(kullaniciAdi)
        driver.find_element(By.ID, "kullaniciIlkKontrollerGiris_isyeri_kod").send_keys(kullaniciKodu)
        driver.find_element(By.ID, "kullaniciIlkKontrollerGiris_password").send_keys(sistemSifresi)
        driver.find_element(By.ID, "kullaniciIlkKontrollerGiris_isyeri_sifre").send_keys(isyeriSifresi)
        driver.find_element(By.ID, "kullaniciIlkKontrollerGiris_isyeri_guvenlik").send_keys(self.ocr())

    def isKazasi(self,kullaniciAdi, kullaniciKodu, sistemSifresi, isyeriSifresi):
        driver = self.drivers()
        driver.get("https://uyg.sgk.gov.tr/IsvBildirimFormu/kullanici_login.do")
        driver.find_element(By.XPATH, "//tr[5]/td[3]/img").screenshot(r"captcha.png")
        driver.find_element(By.NAME, "kullaniciAdi").send_keys(kullaniciAdi)
        driver.find_element(By.NAME, "isyeriKodu").send_keys(kullaniciKodu)
        driver.find_element(By.NAME, "isyeriSifresi").send_keys(isyeriSifresi)
        driver.find_element(By.NAME, "guvenlikKodu").send_keys(self.ocr())
    
    def vizite(self,kullaniciAdi, kullaniciKodu, sistemSifresi, isyeriSifresi):
        driver = self.drivers()
        driver.get("https://uyg.sgk.gov.tr/vizite/welcome.do")
        driver.find_element(By.CSS_SELECTOR, "img:nth-child(2)").screenshot(r"captcha.png")
        driver.find_element(By.NAME, "kullaniciAdi").send_keys(kullaniciAdi)
        driver.find_element(By.NAME, "isyeriKodu").send_keys(kullaniciKodu)
        driver.find_element(By.NAME, "isyeriSifresi").send_keys(isyeriSifresi)
        driver.find_element(By.NAME, "guvenlikKodu").send_keys(self.ocr())
        
    def eBildirgeV2(self,kullaniciAdi, kullaniciKodu, sistemSifresi, isyeriSifresi):
        driver = self.drivers()
        driver.get("https://ebildirge.sgk.gov.tr/EBildirgeV2")
        driver.find_element(By.ID, "guvenlik_kod").screenshot(r"captcha.png")
        driver.find_element(By.ID, "kullaniciIlkKontrollerGiris_username").send_keys(kullaniciAdi)
        driver.find_element(By.ID, "kullaniciIlkKontrollerGiris_isyeri_kod").send_keys(kullaniciKodu)
        driver.find_element(By.ID, "kullaniciIlkKontrollerGiris_password").send_keys(sistemSifresi)
        driver.find_element(By.ID, "kullaniciIlkKontrollerGiris_isyeri_sifre").send_keys(isyeriSifresi)
        driver.find_element(By.ID, "kullaniciIlkKontrollerGiris_isyeri_guvenlik").send_keys(self.ocr())
        
    def topluGiris(self,kullaniciAdi, kullaniciKodu, sistemSifresi, isyeriSifresi):
        driver = self.drivers()
        driver.get("https://uyg.sgk.gov.tr/SgkTescil4a/index.jsf")
        driver.find_element(By.CSS_SELECTOR, "img:nth-child(2)").screenshot(r"captcha.png")
        driver.find_element(By.ID, "loginForm:j_id_f").send_keys(kullaniciAdi)
        driver.find_element(By.ID, "loginForm:j_id_h").send_keys(kullaniciKodu)
        driver.find_element(By.ID, "loginForm:j_id_l").send_keys(sistemSifresi)
        driver.find_element(By.ID, "loginForm:j_id_p").send_keys(isyeriSifresi)
        driver.find_element(By.ID, "loginForm:j_id_t").send_keys(self.ocr())
    
    def eBildirge(self,kullaniciAdi, kullaniciKodu, sistemSifresi, isyeriSifresi):
        driver = self.drivers()
        driver.get("https://ebildirge.sgk.gov.tr/WPEB/amp/loginldap")
        driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td:nth-child(2) > img").screenshot(r"captcha.png")
        driver.find_element(By.NAME, "j_username").send_keys(kullaniciAdi)
        driver.find_element(By.NAME, "isyeri_kod").send_keys(kullaniciKodu)
        driver.find_element(By.NAME, "j_password").send_keys(sistemSifresi)
        driver.find_element(By.NAME, "isyeri_sifre").send_keys(isyeriSifresi)
        driver.find_element(By.ID, "isyeri_guvenlik").send_keys(self.ocr())  