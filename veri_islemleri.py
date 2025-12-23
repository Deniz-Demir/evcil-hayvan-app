import sqlite3

# Veritabanı dosyamızın adı
DOSYA = "evcil_hayvanlar.db"

# ====================================================================
# 1. MASAYI HAZIRLA (Kullanıcı Ayrımı ve Veteriner Düzenlemesi Eklendi)
# ====================================================================

def veritabani_kur():
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()

    # 1. MADDE İÇİN: sahip_id eklendi (Kullanıcılar sadece kendi hayvanını görsün diye)
    yazici.execute("""
        CREATE TABLE IF NOT EXISTS hayvanlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sahip_id TEXT,                 -- Hayvanın hangi kullanıcıya ait olduğunu tutar
            ad TEXT,
            yas INTEGER,
            kilo REAL,
            boy REAL,
            cinsiyet TEXT,
            mama_markasi TEXT,
            mama_turu TEXT,                -- Kuru/Yaş bilgisi burada tutuluyor
            mama_miktari TEXT,
            mama_saati TEXT,
            alerjiler TEXT,
            sevilen_urunler TEXT,
            veteriner_gecmisi TEXT,
            asi_takvimi TEXT,
            durum_notu TEXT
        )
    """)

    # Veterinerler Tablosu
    yazici.execute("""
        CREATE TABLE IF NOT EXISTS veterinerler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vet_ad TEXT,
            uzmanlik TEXT,
            telefon TEXT
        )
    """)

    # 4. MADDE İÇİN: Ali Hekim Bey'in unvanı ve numarası düzenlendi
    yazici.execute("SELECT COUNT(*) FROM veterinerler")
    if yazici.fetchone()[0] == 0:
        yazici.execute("""
            INSERT INTO veterinerler (vet_ad, uzmanlik, telefon) 
            VALUES (?, ?, ?)""", 
            ("Ali Hekim Bey", "Uzman Veteriner", "05xx xxx xx xx")
        )
        yazici.execute("""
            INSERT INTO veterinerler (vet_ad, uzmanlik, telefon) 
            VALUES (?, ?, ?)""", 
            ("Veli Bey", "Uzman Veteriner", "05xx xxx xx xx")
        )

    baglanti.commit()
    baglanti.close()

# ====================================================================
# 2. YENİ HAYVAN EKLE (sahip_id Parametresi Eklendi)
# ====================================================================

# Fonksiyona sahip_id eklendi, böylece kayıt yapan kişiyle eşleşir
def hayvan_ekle(sahip_id, ad, yas, kilo, boy, cinsiyet, mama_marka, mama_tur, miktar, saat, alerji, urun, vet, asi, durum):
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()

    komut = """INSERT INTO hayvanlar 
               (sahip_id, ad, yas, kilo, boy, cinsiyet, mama_markasi, mama_turu, mama_miktari, mama_saati, alerjiler, sevilen_urunler, veteriner_gecmisi, asi_takvimi, durum_notu) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    
    bilgiler = (sahip_id, ad, yas, kilo, boy, cinsiyet, mama_marka, mama_tur, miktar, saat, alerji, urun, vet, asi, durum)

    yazici.execute(komut, bilgiler)
    baglanti.commit()
    
    # Son eklenen hayvanın ID'sini geri döndürüyoruz (Analiz ekranına geçiş için)
    son_id = yazici.lastrowid
    baglanti.close()
    return son_id

# ====================================================================
# 3. VERİ ÇEKME (Kullanıcıya Özel Filtreleme)
# ====================================================================

# 1. MADDE İÇİN: Sadece giriş yapan kullanıcının ID'sine göre liste getirir
def hayvanlari_goster(sahip_id):
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()
    
    # Filtreleme: WHERE sahip_id = ?
    yazici.execute("SELECT id, ad, yas, kilo, mama_turu FROM hayvanlar WHERE sahip_id = ?", (sahip_id,))
    liste = yazici.fetchall()
    
    baglanti.close()
    return liste

def hayvan_detay_getir(hayvan_id):
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
