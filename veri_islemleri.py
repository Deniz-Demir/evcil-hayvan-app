import sqlite3

# Veritabanı dosyamızın adı
DOSYA = "evcil_hayvanlar.db"

# ====================================================================
# 1. MASAYI HAZIRLA (Tablo Güncellendi)
# ====================================================================

def veritabani_kur():
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()

    # Hayvanlar tablosuna BOY, MAMA_SAATI ve MAMA_MIKTARI eklendi
    yazici.execute("""
        CREATE TABLE IF NOT EXISTS hayvanlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT,
            yas INTEGER,
            kilo REAL,
            boy REAL,              -- Yeni eklendi
            cinsiyet TEXT,
            mama_markasi TEXT,
            mama_turu TEXT,        -- Yeni eklendi
            mama_miktari TEXT,     -- Yeni eklendi
            mama_saati TEXT,       -- Yeni eklendi
            alerjiler TEXT,
            sevilen_urunler TEXT,
            veteriner_gecmisi TEXT,
            asi_takvimi TEXT,
            durum_notu TEXT
        )
    """)

    # Safiye'nin istediği Veterinerler Tablosu
    yazici.execute("""
        CREATE TABLE IF NOT EXISTS veterinerler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vet_ad TEXT,
            uzmanlik TEXT,
            telefon TEXT
        )
    """)

    # İlk kurulumda Safiye'nin istediği doktorları otomatik ekle
    yazici.execute("SELECT COUNT(*) FROM veterinerler")
    if yazici.fetchone()[0] == 0:
        yazici.execute("INSERT INTO veterinerler (vet_ad, uzmanlik) VALUES (?, ?)", ("Ali Hekim Bey", "Genel Cerrahi"))
        yazici.execute("INSERT INTO veterinerler (vet_ad, uzmanlik) VALUES (?, ?)", ("Veli Bey", "Aşı Uzmanı"))

    baglanti.commit()
    baglanti.close()

# ====================================================================
# 2. YENİ HAYVAN EKLE (Parametreler Güncellendi)
# ====================================================================

def hayvan_ekle(ad, yas, kilo, boy, cinsiyet, mama_marka, mama_tur, miktar, saat, alerji, urun, vet, asi, durum):
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()

    komut = """INSERT INTO hayvanlar 
               (ad, yas, kilo, boy, cinsiyet, mama_markasi, mama_turu, mama_miktari, mama_saati, alerjiler, sevilen_urunler, veteriner_gecmisi, asi_takvimi, durum_notu) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    
    bilgiler = (ad, yas, kilo, boy, cinsiyet, mama_marka, mama_tur, miktar, saat, alerji, urun, vet, asi, durum)

    yazici.execute(komut, bilgiler)
    baglanti.commit()
    baglanti.close()
    return f"{ad} başarıyla kaydedildi!"

# ====================================================================
# 3. VERİ ÇEKME (Nevada'nın Arayüzü İçin)
# ====================================================================

def hayvanlari_goster():
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()
    # Arayüzde listelemek için önemli bilgileri çekiyoruz
    yazici.execute("SELECT id, ad, yas, kilo, mama_turu FROM hayvanlar")
    liste = yazici.fetchall()
    baglanti.close()
    return liste

def hayvan_detay_getir(hayvan_id):
    """Seçilen hayvanın tüm özelliklerini Safiye'nin mantık motoruna gönderir."""
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()
    yazici.execute("SELECT * FROM hayvanlar WHERE id = ?", (hayvan_id,))
    detay = yazici.fetchone()
    baglanti.close()
    return detay

def veterinerleri_listele():
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()
    yazici.execute("SELECT * FROM veterinerler")
    vets = yazici.fetchall()
    baglanti.close()
    return vets
