from veri_islemleri import veritabani_kur, hayvan_ekle, hayvanlari_ekle, hayvanlari_göster

kullanicilar = {
    "admin": "12345", 
    "deneme": "sifre"
}
evcil_hayvanlar = [] 
def verileri_senkronize_et()
    global evcil_hayvanlar
    evcil_haycanlar = []
    gelen_veriler = hayvanlari_göster()

    for h in gelen_veriler:
        yeni = {
            "id": h[0], "isim": h[1], "yas": h[2], "kilo": h[3],
            "cins": "Belirtilmedi", "ozel_not": "Yok",
            "asi_takvimi": [], "gecmis_veriler": []
        }
        evcil_hayvanlar.append(yeni)



def hayvan_detay_sayfasi(hayvan):
    print("\n**************")
    print(f"{hayvan['isim'].upper()} - DETAY SAYFASI ")
    print("**************")
  
    print("\n--- TEMEL BİLGİLER ---")
    print(f"Adı: {hayvan['isim']}, Cinsi: {hayvan['cins']}, Yaşı: {hayvan['yas']} yıl, Kilosu: {hayvan['kilo']} kg")
    print(f"Özel Not: {hayvan.get('ozel_not', 'Yok')}")
  
    print("\n--- AŞI TAKVİMİ ---")
    if hayvan.get('asi_takvimi'):
        for a in hayvan['asi_takvimi']:
            durum = " YAPILDI" if a['yapildi'] else "BEKLİYOR"
            print(f"- {a['ad']} ({a['tarih']}): {durum}")
    else:
        print("Aşı kaydı yok.")

    print("\n--- GEÇMİŞ VERİLER ---")
    if hayvan.get('gecmis_veriler'):
        for g in hayvan['gecmis_veriler']:
            print(f"[{g['tarih']}] Kilo: {g['kilo']} kg, Durum: {g['durum']}")
    else:
        print("Geçmiş veri kaydı yok.")
        
    input("\nDevam etmek için ENTER tuşuna basın...")

def hayvanlari_goruntule(sahip_adi):
    verileri_senkronize_et()
    
    if not evcil_hayvanlar:
        print("\nKayıtlı evcil hayvanınız bulunmamaktadır.")
        return

    while True:
        print("\n==================================")
        print("EVCİL HAYVAN LİSTESİ")
        print("\n==================================")
        for i, hayvan in enumerate(evcil_hayvanlar):
            print(f"{i+1}. {hayvan['isim']} (Yaş: {hayvan['yas']} yıl)")
        
        secim = input("\nDetay numarası (Geri için '0'): ")
        if secim == '0': return 
        
        try:
            secilen_index = int(secim) - 1
            if 0 <= secilen_index < len(evcil_hayvanlar):
                hayvan_detay_sayfasi(evcil_hayvanlar[secilen_index])
        except ValueError:
            print("Hata: Geçersiz numara.")

def hayvan_kayit_formu(sahip_adi):
    print("\n--- YENİ EVCİL HAYVAN KAYIT FORMU ---")
    try:
        isim = input("Hayvanın Adı: ")
        cins = input("Hayvanın Cinsi: ")
        yas = int(input("Yaşı (yıl): "))
        kilo = float(input("Kilosu (kg): "))
        notu = input("Özel Not: ")

        hayvan_ekle(isim, yas, kilo, cins, "Yok", "Yok", "Yok", "Yok", "Yok", "Yok", notu, "Yok")
        
        verileri_senkronize_et()
        print(f"\n {isim} başarıyla kaydedildi!")
    except ValueError:
        print("Hata: Sayı girmelisiniz.")


def ana_sayfa(kullanici_adi):
    print(f"\n** HOŞ GELDİNİZ, {kullanici_adi.upper()}! **")
    
    while True:
        print("\n--- MENÜ ---")
        print("1. Hayvan Listesini Görüntüle (Detay)")
        print("2. Yeni Evcil Hayvan Kaydet")
        print("3. Çıkış Yap")
        
        secim = input("Seçiminizi yapın (1-3): ")
        
        if secim == '1':
            hayvanlari_goruntule(kullanici_adi) 
        elif secim == '2':
            hayvan_kayit_formu(kullanici_adi) 
        elif secim == '3':
            print(" Güle güle! Ana menüye dönülüyor.")
            return
        else:
            print("Geçersiz seçim.")

def kayit_ol():
    print("\n--- YENİ KAYIT EKRANI ---")
    while True:
        yeni_kullanici_adi = input("Yeni Kullanıcı Adınızı Girin: ").lower()
        if yeni_kullanici_adi in kullanicilar:
            print("Bu kullanıcı adı zaten mevcut.")
        else:
            yeni_parola = input("Parolanızı Girin: ")
            kullanicilar[yeni_kullanici_adi] = yeni_parola
            print(f"\n {yeni_kullanici_adi} başarıyla kaydedildi!")
            return

def giris_yap():
    """Kullanıcı girişini doğrular."""
    print("\n--- GİRİŞ EKRANI ---")
    kullanici_adi = input("Kullanıcı Adı: ").lower()
    parola = input("Parola: ")
    
    if kullanici_adi in kullanicilar and kullanicilar[kullanici_adi] == parola:
        print("\n Başarılı giriş!")
        ana_sayfa(kullanici_adi)
    else:
        print("\n Hatalı giriş bilgileri.")

def ana_menu():
    veritabani_kur() 
    while True:
        print("\n1. Giriş Yap\n2. Kaydol\n3. Çıkış")
        secim = input("Seçim: ")
        if secim == '1': giris_yap()
        elif secim == '2': kayit_ol()
        elif secim == '3': break

if __name__ == "__main__":
    ana_menu()
