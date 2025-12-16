kullanicilar = {
    "admin": "12345", 
    "deneme": "sifre"
}
evcil_hayvanlar = [
    {
        "sahip": "admin", 
        "isim": "Karabas", 
        "cins": "Kedi", 
        "yas": 3, 
        "kilo": 5.2,
        "ozel_not": "Yaş mamayı sever.",
        "asi_takvimi": [{"ad": "Karma Aşı", "tarih": "01.03.2024", "yapildi": True}],
        "gecmis_veriler": [{"tarih": "15.10.2024", "kilo": 5.0, "durum": "Rutin kontrol."}]
    },
    {
        "sahip": "deneme", 
        "isim": "Fındık", 
        "cins": "Köpek", 
        "yas": 1, 
        "kilo": 8.5,
        "ozel_not": "Top oynamayı çok sever.",
        "asi_takvimi": [{"ad": "Kuduz Aşısı", "tarih": "15.01.2025", "yapildi": False}],
        "gecmis_veriler": []
    },
] 

def hayvan_detay_sayfasi(hayvan):
    print("\n**************")
    print(f" 🐾 {hayvan['isim'].upper()} - DETAY SAYFASI 🐾")
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
    kullaniciya_ait_hayvanlar = [h for h in evcil_hayvanlar if h["sahip"] == sahip_adi]
    
    if not kullaniciya_ait_hayvanlar:
        print("\nKayıtlı evcil hayvanınız bulunmamaktadır.")
        return

    while True:
        print("\n==================================")
        print("EVCİL HAYVAN LİSTESİ")
        print("\n==================================")
        
      
        for i, hayvan in enumerate(kullaniciya_ait_hayvanlar):
            print(f"{i+1}. {hayvan['isim']} (Cins: {hayvan['cins']}, Yaş: {hayvan['yas']} yıl)")
        
        secim = input("\nDetay numarasını girin (Geri dönmek için '0'): ")
        
        if secim == '0':
            return 
        
        try:
            secilen_index = int(secim) - 1
            if 0 <= secilen_index < len(kullaniciya_ait_hayvanlar):
                hayvan_detay_sayfasi(kullaniciya_ait_hayvanlar[secilen_index])
            else:
                print(" Hata: Geçersiz sıra numarası.")
        except ValueError:
            print(" Hata: Lütfen geçerli bir numara girin.")

def hayvan_kayit_formu(sahip_adi):
     print("\n--- YENİ EVCİL HAYVAN KAYIT FORMU ---")
    
while True:
        try:
            isim = input("Hayvanın Adı: ")
            cins = input("Hayvanın Cinsi: ")
            yas = int(input("Yaşı (yıl): "))
            kilo = float(input("Kilosu (kg): "))

            yeni_hayvan = {
                "sahip":isim, "isim": isim, "cins": cins, "yas": yas, "kilo": kilo,
                "ozel_not": input("Özel Notlar (Opsiyonel): "),
                "asi_takvimi": [], "gecmis_veriler": []
            }
            evcil_hayvanlar.append(yeni_hayvan)
            print(f"\n {isim} başarıyla kaydedildi!")
            break
        except ValueError:
            print("Hata: Yaş ve kilo alanlarına sadece sayı girmelisiniz.")

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
    while True:
        print("\n==============================")
        print(" EVCİL HAYVAN UYGULAMASI MENÜSÜ")
        print("==============================")
        print("1. Giriş Yap")
        print("2. Kaydol")
        print("3. Çıkış")
        
        ana_secim = input("Seçiminizi yapın (1-3): ")
       
        if ana_secim == '1':
            giris_yap()
        elif ana_secim == '2':
            kayit_ol()
        elif ana_secim == '3':
            print("Uygulamadan çıkılıyor. İyi günler!")
            break
        else:
            print("Hatalı seçim!")

if __name__== "_main_":
    ana_menu()



