import sqlite3
import datetime

# Veritabanı dosyamızın adı
DOSYA = "evcil_hayvanlar.db"

# ====================================================================
# 1. MASAYI HAZIRLA (Tabloları Oluşturma)
# ====================================================================

def veritabani_kur():
    # Dosyaya bağlan (Yoksa otomatik oluşturur)
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()

    # Hayvanların bilgilerini tutacak tabloyu oluştur
    yazici.execute("""
        CREATE TABLE IF NOT EXISTS hayvanlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT,
            yas INTEGER,
            kilo REAL,
            cinsiyet TEXT,
            mama_markasi TEXT,
            alerjiler TEXT,
            sevilen_urunler TEXT,
            veteriner_gecmisi TEXT,
            gunluk_rutin TEXT,
            asi_takvimi TEXT,
            durum_notu TEXT,
            acil_durum_notu TEXT
        )
    """)

    # Paylaşılan önerileri tutacak tabloyu oluştur
    yazici.execute("""
        CREATE TABLE IF NOT EXISTS paylasimlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici TEXT,
            urun TEXT,
            tarih TEXT
        )
    """)

    baglanti.commit() # Yapılanları kaydet
    baglanti.close()  # Bağlantıyı bitir

# ====================================================================
# 2. YENİ HAYVAN EKLE
# ====================================================================

def hayvan_ekle(ad, yas, kilo, cinsiyet, mama, alerji, urun, veteriner, rutin, asi, durum, acil):
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()

    # Soru işaretleri (?) güvenlik içindir, bilgileri sırayla yerleştirir
    komut = "INSERT INTO hayvanlar (ad, yas, kilo, cinsiyet, mama_markasi, alerjiler, sevilen_urunler, veteriner_gecmisi, gunluk_rutin, asi_takvimi, durum_notu, acil_durum_notu) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    bilgiler = (ad, yas, kilo, cinsiyet, mama, alerji, urun, veteriner, rutin, asi, durum, acil)

    yazici.execute(komut, bilgiler)

    baglanti.commit()
    baglanti.close()
    return "Hayvan başarıyla kaydedildi!"

# ====================================================================
# 3. KAYITLARI LİSTELE
# ====================================================================

def hayvanlari_goster():
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()

    # Sadece isim ve yaş gibi temel bilgileri çek
    yazici.execute("SELECT id, ad, yas FROM hayvanlar")
    liste = yazici.fetchall() # Tüm satırları bir liste olarak getir

    baglanti.close()
    return liste

# ====================================================================
# 4. KAYIT SİL
# ====================================================================

def hayvan_sil(numara):
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()
    
    # Gelen numarayı sayıya çevirerek işimizi garantiye alıyoruz
    yazici.execute("DELETE FROM hayvanlar WHERE id = ?", (int(numara),))

    baglanti.commit()
    baglanti.close()
    return "Kayıt silindi."
