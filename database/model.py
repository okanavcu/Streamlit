from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship,class_mapper
from sqlalchemy import ForeignKey,Text
from typing import List


class Base(DeclarativeBase):
    pass


class Kullanicilar(Base):
    
    __tablename__ =  "Kullanicilar"
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True,unique=True)
    SirketId:Mapped[str] = mapped_column(nullable=False)
    BolgeId:Mapped[str] = mapped_column(nullable=False)
    KullaniciAdi:Mapped[str] = mapped_column(unique=True)
    Mail:Mapped[str] = mapped_column()
    Admin:Mapped[bool] = mapped_column()
    

class Bolgeler(Base):
    
    __tablename__ = "Bolgeler"
    
    id:Mapped[int] = mapped_column(primary_key=True,nullable=False,autoincrement=True)
    bolge:Mapped[str] = mapped_column(nullable=False,unique=True)
    isyerleri: Mapped["Isyerleri"] = relationship("Isyerleri", back_populates="bolge")


class Sirketler(Base):
    
    __tablename__ = "Sirketler"
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True,unique=True)
    SirketKodu:Mapped[int] = mapped_column(unique=True,nullable=False)
    SirketAdi:Mapped[str] = mapped_column(unique=True,nullable=False)
    isyerleri: Mapped["Isyerleri"] = relationship("Isyerleri", back_populates="sirket")


class Projeler(Base):
    
    __tablename__= "Projeler"
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True,unique=True)
    IsyeriId:Mapped[int] = mapped_column(ForeignKey("Isyerleri.id"),nullable=False)
    PYPOgesi:Mapped[str] = mapped_column(unique=True)
    isyerleri: Mapped["Isyerleri"] = relationship("Isyerleri", back_populates="proje")

    def __repr__(self) -> str:
        return f"< SAP Kodu = {self.Isyerleri.SAPKodu}  {self.PYPOgesi}>"


class Isyerleri(Base):
    
    __tablename__ = "Isyerleri"
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    SirketId:Mapped[int] = mapped_column(ForeignKey("Sirketler.id"),nullable=False)
    BolgeId:Mapped[int] = mapped_column(ForeignKey("Bolgeler.id"),nullable=False)
    SAPKodu:Mapped[str] = mapped_column(nullable=False,unique= True)
    IsYeriAdi:Mapped[str] = mapped_column(nullable=False,unique= True)
    KullaniciAdi:Mapped[str] = mapped_column(nullable=True)
    KullaniciKodu:Mapped[str] = mapped_column(nullable=True)
    SistemSifresi:Mapped[str] = mapped_column(nullable=True)
    IsYeriSifresi:Mapped[str] = mapped_column(nullable=True)
    SGKSicilNo:Mapped[str] = mapped_column(nullable=True,unique= True)
    IsYeriAdresi:Mapped[str] = mapped_column(nullable=True)
    AcilişTarihi:Mapped[str] = mapped_column(nullable=True)
    KapanisTarihi:Mapped[str] = mapped_column(nullable=True)
    proje:Mapped["Projeler"] = relationship("Projeler", back_populates="isyerleri")
    bolge:Mapped["Bolgeler"] = relationship("Bolgeler", back_populates="isyerleri")
    sirket:Mapped["Sirketler"] = relationship("Sirketler", back_populates="isyerleri")