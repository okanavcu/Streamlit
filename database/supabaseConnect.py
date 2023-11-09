from dotenv import load_dotenv
import pandas as pd
load_dotenv()

import os
from supabase import create_client

url= os.environ.get("SUPABASE_URL")
key= os.environ.get("SUPABASE_KEY")
supabase= create_client(url, key)

class Eylemler:
    @classmethod
    def giris(cls,mail,sifre):
        try:
            session = supabase.auth.sign_in_with_password(
            {"email": mail, "password": sifre})
            return session
        except:
            pass
    @classmethod
    def girisYenile(cls):
        try:
            session = supabase.auth.refresh_session()
            return session
        except:
            pass
    @classmethod
    def cıkıs(cls):
        session = supabase.auth.sign_out()
        return session
    @classmethod
    def kayitOl(cls,mail,sifre,ad,soyad,bolge,sirket):
        try:
            res = supabase.auth.sign_up(
            {"email": mail,"password": sifre,"options": 
            {"data": {
                "Adı": ad,
                "SoyAdı": soyad,
                "Admin": False,
                "Bölgeleri": [],
                "Şirketleri": [],
                }}})
            return res
        except:
            pass
    @classmethod
    def Admin_sorgu(cls,session):
        admin = session.user.user_metadata['Admin']
        return admin
    @classmethod
    def vericek(cls,session):
        params = {'user_sirketleri': session.user.user_metadata['Şirketleri'],
                'user_bolgeleri': session.user.user_metadata['Bölgeleri']}
        request = supabase.rpc('get_isyerleri', params)
        response = request.execute()
        df = pd.DataFrame(response.data)
        return df
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