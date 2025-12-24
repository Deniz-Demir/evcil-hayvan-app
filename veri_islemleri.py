import sqlite3


DOSYA = "evcil_hayvanlar.db"


# VERİTABANI ALTYAPISININ HAZIRLANMASI


def veritabani_kur():
    """
    Sistemin çalışması için gerekli tabloları oluşturur ve başlangıç 
    verilerini sisteme yükler.
    """
    # Veritabanı dosyasına bağlantı sağlanır
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()

    # Hayvanlar Tablosu: Tüm fiziksel özellikleri ve sağlık geçmişini saklar.
    # Kullanıcılar arası veri ayrımı 'sahip_id' alanı ile kontrol edilir.
    yazici.execute("""
        CREATE TABLE IF NOT EXISTS hayvanlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            sahip_id TEXT,                         
           ad TEXT,
            yas INTEGER,
            kilo REAL,
            boy REAL,
            cinsiyet TEXT,
            mama_markasi TEXT,
            mama_turu TEXT,                         
            mama_miktari TEXT,
            mama_saati TEXT,
            alerjiler TEXT,
            sevilen_urunler TEXT,
            veteriner_gecmisi TEXT,
            asi_takvimi TEXT,
            durum_notu TEXT
        )
    """)

    # Veterinerler Tablosu: Uygulama içinden ulaşılabilecek uzman bilgilerini tutar.
    yazici.execute("""
        CREATE TABLE IF NOT EXISTS veterinerler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vet_ad TEXT,
            uzmanlik TEXT,
            telefon TEXT
        )
    """)

    # Varsayılan Veri Girişi: Eğer uzman tablosu boşsa rehber bilgileri eklenir.
    # Uzman unvanları ve telefon maskeleme standartlarına göre düzenlenmiştir.
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

    # Yapılan tüm işlemler veritabanına kalıcı olarak işlenir
    baglanti.commit()
    # Veritabanı bağlantısı güvenli bir şekilde kapatılır
    baglanti.close()


#  VERİ EKLEME VE GÜNCELLEME İŞLEMLERİ (DML İşlemleri)


def hayvan_ekle(sahip_id, ad, yas, kilo, boy, cinsiyet, mama_marka, mama_tur, miktar, saat, alerji, urun, vet, asi, durum):
    """
    Arayüzden iletilen bilgileri veritabanı tablosuna yeni bir kayıt olarak ekler.
    Güvenlik için doğrudan değer atamak yerine parametrik sorgu kullanılmıştır.
    """
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()

    # SQL Injection saldırılarını önlemek amacıyla (?) yer tutucuları tercih ettim.
    komut = """INSERT INTO hayvanlar 
               (sahip_id, ad, yas, kilo, boy, cinsiyet, mama_markasi, mama_turu, mama_miktari, mama_saati, alerjiler, sevilen_urunler, veteriner_gecmisi, asi_takvimi, durum_notu) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    
    bilgiler = (sahip_id, ad, yas, kilo, boy, cinsiyet, mama_marka, mama_tur, miktar, saat, alerji, urun, vet, asi, durum)

    yazici.execute(komut, bilgiler)
    baglanti.commit()
    
    
    son_id = yazici.lastrowid
    baglanti.close()
    return son_id


# VERİ SORGULAMA VE LİSTELEME MANTIĞI


def hayvanlari_goster(sahip_id):
    """
    Giriş yapan kullanıcının kimlik bilgisine göre sadece ona ait kayıtları seçer.
    Bu sayede her kullanıcı sadece kendi evcil hayvan listesini görüntüleyebilir.
    """
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()
    
    # WHERE filtresi ile veri tabanından seçici okuma yapılır.
    yazici.execute("SELECT id, ad, yas, kilo, mama_turu FROM hayvanlar WHERE sahip_id = ?", (sahip_id,))
    liste = yazici.fetchall()
    
    baglanti.close()
    return liste

def hayvan_detay_getir(hayvan_id):
    """
    Belirli bir hayvana ait tüm detaylı verileri ID üzerinden sorgular.
    Sağlık raporu ve fiziksel analiz ekranı için gerekli veriyi sağlar.
    """
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()
    yazici.execute("SELECT * FROM hayvanlar WHERE id = ?", (hayvan_id,))
    detay = yazici.fetchone()
    baglanti.close()
    return detay

def veterinerleri_listele():
    """
    Rehberde kayıtlı olan tüm uzman veteriner bilgilerini getirir.
    """
    baglanti = sqlite3.connect(DOSYA)
    yazici = baglanti.cursor()
    yazici.execute("SELECT * FROM veterinerler")
    vets = yazici.fetchall()
    baglanti.close()
    return vets
