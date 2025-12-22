import tkinter as tk
from tkinter import messagebox
from veri_islemleri import veritabani_kur, hayvan_detay_getir

def hayvana_ozel_cozum(hayvan_id):
    detay = hayvan_detay_getir(hayvan_id)
    if not detay:
        return "❌ Hayvan bilgisi bulunamadı."

    # Deniz'in tablosuna göre alanlar
    ad = detay[1]
    yas = detay[2]
    kilo = detay[3]
    boy = detay[4]
    mama_tur = detay[7]
    alerji = detay[10]
    parazit = detay[13]

    rapor = f"🐾 {ad.upper()} İÇİN AKILLI ANALİZ RAPORU\n"
    rapor += "-" * 45 + "\n"

    puan = 100  # Genel sağlık puanı
    
    # KİLO / BOY ANALİZİ
    if boy > 0:
        endeks = kilo / boy
        rapor += f"📏 Kilo/Boy Endeksi: {endeks:.2f}\n"

        if endeks > 0.5:
            rapor += "⚠️ DURUM: Kilolu\n"
            rapor += "➡️ ÖNERİ: Günlük aktivite +15 dk artırılmalı\n"
            puan -= 15
        elif endeks < 0.2:
            rapor += "⚠️ DURUM: Zayıf\n"
            rapor += "➡️ ÖNERİ: Protein oranı yüksek mama\n"
            puan -= 20
        else:
            rapor += "✅ DURUM: İdeal kilo\n"
    else:
        rapor += "❗ Boy bilgisi eksik\n"
        puan -= 10
        
    # ALERJİ KONTROLÜ
    if str(alerji).lower() != "yok":
        rapor += f"\n🚨 ALERJİ: {alerji}\n"
        rapor += "➡️ Hiporalerjenik mama zorunlu\n"
        puan -= 25
    else:
        rapor += "\n✅ Alerji tespit edilmedi\n"
        
    # PARAZİT DURUMU
    if str(parazit).lower() != "yok":
        rapor += f"\n🦠 PARAZİT UYARISI: {parazit}\n"
        rapor += "➡️ Acil veteriner kontrolü önerilir\n"
        puan -= 30
    else:
        rapor += "\n✅ Parazit bulgusu yok\n"
        
    # MAMA DEĞERLENDİRMESİ
    rapor += f"\n🍽️ Mevcut Mama Türü: {mama_tur}\n"
    rapor += "➡️ Mama seçimi yaş ve kiloya göre kontrol edildi\n"

    # GENEL SAĞLIK PUANI
    
    rapor += "\n📊 GENEL SAĞLIK PUANI: " + str(max(puan, 0)) + "/100\n"

    if puan >= 80:
        rapor += "🟢 Genel durum çok iyi\n"
    elif puan >= 50:
        rapor += "🟡 Takip edilmeli\n"
    else:
        rapor += "🔴 Riskli – Veteriner önerilir\n"
        
    # VETERİNER ÖNERİSİ
    rapor += "\n👨‍⚕️ ÖNERİLEN VETERİNER: Ali Hekim Bey\n"
    return rapor



# 2. TKINTER ARAYÜZÜ (DETAYLANDIRILDI)
def pencereyi_ac():
    pencere = tk.Tk()
    pencere.title("Safiye | Akıllı Hayvan Takip Sistemi")
    pencere.geometry("550x700")

    tk.Label(pencere, text="🐶 EVCİL HAYVAN ÇÖZÜM MERKEZİ",
             font=("Arial", 14, "bold")).pack(pady=10)

    # HAYVAN SEÇİMİ
    tk.Label(pencere, text="Hayvan ID Giriniz:").pack()
    hayvan_id_entry = tk.Entry(pencere, width=10)
    hayvan_id_entry.pack(pady=5)
    
    # ANALİZ ALANI
    cozum_alani = tk.Text(pencere, height=18, width=65)
    cozum_alani.pack(pady=10)

    def analizi_goster():
        try:
            hayvan_id = int(hayvan_id_entry.get())
            rapor = hayvana_ozel_cozum(hayvan_id)
            cozum_alani.delete("1.0", tk.END)
            cozum_alani.insert(tk.END, rapor)
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir ID girin")

    tk.Button(
        pencere,
        text="🔍 Hayvanı Analiz Et",
        command=analizi_goster,
        bg="lightgreen"
    ).pack(pady=5)
    
    # HATIRLATICI SİSTEMİ

    tk.Label(pencere, text="⏰ Hatırlatıcı (Örn: 08:00 Mama)").pack()
    hatirlatma_entry = tk.Entry(pencere, width=40)
    hatirlatma_entry.pack()

    liste_kutusu = tk.Listbox(pencere, width=55, height=8)
    liste_kutusu.pack(pady=10)

    def hatirlatma_ekle():
        if hatirlatma_entry.get():
            liste_kutusu.insert(tk.END, f"⏰ {hatirlatma_entry.get()}")
            hatirlatma_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Uyarı", "Hatırlatma boş olamaz")

    tk.Button(pencere, text="➕ Hatırlatıcı Ekle",
              command=hatirlatma_ekle).pack(pady=5)

    # VETERİNER BİLGİSİ
  
    tk.Label(pencere, text="👨‍⚕️ Kayıtlı Veterinerler",
             font=("Arial", 10, "bold")).pack(pady=5)

    vets = (
        "1️⃣ Ali Hekim Bey – Genel & Cerrahi\n"
        "2️⃣ Veli Bey – Aşı ve Koruyucu Sağlık"
    )
    tk.Label(pencere, text=vets, fg="blue").pack()

    pencere.mainloop()

if __name__ == "__main__":
    veritabani_kur()
    pencereyi_ac()
