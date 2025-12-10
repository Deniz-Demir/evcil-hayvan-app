import sqlite3
import datetime

# Veritabanı dosyamızın adı
DB_ADI = "evcil_hayvanlar.db"

# ====================================================================
# YARDIMCI İŞLEV: Bağlantı Kurma
# ====================================================================

def baglanti_ac():
    """Veritabanı bağlantısını açar ve 'with' ifadesi için hazırlar."""
    return sqlite3.connect(DB_ADI)

# ====================================================================
# 1. TEMEL KURULUM
# ====================================================================

def veritabani_kur():
    """Veritabanını ve gerekli tüm tabloları oluşturur."""
    with baglanti_ac() as conn: 
        cur = conn.cursor()

        # HAYVANLAR TABLOSU (Tüm 13 sütun korundu)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hayvanlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
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

        # PAYLAŞIMLAR TABLOSU
        cur.execute("""
            CREATE TABLE IF NOT EXISTS paylasimlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici TEXT,
                urun TEXT,
                tarih TEXT
            )
        """)

# ====================================================================
# 2. KAYIT EKLEME (CREATE)
# ====================================================================

def hayvan_ekle(ad, yas, kilo, cinsiyet, mama_markasi, alerjiler,
                sevilen_urunler, veteriner_gecmisi, gunluk_rutin,
                asi_takvimi, durum_notu, acil_durum_notu):
    """Yeni bir evcil hayvanın tüm 12 detayını kaydeder."""
    
    # Tüm verileri tek bir demet (tuple) içinde topluyoruz.
    degerler = (ad, yas, kilo, cinsiyet, mama_markasi, alerjiler,
                sevilen_urunler, veteriner_gecmisi, gunluk_rutin,
                asi_takvimi, durum_notu, acil_durum_notu)
    
    with baglanti_ac() as conn:
        cur = conn.cursor()
        
        # INSERT INTO komutu: 12 alan adı ve 12 soru işareti (?) var.
        cur.execute("""
            INSERT INTO hayvanlar (
             ad, yas, kilo, cinsiyet, mama_markasi, alerjiler, sevilen_urunler, 
             veteriner_gecmisi, gunluk_rutin, asi_takvimi, durum_notu, acil_durum_notu
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, degerler) # Değerleri sırasıyla gönderiyoruz.

    return f"{ad} başarıyla eklendi."

# ====================================================================
# 3. KAYIT GÜNCELLEME (UPDATE)
# ====================================================================

# Fonksiyon çok uzun görünse de, içerideki mantık çok kısaldı.
def hayvan_guncelle(hayvan_id, ad=None, yas=None, kilo=None, cinsiyet=None,
                    mama_markasi=None, alerjiler=None, sevilen_urunler=None,
                    veteriner_gecmisi=None, gunluk_rutin=None, asi_takvimi=None,
                    durum_notu=None, acil_durum_notu=None):
    """Sadece gönderilen alanları günceller."""
    
    # Sadece None (Boş) olmayan, yani gerçekten yeni bir değer alanları topluyoruz
    guncellenecek_alanlar = {}
    
    # Alanları tek tek kontrol edip, boş değilse (None değilse) sözlüğe ekle:
    if ad is not None: guncellenecek_alanlar['ad'] = ad
    if yas is not None: guncellenecek_alanlar['yas'] = yas
    if kilo is not None: guncellenecek_alanlar['kilo'] = kilo
    if cinsiyet is not None: guncellenecek_alanlar['cinsiyet'] = cinsiyet
    if mama_markasi is not None: guncellenecek_alanlar['mama_markasi'] = mama_markasi
    if alerjiler is not None: guncellenecek_alanlar['alerjiler'] = alerjiler
    if sevilen_urunler is not None: guncellenecek_alanlar['sevilen_urunler'] = sevilen_urunler
    if veteriner_gecmisi is not None: guncellenecek_alanlar['veteriner_gecmisi'] = veteriner_gecmisi
    if gunluk_rutin is not None: guncellenecek_alanlar['gunluk_rutin'] = gunluk_rutin
    if asi_takvimi is not None: guncellenecek_alanlar['asi_takvimi'] = asi_takvimi
    if durum_notu is not None: guncellenecek_alanlar['durum_notu'] = durum_notu
    if acil_durum_notu is not None: guncellenecek_alanlar['acil_durum_notu'] = acil_durum_notu
    
    # Eğer güncellenecek bir şey yoksa, dur
    if not guncellenecek_alanlar:
        return "Güncellenecek yeni bilgi bulunamadı."
        
    # SQL CÜMLESİNİ ÇOK TEMİZ BİR ŞEKİLDE OLUŞTURMA (En büyük kolaylık)
    # Örn: 'ad = ?, kilo = ?, durum_notu = ?' şeklinde bir metin oluşturur.
    set_komutu = ', '.join([f"{k} = ?" for k in guncellenecek_alanlar.keys()])
    
    # SQL sorgusunun tamamını oluştur:
    sql_komutu = f"UPDATE hayvanlar SET {set_komutu} WHERE id = ?"
    
    # Değerler listesini hazırlıyoruz: Önce yeni değerler, sonra ID
    degerler = list(guncellenecek_alanlar.values()) 
    degerler.append(hayvan_id)

    with baglanti_ac() as conn:
        cur = conn.cursor()

        # Önce kayıt var mı kontrol et (Önemli!)
        cur.execute("SELECT id FROM hayvanlar WHERE id = ?", (hayvan_id,))
        if cur.fetchone() is None:
            return "Kayıt bulunamadı."
            
        # SQL komutunu çalıştır
        cur.execute(sql_komutu, degerler)
        
    return "Güncelleme tamamlandı."

# ====================================================================
# 4. VERİ OKUMA (READ)
# ====================================================================

def hayvan_detay(hayvan_id):
    """Belirtilen ID'ye sahip hayvanın tüm detaylarını getirir (Demet döndürür)."""
    with baglanti_ac() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM hayvanlar WHERE id = ?", (hayvan_id,))
        sonuc = cur.fetchone() # Sadece ilk kaydı al
    return sonuc 

def hayvanlari_listele():
    """Tüm hayvanların temel bilgilerini bir liste olarak getirir."""
    with baglanti_ac() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, ad, cinsiyet, yas, kilo FROM hayvanlar")  
        sonuclar = cur.fetchall() 
    return sonuclar

# ====================================================================
# 5. VERİ SİLME (DELETE)
# ====================================================================

def hayvan_sil(hayvan_id):
    """Belirtilen ID'ye sahip hayvan kaydını veritabanından siler."""
    with baglanti_ac() as conn:
        cur = conn.cursor()
        
        # Silmeden önce kayıt kontrolü
        cur.execute("SELECT id FROM hayvanlar WHERE id = ?", (hayvan_id,))
        if cur.fetchone() is None:
            return "Kayıt bulunamadı. Silme işlemi iptal edildi."

        # Silme komutu
        cur.execute("DELETE FROM hayvanlar WHERE id = ?", (hayvan_id,))
        
    return f"ID {hayvan_id} numaralı kayıt silindi."

# ====================================================================
# 6. YARDIMCI İŞLEV (PAYLAŞIM)
# ====================================================================

def paylasim_ekle(kullanici, urun):
    """Sosyal paylaşım tablosuna yeni bir kayıt ekler."""
    tarih = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with baglanti_ac() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO paylasimlar (kullanici, urun, tarih)
            VALUES (?, ?, ?)
        """, (kullanici, urun, tarih))

    return "Paylaşım başarıyla kaydedildi."
