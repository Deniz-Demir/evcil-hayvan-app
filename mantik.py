from veri_islemleri import hayvan_detay_getir

# 1. AKILLI ANALİZ VE MAMA MOTORU
def hayvana_ozel_cozum(hayvan_id):
    """
    Veritabanından bilgileri alır ve akıllı algoritma ile analiz eder.
    Düzenleme: Mama türü değerlendirmesi ve veteriner bilgileri güncellendi.
    """
    detay = hayvan_detay_getir(hayvan_id)
    if not detay:
        return "❌ Hayvan bilgisi bulunamadı."

    # Veritabanı sütun eşleşmeleri:
    # 1:ad, 2:yas, 3:kilo, 4:boy, 7:mama_markasi, 8:mama_turu, 11:alerji, 15:durum_notu
    ad = detay[1]
    kilo = detay[3]
    boy = detay[4]
    mama_turu = detay[8] # Yeni eklenen Kuru/Yaş bilgisi
    alerji = detay[11]
    
    cozum = f"--- 🐾 {ad.upper()} ANALİZ RAPORU ---\n"
    cozum += "="*35 + "\n"
    
    # 📊 Kilo/Boy Endeksi Analizi
    if boy > 0:
        endeks = kilo / boy
        if endeks > 0.5:
            cozum += "⚠️ DURUM: Kilolu\n- ÖNERİ: Hareket artırılmalı, günlük oyun süresi +15 dk.\n"
        elif endeks < 0.2:
            cozum += "⚠️ DURUM: Zayıf\n- ÖNERİ: Protein oranı yüksek beslenme düzeni.\n"
        else:
            cozum += "✅ DURUM: İdeal kilo saptandı.\n"
    
    # 🍽️ Mama Türü ve Alerji Değerlendirmesi (3. Madde Düzenlemesi)
    cozum += f"\n🍴 MEVCUT BESLENME: {mama_turu} Mama\n"
    
    if str(alerji).lower() != "yok" and str(alerji).strip() != "":
        cozum += f"🚨 UYARI: {alerji} alerjisi var! Sadece hiporalerjenik {mama_turu} mama kullanın.\n"
    else:
        cozum += f"✅ Alerji saptanmadı, standart {mama_turu} mama devam edebilir.\n"

    # 👨‍⚕️ Uzman Veteriner Tavsiyesi (4. Madde Düzenlemesi)
    # Unvan "Uzman Veteriner" yapıldı, numara gizlendi.
    cozum += "\n" + "-"*35 + "\n"
    cozum += "👨‍⚕️ TAVSİYE EDİLEN UZMAN:\n"
    cozum += "Ali Hekim Bey - Uzman Veteriner\n"
    cozum += "📞 İletişim: 05xx xxx xx xx\n"
    
    return cozum

# 2. TKINTER ARAYÜZÜ (Geliştirilmiş Görünüm)
def pencereyi_ac():
    import tkinter as tk
    from tkinter import messagebox

    pencere = tk.Tk()
    pencere.title("Safiye | Akıllı Analiz Sistemi")
    pencere.geometry("500x650")
    pencere.configure(bg="#f0f0f0")

    # Başlık
    tk.Label(pencere, text="🐾 SAFİYE KARAR DESTEK", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=15)

    # Analiz Sonuç Alanı
    tk.Label(pencere, text="Hayvan Analizi ve Uzman Görüşü:", bg="#f0f0f0").pack()
    cozum_alani = tk.Text(pencere, height=12, width=55, font=("Courier", 10), padx=10, pady=10)
    cozum_alani.pack(pady=5)

    def analizi_goster():
        # Buradaki ID normalde arayüzden seçilen hayvandan gelir.
        # Test için 1 numaralı hayvanı çekiyoruz.
        rapor = hayvana_ozel_cozum(1)
        cozum_alani.delete('1.0', tk.END)
        cozum_alani.insert(tk.END, rapor)

    tk.Button(pencere, text="🔍 ANALİZİ ÇALIŞTIR", command=analizi_goster, 
              bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=25).pack(pady=10)

    # Veteriner Listesi (Düzeltilmiş Hali)
    tk.Label(pencere, text="🏥 KAYITLI UZMANLARIMIZ", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=10)
    
    # 4. Madde: Uzman veteriner yazısı ve maskeli numara
    vet_bilgi = "1. Ali Hekim Bey (Uzman Veteriner) - 05xx xxx xx xx\n2. Veli Bey (Uzman Veteriner) - 05xx xxx xx xx"
    tk.Label(pencere, text=vet_bilgi, fg="#2980b9", justify="left", bg="#f0f0f0").pack()

    # Hatırlatıcı Bölümü
    tk.Label(pencere, text="\n⏰ HIZLI HATIRLATICI", font=("Arial", 10, "bold"), bg="#f0f0f0").pack()
    hatirlatma_entry = tk.Entry(pencere, width=40)
    hatirlatma_entry.pack(pady=5)
    
    def hatirlatma_ekle():
        metin = hatirlatma_entry.get()
        if metin:
            liste_kutusu.insert(tk.END, f"• {metin}")
            hatirlatma_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Uyarı", "Lütfen bir hatırlatma girin!")

    tk.Button(pencere, text="➕ EKLE", command=hatirlatma_ekle, width=10).pack()

    liste_kutusu = tk.Listbox(pencere, width=55, height=5)
    liste_kutusu.pack(pady=15)

    pencere.mainloop()

if __name__ == "__main__":
    from veri_islemleri import veritabani_kur
    veritabani_kur()
    pencereyi_ac()
