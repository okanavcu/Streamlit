from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

import os
from supabase import create_client

url= os.environ.get('SUPABASE_URL')
key= os.environ.get('SUPABASE_KEY')
supabase= create_client(url, key)

class Eylemler:
    @classmethod
    def giris(cls,mail,sifre):
        try:
            session = supabase.auth.sign_in_with_password(
            {'email': mail, 'password': sifre})
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
            {'email': mail,'password': sifre,'options': 
            {'data': {
                'Adı': ad,
                'SoyAdı': soyad,
                'Admin': False,
                'Bölgeleri': [],
                'Şirketleri': [],
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
    def bolgeKod(cls,session):
        bolge = supabase.table('Bolgeler').select('bolge').execute()
        return bolge.data
    @classmethod
    def sirketKod(cls,session):
        sirket = supabase.table('Sirketler').select('sirketKodu').execute()
        return sirket.data
    @classmethod
    def ekle(cls, formdegeri):
        try:
            isyeri_sorgu = supabase.table('IsYerleri').select('*').eq('sgkSicilNo', formdegeri['sgkSicilNo']).execute()
            if len(isyeri_sorgu.data) > 0:
                isyerisicil = isyeri_sorgu.data[0]['sgkSicilNo']
            else:
                isyerisicil = None
            bolge = supabase.table('Bolgeler').select('*').eq('bolge', formdegeri['bolge']).execute()
            if len(bolge.data) > 0:
                bolge_id = bolge.data[0]['id']
            else:
                bolge_id = None
            sirket = supabase.table('Sirketler').select('*').eq('sirketKodu', formdegeri['sirketKod']).execute()
            if len(sirket.data) > 0:
                sirket_id = sirket.data[0]['id']
            else:
                sirket_id = None
            proje = supabase.table('Projeler').select('*').eq('pypOgesi', formdegeri['pypOgesi']).execute()
            if 'data' in proje and len(proje.data) > 0:
                proje_id = proje.data[0]['id']
            else:
                proje_id = None

            tarih_str = formdegeri['acilisTarihi']
            if tarih_str is not None:
                tarih_dt = datetime(tarih_str.year, tarih_str.month, tarih_str.day)
                acilis_tarihi_str = tarih_dt.strftime('%d.%m.%Y')
            else:
                acilis_tarihi_str = ""
            
            tarih_str = formdegeri['kapanisTarihi']
            if tarih_str is not None:
                tarih_dt = datetime(tarih_str.year, tarih_str.month, tarih_str.day)
                kapanis_tarihi_str = tarih_dt.strftime('%d.%m.%Y')
            else:
                kapanis_tarihi_str = "" 
            user2 = {
                'sapKodu': formdegeri['sapKodu'],
                'isYeriAdi': formdegeri['isYeriAdi'],
                'kullaniciAdi': formdegeri['kullaniciAdi'],
                'kullaniciKodu': formdegeri['kullaniciKodu'],
                'sistemSifresi': formdegeri['sistemSifresi'],
                'isYeriSifresi': formdegeri['isYeriSifresi'],
                'sgkSicilNo': formdegeri['sgkSicilNo'],
                'isYeriAdresi': formdegeri['isYeriAdresi'],
                'acilisTarihi': acilis_tarihi_str,
                'kapanisTarihi': kapanis_tarihi_str,
            }

            if bolge_id:
                user2["bolgeId"] = bolge_id
            else:
                yeni_bolge = {'bolge': formdegeri['bolge']}
                bolge_ekle_sonuc = supabase.table('Bolgeler').insert([yeni_bolge]).execute()
                bolge_id = bolge_ekle_sonuc['data'][0]['id']
                user2["bolgeId"] = bolge_id

            if sirket_id:
                user2["sirketId"] = sirket_id
            else:
                yeni_sirket = {'sirketKodu': formdegeri['sirketKodu'], 'sirketAdi': formdegeri['sirketAdi']}
                sirket_ekle_sonuc = supabase.table('Sirketler').insert([yeni_sirket]).execute()
                sirket_id = sirket_ekle_sonuc['data'][0]['id']
                user2["sirketId"] = sirket_id

            if isyerisicil:
                pass
            else:
                isyeri_ekle_sonuc = supabase.table('IsYerleri').insert([user2]).execute()
                yeni_isyeri_id = isyeri_ekle_sonuc.data[0]['id']

            if proje_id is None:
                yeni_proje = {'isYeriId': yeni_isyeri_id, 'pypOgesi': formdegeri['pypOgesi']}
                proje_ekle_sonuc = supabase.table('Projeler').insert([yeni_proje]).execute()
            else:
                pass

            kontrol = 0
        except Exception as e:
            kontrol = 1
            print(e)
        finally:
            return kontrol
    @classmethod
    def guncelle(cls, formdegeri,günSicNo):
        sirket = supabase.table('Sirketler').select('*').eq('sirketKodu', formdegeri['sirketKod']).execute()
        if len(sirket.data) > 0:
            sirket_id = sirket.data[0]['id']
        bolge = supabase.table('Bolgeler').select('*').eq('bolge', formdegeri['bolge']).execute()
        if len(bolge.data) > 0:
            bolge_id = bolge.data[0]['id']
        tarih_str = formdegeri['acilisTarihi']
        if tarih_str is not None:
            tarih_dt = datetime(tarih_str.year, tarih_str.month, tarih_str.day)
            acilis_tarihi_str = tarih_dt.strftime('%d.%m.%Y')
        else:
            acilis_tarihi_str = ""
        
        tarih_str = formdegeri['kapanisTarihi']
        if tarih_str is not None:
            tarih_dt = datetime(tarih_str.year, tarih_str.month, tarih_str.day)
            kapanis_tarihi_str = tarih_dt.strftime('%d.%m.%Y')
        else:
            kapanis_tarihi_str = "" 

        # Eğer formdegeri['acilisTarihi'] bir datetime.date nesnesi olarak geliyorsa:
        acilis_tarihi_str = formdegeri['acilisTarihi'].strftime('%d.%m.%Y')
        supabase.table("IsYerleri").update({
            "sirketId": sirket_id,
            "bolgeId": bolge_id,
            "sapKodu": formdegeri['sapKodu'],
            "isYeriAdi": formdegeri['isYeriAdi'],
            "kullaniciAdi": formdegeri['kullaniciAdi'],
            "kullaniciKodu": formdegeri['kullaniciKodu'],
            "sistemSifresi": formdegeri['sistemSifresi'],
            "isYeriSifresi": formdegeri['isYeriSifresi'],
            "sgkSicilNo": formdegeri['sgkSicilNo'],
            "isYeriAdresi": formdegeri['isYeriAdresi'],
            "acilisTarihi": acilis_tarihi_str,
            "kapanisTarihi": kapanis_tarihi_str
        }).eq("sgkSicilNo", günSicNo).execute()

    @classmethod        
    def sil(cls, formdegeri,günSicNo):
        supabase.table("IsYerleri").delete().eq("sgkSicilNo", günSicNo).execute()