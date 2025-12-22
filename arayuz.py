from veri_islemleri import veritabani_kur, hayvan_ekle, hayvanlari_goster, hayvan_detay_getir
from safiye import hayvana_ozel_cozum

kullanicilar = {
    "admin": "12_345", 
    "deneme": "sifre"
}
evcil_hayvanlar = [] 

def verileri_senkronize_et():
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
    detay = hayvan_detay_getir(hayvan_id)
    if detay:
        print("\n" + "="*40)
        print(f" {str(detay[1]).upper()} - BİLGİ VE ANALİZ EKRANI ")
        print("="*40)
        print(f"Adı: {detay[1]} | Cinsi: {detay[5]} | Yaşı: {detay[2]}")
        print(f"Boy: {detay[4]} cm | Kilo: {detay[3]} kg")
        print(f"Mama Saati: {detay[9]} | Miktarı: {detay[8]}")
        print("-" * 40)
        
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
    print("\n--- YENİ HAYVAN KAYIT FORMU ---")
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
        
        hayvan_ekle(ad, yas, kilo, boy, "Belirtilmedi", "Marka", mama_tur, miktar, saat, alerji, "Yok", "Ali Hekim Bey", "Kuduz", "Normal")
        
        print(f"\n[+] {ad} başarıyla sisteme eklendi!")
    except ValueError:
        print("Hata: Sayısal alanları kontrol edin!")

def ana_sayfa(kullanici_adi):
    while True:
        print(f"\n---  ANA SAYFA ({kullanici_adi.upper()}) ---")
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


def giris_kontrol():
    kullanici = input("Kullanıcı Adı: ")
    sifre = input("Parola: ")

    if kullanici == "" or sifre == "":
        print("Boş alan bırakılamaz")
        return

    if kullanici in kullanicilar and kullanicilar[kullanici] == sifre:
        ana_sayfa(kullanici)
    else:
        print("Hatalı giriş")

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
            giris_kontrol() 
        elif secim == '2':
            yeni_ad = input("Yeni Kullanıcı Adı: ").lower()
            if yeni_ad in kullanicilar:
                print("Bu kullanıcı adı zaten alınmış!")
                continue

            yeni_sifre = input("Yeni Parola: ")
            buyuk_harf_var_mi = False
            sayi_var_mi = False

            for karakter in yeni_sifre:
                if karakter.isupper(): buyuk_harf_var_mi = True
                if karakter.isdigit(): sayi_var_mi = True

            if len(yeni_sifre) >= 8 and buyuk_harf_var_mi and sayi_var_mi:
                kullanicilar[yeni_ad] = yeni_sifre
                print(" Kayıt başarılı!")
            else:
                print("\n Hata: Şifre kriterlere uygun değil!")
                print("- En az 8 karakter olmalı")
                print("- En az 1 büyük harf içermeli")
                print("- En az 1 rakam içermeli")
                
        elif secim == '3':
            print("Çıkış yapılıyor...")
            break

if __name__ == "__main__":
    ana_menu()
