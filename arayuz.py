from veri_islemleri import veritabani_kur, hayvan_ekle, hayvanlari_goster, hayvan_detay_getir
from safiye import hayvana_ozel_cozum

# Kullanıcı veritabanı
kullanicilar = {
    "admin": "12_345", 
    "deneme": "sifre"
}
evcil_hayvanlar = [] 

def verileri_senkronize_et():
    """Deniz'in güncel veritabanından (id, ad, yas, kilo, mama_turu) bilgileri çeker."""
    global evcil_hayvanlar
    try:
        gelen_veriler = hayvanlari_goster() 
        evcil_hayvanlar = [] 
        for h in gelen_veriler:
            evcil_hayvanlar.append({
                "id": h[0], 
                "isim": h[1], 
                "yas": h[2], 
                "kilo": h[3],
                "mama_turu": h[4]
            })
    except Exception as e:
        print(f"Veri senkronizasyon hatası: {e}")

def hayvan_detay_sayfasi(hayvan_id):
    """Safiye'nin analiz motorunu ve Deniz'in tüm detaylarını birleştirir."""
    detay = hayvan_detay_getir(hayvan_id)
    if detay:
        print("\n" + "="*40)
        print(f"🐾 {str(detay[1]).upper()} - BİLGİ VE ANALİZ EKRANI 🐾")
        print("="*40)
        print(f"Adı: {detay[1]} | Cinsi: {detay[5]} | Yaşı: {detay[2]}")
        print(f"Boy: {detay[4]} cm | Kilo: {detay[3]} kg")
        print(f"Mama Saati: {detay[9]} | Miktarı: {detay[8]}")
        print("-" * 40)
        
        # Safiye'nin 'Çözüm Açıklayan' fonksiyonunu buraya bağladık
        rapor = hayvana_ozel_cozum(hayvan_id)
        print(rapor)
        
        print("-" * 40)
        input("\nAna menüye dönmek için ENTER'a basın...")

def hayvanlari_goruntule():
    verileri_senkronize_et()
    if not evcil_hayvanlar:
        print("\n[!] Liste boş. Lütfen önce hayvan ekleyin.")
        return

    while True:
        print("\n=== EVCİL HAYVAN LİSTESİ ===")
        for i, h in enumerate(evcil_hayvanlar):
            print(f"{i+1}. {h['isim']} ({h['mama_turu']})")
        
        secim = input("\nDetay ve Çözüm Yolu İçin Numara (Geri: 0): ")
        if secim == '0': break 
        
        try:
            indeks = int(secim) - 1
            if 0 <= indeks < len(evcil_hayvanlar):
                hayvan_detay_sayfasi(evcil_hayvanlar[indeks]["id"])
            else:
                print("Hatalı numara!")
        except ValueError:
            print("Lütfen sayı girin.")

def hayvan_kayit_formu():
    print("\n--- 📝 YENİ HAYVAN KAYIT FORMU ---")
    try:
        ad = input("Adı: ")
        yas = int(input("Yaşı: "))
        kilo = float(input("Kilosu: "))
        boy = float(input("Boyu (cm): "))
        cins = input("Cinsi: ")
        mama_tur = input("Mama Türü (Kuru/Yaş): ")
        miktar = input("Mama Miktarı (Gram): ")
        saat = input("Mama Saatleri: ")
        alerji = input("Alerji Durumu (Yoksa 'Yok'): ")
        
        # Deniz'in 14 parametreli yeni fonksiyonuna gönderiyoruz
        hayvan_ekle(ad, yas, kilo, boy, "Belirtilmedi", "Marka", mama_tur, miktar, saat, alerji, "Yok", "Ali Hekim Bey", "Kuduz", "Normal")
        
        print(f"\n[+] {ad} başarıyla sisteme eklendi!")
    except ValueError:
        print("Hata: Sayısal alanları kontrol edin!")

def ana_sayfa(kullanici_adi):
    while True:
        print(f"\n--- 🏠 ANA SAYFA ({kullanici_adi.upper()}) ---")
        print("1. Hayvanlarımı Listele & Öneri Al")
        print("2. Yeni Hayvan Ekle")
        print("3. Veteriner Listesi (Ali Hekim Bey)")
        print("4. Oturumu Kapat")
        
        secim = input("Seçiminiz: ")
        if secim == '1': hayvanlari_goruntule()
        elif secim == '2': hayvan_kayit_formu()
        elif secim == '3':
            print("\n--- KAYITLI VETERİNERLER ---")
            print("1. Ali Hekim Bey (Cerrahi Uzmanı)")
            print("2. Veli Bey (Aşı Takip)")
            input("\nDevam etmek için ENTER...")
        elif secim == '4': break

def ana_menu():
    veritabani_kur()
    print("*"*40)
    print("  EVCİL HAYVAN SİSTEMİNE HOŞGELDİNİZ  ")
    print("*"*40)
    while True:
        print("\n1. Giriş Yap")
        print("2. Kayıt Ol")
        print("3. Uygulamadan Çık")
        
        secim = input("Seçiminiz: ")
        if secim == '1':
            ad = input("Kullanıcı Adı: ").lower()
            sifre = input("Parola: ")
            if ad in kullanicilar and kullanicilar[ad] == sifre:
                ana_sayfa(ad)
            else:
                print("Hatalı giriş!")
        elif secim == '2':
            yeni_ad = input("Yeni Kullanıcı Adı: ").lower()
            yeni_sifre = input("Parola: ")
            kullanicilar[yeni_ad] = yeni_sifre
            print("Kayıt başarılı!")
        elif secim == '3':
            break

if __name__ == "__main__":
    ana_menu()
