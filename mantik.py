from veri_islemleri import hayvan_detay_getir, veterinerleri_listele

# 1. AKILLI ANALİZ VE MAMA MOTORU
def hayvana_ozel_cozum(hayvan_id): 
    """Veritabanından bilgileri alır ve akıllı algoritma ile analiz eder."""
    detay = hayvan_detay_getir(hayvan_id)
    if not detay:
        return "Hayvan bilgisi bulunamadı."

    # Veritabanı sütun eşleşmeleri (hayvanlar tablosu):
    # 2:ad, 3:yas, 4:kilo, 5:boy, 7:mama_markasi, 8:mama_turu, 9:mama_miktari, 10:mama_saati, 11:alerji, 14:asi_takvimi
    ad = detay[2]
    yas = detay[3]
    kilo = detay[4]
    boy = detay[5]
    mevcut_marka = detay[7] if detay[7] else "Belirtilmedi"
    mama_turu = detay[8] 
    girilen_miktar = detay[9] if detay[9] else 0
    girilen_saat = detay[10] if detay[10] else "Belirtilmedi"
    alerji = detay[11].lower() if detay[11] else "yok"
    asi_bilgisi = detay[14] if detay[14] else "Bilgi girilmedi"
    
    cozum = f"[b]--- {ad.upper()} ANALİZ VE BESLENME RAPORU ---[/b]\n"
    cozum += "="*35 + "\n"
    
    # 1. Kilo/Boy Analizi
    durum = "İdeal"
    if boy > 0:
        endeks = kilo / boy
        if endeks > 0.5:
            durum = "Kilolu"
            cozum += f" DURUM: {durum}\n- ÖNERİ: Hareket artırılmalı, oyun süresi +15 dk.\n"
        elif endeks < 0.2:
            durum = "Zayıf"
            cozum += f" DURUM: {durum}\n- ÖNERİ: Protein oranı yüksek beslenme düzeni.\n"
        else:
            cozum += " DURUM: İdeal kilo bulundu.\n"
    
    # 2. Mevcut Beslenme Düzeni (Kayıp Veriler)
    cozum += f"\n[b]🕒 GÜNCEL DURUM:[/b]\n"
    cozum += f"- Kullanılan Marka: {mevcut_marka}\n"
    cozum += f"- Besleme Saati: {girilen_saat}\n"
    cozum += f"- Sizin Verdiğiniz: {girilen_miktar} Gram\n"

    # 3. Aşı Durumu
    cozum += f"\n[b]💉 AŞI TAKVİMİ:[/b]\n- Son Kayıt: {asi_bilgisi}\n"

    # 4. Beslenme Planı Hesaplama
    if yas < 2:
        gramaj = kilo * 25 # Yavru/Genç
    elif yas > 7:
        gramaj = kilo * 12 # Yaşlı
    else:
        gramaj = kilo * 18 # Yetişkin

    if durum == "Kilolu": gramaj *= 0.8 # %20 azalt
    if durum == "Zayıf": gramaj *= 1.2  # %20 artır

    cozum += f"\n[b]🍴 SAFİYE'NİN İDEAL PLANI:[/b]\n"
    cozum += f"- Gereken Miktar: [b]{int(gramaj)} Gram[/b]\n"
    
    # Miktar Kıyaslama Analizi
    try:
        fark = int(gramaj) - int(girilen_miktar)
        if fark > 20:
            cozum += f"! Öneri: Günlük porsiyonu {fark} gr artırmanız iyi olabilir.\n"
        elif fark < -20:
            cozum += f"! Öneri: Günlük porsiyonu {abs(fark)} gr azaltmanız iyi olabilir.\n"
    except:
        pass

    # 5. Mama Markası Önerisi
    cozum += f"\n[b]🛒 ÖNERİLEN MAMA TÜRÜ:[/b] "
    if "tavuk" in alerji:
        cozum += "Kuzulu/Somonlu (Hiporalerjenik)\n- Öneri: Royal Canin Dermacomfort\n"
    elif "tahil" in alerji or "buğday" in alerji:
        cozum += "Tahılsız (Grain Free)\n- Öneri: N&D Prime veya Orijen\n"
    else:
        cozum += "Premium Standart\n- Öneri: Pro Plan veya Hill's\n"

    # 6. Dinamik Uzman Veterinerler (Veritabanından çekilir)
    cozum += "\n" + "-"*35 + "\n"
    cozum += "[b]👨‍⚕️ SİSTEME KAYITLI UZMANLARIMIZ:[/b]\n"
    
    vets = veterinerleri_listele()
    if vets:
        for v in vets[:2]: # İlk 2 veterineri listele
            cozum += f"- {v[1]} ({v[2]})\n  İletişim: {v[3]}\n"
    else:
        cozum += "Kayıtlı veteriner bulunamadı.\n"
    
    return cozum

# 2. TKINTER ARAYÜZÜ (PC TESTİ İÇİN)
def pencereyi_ac():
    import tkinter as tk
    from tkinter import messagebox
    pencere = tk.Tk()
    pencere.title("Safiye | Akıllı Analiz Sistemi")
    pencere.geometry("500x700")
    pencere.configure(bg="#f0f0f0")
    
    tk.Label(pencere, text=" SAFİYE KARAR DESTEK", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=15)
    tk.Label(pencere, text="Analiz Sonucu:", bg="#f0f0f0").pack()
    
    cozum_alani = tk.Text(pencere, height=20, width=55, font=("Courier", 10), padx=10, pady=10)
    cozum_alani.pack(pady=5)
    
    def analizi_goster():
        # Test amaçlı 1 numaralı hayvanı çekiyoruz
        rapor = hayvana_ozel_cozum(1)
        # Kivy taglerini temizle
        temiz_rapor = rapor.replace("[b]","").replace("[/b]","").replace("[u]","").replace("[/u]","").replace("[color=ff9900]","").replace("[/color]","")
        cozum_alani.delete('1.0', tk.END)
        cozum_alani.insert(tk.END, temiz_rapor)

    tk.Button(pencere, text=" ANALİZİ ÇALIŞTIR", command=analizi_goster, 
              bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=25).pack(pady=10)

    pencere.mainloop()

if __name__ == "__main__":
    from veri_islemleri import veritabani_kur
    veritabani_kur()
    pencereyi_ac()
