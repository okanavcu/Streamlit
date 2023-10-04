from .model import Base, Kullanicilar,Isyerleri,Bolgeler,Sirketler,Projeler
import getpass
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func

engine = create_engine("sqlite:///C:/Users/okan.avcu/Desktop/PROGRAMLAR/PYTHON/Streamlit/database/ohm_ozluk_veri_tabani.db")

class Eylemler:

    @classmethod
    def tablo_olustur(cls):
        Base.metadata.create_all(bind=engine)

    @classmethod
    def Kullanici_sorgu(cls):
        try:
            session = Session(bind=engine)
            kullanici_adi = getpass.getuser()

            query = session.query(Kullanicilar).filter(Kullanicilar.KullaniciAdi == kullanici_adi)

            # Sorguyu çalıştırma ve sonuçları alıp kullanma
            results = query.first()
            if results:
                pass
            return results
        except Exception as e:
            return "Bağlantı Yok"
        finally :
            session.close()

    @classmethod
    def Admin_sorgu(cls):
        try:
            session = Session(bind=engine)
            kullanici_adi = getpass.getuser()
            query = session.query(Kullanicilar).filter(Kullanicilar.KullaniciAdi == kullanici_adi, Kullanicilar.Admin == True)
            # Sorguyu çalıştırma ve sonuçları alıp kullanma
            result = query.first()
            if result:
                return result
            else:
                return None
        except Exception as e:
            return "Bağlantı Yok"
        finally:
            session.close()

    @classmethod
    def vericek(cls):
        try:
            session = Session(bind=engine)
            bölge_listesi = cls.Kullanici_sorgu().BolgeId
            if type(bölge_listesi) == str:
                bolgeliste = [int(x) for x in bölge_listesi.split(",")]
            else:
                bolgeliste = [0,bölge_listesi]
            sirket_listesi = cls.Kullanici_sorgu().SirketId
            if type(sirket_listesi) == str:
                sirketliste = [int(x) for x in sirket_listesi.split(",")]
            else:
                sirketliste = [0,sirket_listesi]
            results = (
                session.query(
                    Sirketler.SirketKodu.label('ŞİRKET KOD'),
                    Sirketler.SirketAdi.label('ŞİRKET ADI'),
                    Bolgeler.bolge.label('BÖLGE'),
                    Isyerleri.SAPKodu.label('SAP KODU'),
                    Isyerleri.IsYeriAdi.label('İŞ YERİ ADI'),
                    Isyerleri.KullaniciAdi.label('KULLANICI ADI'),
                    Isyerleri.KullaniciKodu.label('KULLANICI KODU'),
                    Isyerleri.SistemSifresi.label('SİSTEM ŞİFRESİ'),
                    Isyerleri.IsYeriSifresi.label('İŞ YERİ ŞİFRESİ'),
                    Isyerleri.SGKSicilNo.label('SGK SİCİL NO'),
                    Isyerleri.IsYeriAdresi.label('İŞYERİ ADRESİ'),
                    Isyerleri.AcilişTarihi.label('AÇILIŞ TARİHİ'),
                    Isyerleri.KapanisTarihi.label('KAPANIŞ TARİHİ'),
                    Projeler.PYPOgesi.label('PYP ÖĞESİ')
                )
                .join(Isyerleri.bolge)
                .join(Sirketler, Isyerleri.SirketId == Sirketler.id)
                .join(Isyerleri.proje)
                .filter(Isyerleri.BolgeId.in_(bolgeliste),Isyerleri.SirketId.in_(sirketliste))
                .group_by(
                    Sirketler.SirketKodu,
                    Sirketler.SirketAdi,
                    Bolgeler.bolge,
                    Isyerleri.SAPKodu,
                    Isyerleri.IsYeriAdi,
                    Isyerleri.KullaniciAdi,
                    Isyerleri.KullaniciKodu,
                    Isyerleri.SistemSifresi,
                    Isyerleri.IsYeriSifresi,
                    Isyerleri.SGKSicilNo,
                    Isyerleri.IsYeriAdresi,
                    Isyerleri.AcilişTarihi,
                    Isyerleri.KapanisTarihi,
                    Projeler.PYPOgesi
                )
                .all()
            )
            rapordosya = pd.DataFrame(results)
            return rapordosya
        except Exception as e:
            return "Kullanıcı Kayıtlı Değil !"
        finally :
            session.close()
            
    @classmethod
    def ekle(cls,formdegeri):
        try:
            session = Session(bind=engine)
            Isyeri = session.query(Isyerleri).filter(Isyerleri.SGKSicilNo == formdegeri['SGKSicilNo']).first()
            Isyerisicil = Isyeri.SGKSicilNo if Isyeri else None
            bolge = session.query(Bolgeler).filter(Bolgeler.bolge == formdegeri["Bolge"]).first()
            BolgeId = bolge.id if bolge else None
            sirket = session.query(Sirketler).filter(Sirketler.SirketKodu == formdegeri["SirketKodu"]).first()
            SirketId = sirket.id if sirket else None
            proje = session.query(Projeler).filter(Projeler.PYPOgesi == formdegeri["PYPOgesi"]).first()
            Proje = proje.id if proje else None

            user2 = Isyerleri(
                                SAPKodu=formdegeri["SAPKodu"],
                                IsYeriAdi=formdegeri["IsYeriAdi"],
                                KullaniciAdi=formdegeri["KullaniciAdi"],
                                KullaniciKodu=formdegeri["KullaniciKodu"],
                                SistemSifresi=formdegeri["SistemSifresi"],
                                IsYeriSifresi=formdegeri["IsYeriSifresi"],
                                SGKSicilNo=formdegeri["SGKSicilNo"],
                                IsYeriAdresi=formdegeri["IsYeriAdresi"],
                                AcilişTarihi=formdegeri["AcilişTarihi"],
                                KapanisTarihi=formdegeri["KapanisTarihi"]
            )
            
            if BolgeId:
                user2.BolgeId = BolgeId
            else:
                user2.bolge = Bolgeler(bolge=formdegeri["bolge"])
                
            if SirketId:
                user2.SirketId = SirketId
            else:
                user2.sirket = Sirketler(SirketAdi=formdegeri["SirketAdi"],SirketKodu = formdegeri["SirketKodu"])
            
            if Proje is None:
                user2.proje= Projeler(PYPOgesi = formdegeri["PYPOgesi"])
            else:
                user2.proje = proje

            if Isyerisicil:
                cls.guncelle(formdegeri)
            else:
                session.add_all([user2])
                
            session.commit()
            kontrol =  0
                
        except Exception as e:
            kontrol = 1
            e.print_exc()
            
        finally :
            session.close()
            return kontrol
        
    @classmethod
    def guncelle(cls, formdegeri):
        try:
            session = Session(bind=engine)

            # Güncellenecek kaydı sorgula
            isyeri = session.query(Isyerleri).filter(Isyerleri.SAPKodu == formdegeri["SAPKodu"]).first()
            
            if isyeri is None:
                isyeri = session.query(Isyerleri).filter(Isyerleri.SGKSicilNo == formdegeri["SGKSicilNo"]).first()

            if isyeri:
                # Mevcut veriyi güncelle
                isyeri.IsYeriAdi = formdegeri["IsYeriAdi"]
                isyeri.KullaniciAdi = formdegeri["KullaniciAdi"]
                isyeri.KullaniciKodu = formdegeri["KullaniciKodu"]
                isyeri.SistemSifresi = formdegeri["SistemSifresi"]
                isyeri.IsYeriSifresi = formdegeri["IsYeriSifresi"]
                isyeri.SGKSicilNo = formdegeri["SGKSicilNo"]
                isyeri.IsYeriAdresi = formdegeri["IsYeriAdresi"]
                isyeri.AcilişTarihi = formdegeri["AcilişTarihi"]
                isyeri.KapanisTarihi = formdegeri["KapanisTarihi"]

                # Bolge güncellemesi
                bolge = session.query(Bolgeler).filter(Bolgeler.bolge == formdegeri["bolge"]).first()
                if bolge:
                    isyeri.BolgeId = bolge.id
                else:
                    new_bolge = Bolgeler(bolge=formdegeri["bolge"])
                    session.add(new_bolge)
                    session.flush()
                    isyeri.BolgeId = new_bolge.id

                # Sirket güncellemesi
                sirket = session.query(Sirketler).filter(Sirketler.SirketKodu == formdegeri["SirketKodu"]).first()
                if sirket:
                    isyeri.SirketId = sirket.id
                else:
                    new_sirket = Sirketler(SirketAdi=formdegeri["SirketAdi"], SirketKodu=formdegeri["SirketKodu"])
                    session.add(new_sirket)
                    session.flush()
                    isyeri.SirketId = new_sirket.id

                # Proje güncellemesi
                proje = session.query(Projeler).filter(Projeler.PYPOgesi == formdegeri["PYPOgesi"]).first()
                if proje:
                    isyeri.ProjeId = proje.id
                else:
                    new_proje = Projeler(IsyeriId = isyeri.id ,PYPOgesi=formdegeri["PYPOgesi"])
                    session.add(new_proje)
                    session.flush()
                    isyeri.ProjeId = new_proje.id
                    
                kontrol =  0
                session.commit()
                
                
            else:
                print("Güncellenecek kayıt bulunamadı.")
        except Exception as e:
            kontrol = 1
        finally:
            session.close()
            return kontrol
            
    @classmethod        
    def sil(cls, formdegeri):
        try:
            #bağlantı kur
            session = Session(bind=engine)
            # Silinecek kaydı sorgula
            isyeri = session.query(Isyerleri).filter(Isyerleri.SGKSicilNo == formdegeri["SGKSicilNo"]).first()
            if isyeri:
                projeler_to_delete = session.query(Projeler).filter(Projeler.IsyeriId == isyeri.id).all()
                session.query(Projeler).filter(Projeler.PYPOgesi == formdegeri["PYPOgesi"]).delete(synchronize_session=False)
                session.commit()
                if len(projeler_to_delete) == 1:
                # isyeri kaydını sil
                    session.delete(isyeri)
                    session.commit()
        except Exception as e:
            print(e)
        finally:
            session.close()