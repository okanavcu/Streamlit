import sqlite3
import pandas as pd

class VeriTabani:
    def __init__(self):
        self.dizin = r"database\ohm_ozluk_veri_tabani.db"
        self.baglanti = None
        self.cursor = None
        self.seciliBolge = None
    def baglantiyi_ac(self):
        self.baglanti = sqlite3.connect(self.dizin)
        self.cursor = self.baglanti.cursor()
    def baglantiyi_kapat(self):
        if self.baglanti:
            self.baglanti.close() 
    def kullaniciSorgu(self, kullaniciAdi):
        try:
            self.baglanti = sqlite3.connect(self.dizin)
            self.cursor = self.baglanti.cursor()
            self.kullanicisorgu = f"""
            SELECT COUNT(*) AS count FROM Kullanicilar WHERE KullaniciAdi = '{kullaniciAdi}';"""
            self.cursor.execute(self.kullanicisorgu)
            bolge = self.cursor.fetchone()
            self.baglantiKapat()
            return bolge[0]
        except:
            return 5
    def baglantiKapat(self):
        if self.baglanti:
            self.baglanti.close()
    def veri(self, kullaniciAdi):
        try:
            self.baglanti = sqlite3.connect(self.dizin)
            self.cursor = self.baglanti.cursor()
            # print (kullaniciAdi)
            self.sorgu = f"""
            SELECT Kullanicilar.BolgeId FROM Kullanicilar WHERE Kullanicilar.KullaniciAdi = '{kullaniciAdi}' """
            self.cursor.execute(self.sorgu)
            self.veri_tup = self.cursor.fetchall()
            return self.veri_tup
        except:
            print("Sorgu çalıştırma hatası!")
        finally:
            self.baglantiKapat()
    def veriCek(self, kullaniciAdi):
        
        try:
            self.baglanti = sqlite3.connect(self.dizin)
            self.cursor = self.baglanti.cursor()
            gelenveri = self.veri(kullaniciAdi)[0][0]
            bolge = str(gelenveri).split(',')
            if gelenveri is not None:
                self.baglanti = sqlite3.connect(self.dizin)
                self.cursor = self.baglanti.cursor()
                self.sorgu = f"""SELECT 
                s.SirketKodu AS 'ŞİRKET KOD', 
                s.SirketAdi AS 'ŞİRKET ADI', 
                b.Bolge AS 'BÖLGE', 
                i.SAPKodu AS 'SAP KODU',
                i.IsYeriAdi AS 'İŞ YERİ ADI',
                i.KullaniciAdi AS 'KULLANICI ADI',
                i.KullaniciKodu AS 'KULLANICI KODU',
                i.SistemSifresi AS 'SİSTEM ŞİFRESİ',
                i.IsYeriSifresi AS 'İŞ YERİ ŞİFRESİ',
                i.SGKSicilNo AS 'SGK SİCİL NO',
                i.IsYeriAdresi AS 'İŞYERİ ADRESİ',
                i.AcilişTarihi AS 'AÇILIŞ TARİHİ',
                i.KapanisTarihi AS 'KAPANIŞ TARİHİ',
                p.PYPOgesi AS 'PYP ÖĞESİ'
                FROM Isyerleri i
                INNER JOIN Bolgeler b ON i.BolgeId = b.Id 
                INNER JOIN Sirketler s ON i.SirketId = s.id
                INNER JOIN Projeler p ON i.id = p.IsyeriId
                WHERE b.id IN ({','.join(['?' for _ in bolge])})
                GROUP BY s.SirketKodu, s.SirketAdi, b.Bolge, i.SAPKodu, i.IsYeriAdi,
                i.KullaniciAdi, i.KullaniciKodu, i.SistemSifresi, i.IsYeriSifresi;"""

                

                # print(self.sorgu)
                self.rapordosya = pd.read_sql_query(self.sorgu, self.baglanti, params=bolge)
                return self.rapordosya
            else:
                print("Veri alınamadı: Kullanıcı adı bulunamadı.")
                raise ValueError("Sorgu hatası!")
        except Exception as e:
            print("Sorgu hatası:", e)
        finally:
            self.baglantiKapat()
    def EkleBolge(self, bolge):
            try:
                self.baglantiyi_ac()
                self.seciliBolge = bolge
                self.sorgu = f"""INSERT INTO Bolgeler('Bolge') VALUES ('{self.seciliBolge}')"""
                print(self.sorgu)
                self.cursor.execute(self.sorgu)
                self.baglanti.commit()
            except Exception as e:
                print("Sorgu hatası:", e)
            finally:
                self.baglantiyi_kapat()
    def EkleSirket(self,kod,ad):
        
        try:
            self.baglantiyi_ac()
            self.seciliSirketKod = kod
            self.seciliSirkeAd = ad
            self.sorgu = f"""INSERT INTO Sirketler(SirketKodu,SirketAdi) VALUES ('{kod}','{ad}')"""
            print(self.sorgu)
            self.cursor.execute(self.sorgu)
            self.baglanti.commit()
        except Exception as e:
            print("Sorgu hatası:", e)
        finally:
            self.baglantiyi_kapat()
    def EkleIsyeri(self,sirketid,bolgeid,sap,isyeriadi,kllncadi,kllnckodu,sissifresi,isyersifresi,sicil,adres,atar,ktar):
        self.cmbSirketId = sirketid
        self.cmbBolgeId = bolgeid
        self.cmbSAPKodu = sap
        self.entSirketAd = isyeriadi
        self.entKullaniciAdi = kllncadi
        self.entKullanıcıKodu = kllnckodu
        self.entSisSifresi = sissifresi
        self.entIsYerSifresi = isyersifresi
        self.entSicilNo = sicil
        self.entAdres = adres
        self.entAcTar = atar
        self.entKapTar = ktar

        
        try:
            
            VeriTabani.baglantiyi_ac(self)
            self.sorgu = f"""SELECT Id FROM Sirketler WHERE SirketKodu = {self.cmbSirketId}"""
            self.cursor.execute(self.sorgu)
            SirketId = self.cursor.fetchone()[0]
            self.sorgu = f"""SELECT Id FROM Bolgeler WHERE Bolge = '{self.cmbBolgeId}'"""
            self.cursor.execute(self.sorgu)
            BolgeId = self.cursor.fetchone()[0]
            
            self.sorgu = f"""   INSERT INTO Isyerleri ("SirketId","BolgeId","SAPKodu",
                                "IsYeriAdi","KullaniciAdi","KullaniciKodu","SistemSifresi",
                                "IsYeriSifresi","SGKSicilNo","IsYeriAdresi","AcilişTarihi","KapanisTarihi")
                                VALUES ({SirketId},{BolgeId},'{self.cmbSAPKodu}','{self.entSirketAd}','{self.entKullaniciAdi}','{self.entKullanıcıKodu}',
                                '{self.entSisSifresi}','{self.entIsYerSifresi}','{self.entSicilNo}','{self.entAdres}',
                                '{self.entAcTar}','{self.entKapTar}') """
            print(self.sorgu)
            self.cursor.execute(self.sorgu)
            self.baglanti.commit()
        except Exception as e:
            print("Sorgu hatası:", e)
        finally:
            VeriTabani.baglantiKapat(self)
    def EkleProje(self,sapkod,pyp):
        
        self.cmbPYPNo = pyp
        self.cmbSAPKodu = sapkod
        
        try:
            
            VeriTabani.baglantiyi_ac(self)
            self.sorgu = f"""SELECT Id FROM Isyerleri WHERE SAPKodu = '{sapkod}'"""
            self.cursor.execute(self.sorgu)
            IsyeriId = self.cursor.fetchone()[0]
            
            self.sorgu = f"""   INSERT INTO Projeler ("IsyeriId","PYPOgesi")
                                VALUES ({IsyeriId},'{pyp}') """
            print(self.sorgu)
            self.cursor.execute(self.sorgu)
            self.baglanti.commit()
        except Exception as e:
            print("Sorgu hatası:", e)
        finally:
            VeriTabani.baglantiKapat(self)

    def GuncelleBolge(self, ilkbolge,ikincibolge):
        try:
            self.baglantiyi_ac()
            self.sorgu = f"""UPDATE "Bolgeler" SET "SirketKodu","SirketAdi"= '{ilkbolge}' WHERE "Bolge" = '{ikincibolge}'"""
            print(self.sorgu)
            self.cursor.execute(self.sorgu)
            self.baglanti.commit()
        except Exception as e:
            print("Sorgu hatası:", e)
        finally:
            self.baglantiyi_kapat()

    def GuncelleSirket(self,kod,ad,id):
        
        try:
            self.baglantiyi_ac()
            self.sorgu = f"""SELECT Id FROM Sirketler WHERE SirketKodu = {id}"""
            self.cursor.execute(self.sorgu)
            SirketId = self.cursor.fetchone()[0]
            self.sorgu = f"""UPDATE "Sirketler" SET "SirketKodu" = {kod}, "SirketAdi" = '{ad}' WHERE "id" = {SirketId}"""
            print(self.sorgu)
            self.cursor.execute(self.sorgu)
            self.baglanti.commit()
        except Exception as e:
            print("Sorgu hatası:", e)
        finally:
            self.baglantiyi_kapat()

    def GuncelleIsyeri(self,sirketid,bolgeid,sap,isyeriadi,kllncadi,kllnckodu,sissifresi,isyersifresi,sicil,adres,atar,ktar):
            self.cmbSirketId = sirketid
            self.cmbBolgeId = bolgeid
            self.cmbSAPKodu = sap
            self.entIsyeriAd = isyeriadi
            self.entKullaniciAdi = kllncadi
            self.entKullanıcıKodu = kllnckodu
            self.entSisSifresi = sissifresi
            self.entIsYerSifresi = isyersifresi
            self.entSicilNo = sicil
            self.entAdres = adres
            self.entAcTar = atar
            self.entKapTar = ktar

            
            try:
                
                VeriTabani.baglantiyi_ac(self)
                self.sorgu = f"""SELECT id FROM Isyerleri WHERE  SAPKodu = {self.cmbSirketId}"""
                self.cursor.execute(self.sorgu)
                id = self.cursor.fetchone()[0]
                
                self.sorgu = f"""SELECT id FROM Sirketler WHERE SirketKodu = {self.cmbSirketId}"""
                self.cursor.execute(self.sorgu)
                SrktId = self.cursor.fetchone()[0]
                self.sorgu = f"""SELECT id FROM Bolgeler WHERE Bolge = '{self.cmbBolgeId}'"""
                self.cursor.execute(self.sorgu)
                BlgId = self.cursor.fetchone()[0]
                
                self.sorgu = f""" UPDATE "Isyerleri" SET  "SirketId" = {SrktId},"BolgeId" = {BlgId},"SAPKodu" = '{self.cmbSAPKodu}',
                                    "IsYeriAdi" = '{self.entIsyeriAd}',"KullaniciAdi" = '{self.entKullaniciAdi}',"KullaniciKodu" = '{self.entKullanıcıKodu}',"SistemSifresi" = '{self.entSisSifresi}',
                                    "IsYeriSifresi" = '{self.entSisSifresi}',"SGKSicilNo" = '{self.entSicilNo}',"IsYeriAdresi" = '{self.entAdres}',"AcilişTarihi" = '{self.entAcTar}',"KapanisTarihi" = '{self.entKapTar}' WHERE id = {id}"""
                print(self.sorgu)
                self.cursor.execute(self.sorgu)
                self.baglanti.commit()
            except Exception as e:
                print("Sorgu hatası:", e)
            finally:
                VeriTabani.baglantiKapat(self)
                            
if __name__ == "__main__":
    a = VeriTabani()
    a.veriCek("okan.avcu")

