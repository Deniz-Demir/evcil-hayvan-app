# Safiye'nin Bölümü: Öneri, Hatırlatma ve Akıllı Analiz Sistemi
import tkinter as tk
from veri_islemleri import veritabani_kur, hayvan_ekle, hayvan_detay_getir

# 1. AKILLI ANALİZ VE MAMA MOTORU
def hayvana_ozel_cozum(hayvan_id):
    """Deniz'in veritabanından bilgileri alır ve Safiye'nin mantığıyla analiz eder."""
    detay = hayvan_detay_getir(hayvan_id)
    if not detay:
        return "Hayvan bilgisi bulunamadı."

    # Deniz'in yeni tablosuna göre indexler: kilo=3, boy=4, mama_tur=7, alerji=10, parazit=13
    ad = detay[1]
    kilo = detay[3]
    boy = detay[4]
    alerji = detay[10]
    
    cozum = f"--- {ad.upper()} İÇİN ANALİZ RAPORU ---\n"
    
    # Kilo/Boy Endeksi Analizi (İlerlemesi gereken yol)
    if boy > 0:
        endeks = kilo / boy
        if endeks > 0.5:
            cozum += "- DURUM: Kilolu. Hareket artırılmalı.\n- YOL HARİTASI: Günlük yürüyüş süresini 15 dk artırın.\n"
        elif endeks < 0.2:
            cozum += "- DURUM: Zayıf. Besin değeri yüksek mamaya geçilmeli.\n"
        else:
            cozum += "- DURUM: İdeal kiloda. Mevcut düzen korunmalı.\n"
    
    # Alerji ve Mama Durumu
    if str(alerji).lower() != "yok":
        cozum += f"- UYARI: {alerji} alerjisi var! Hiporalerjenik mama zorunludur.\n"
    else:
        cozum += "- BESLENME: Alerji saptanmadı, standart mama kullanılabilir.\n"

    # Veteriner Tavsiyesi (Ali Hekim Bey eklendi)
    cozum += "- ÖNERİ: Genel kontrol için Ali Hekim Bey'e görünebilirsiniz.\n"
    
    return cozum

# 2. ARAYÜZ (TKINTER) - Safiye'nin Paneli
def pencereyi_ac():
    pencere = tk.Tk()
    pencere.title("Safiye - Karar Destek ve Randevu Sistemi")
    pencere.geometry("500x600")

    # Başlık
    tk.Label(pencere, text="EVCİL HAYVAN ÇÖZÜM MERKEZİ", font=("Arial", 14, "bold")).pack(pady=10)

    # Öneri ve Çözüm Ekranı
    tk.Label(pencere, text="Hayvan Analizi ve Tavsiyeler:").pack()
    cozum_alani = tk.Text(pencere, height=10, width=50)
    cozum_alani.pack(pady=5)

    def analizi_goster():
        # Test için 1 numaralı hayvanı analiz et (Deniz'in db'sindeki ilk kayıt)
        rapor = hayvana_ozel_cozum(1)
        cozum_alani.delete('1.0', tk.END)
        cozum_alani.insert(tk.END, rapor)

    tk.Button(pencere, text="Seçili Hayvanı Analiz Et", command=analizi_goster, bg="lightgreen").pack(pady=5)

    # Hatırlatıcı Bölümü
    tk.Label(pencere, text="Hatırlatıcı (Örn: Sabah 08:00 Mama)").pack(pady=5)
    hatirlatma_entry = tk.Entry(pencere, width=40)
    hatirlatma_entry.pack()
    
    def hatirlatma_ekle():
        liste_kutusu.insert(tk.END, f"⏰ {hatirlatma_entry.get()}")
        hatirlatma_entry.delete(0, tk.END)

    tk.Button(pencere, text="Hatırlatıcı Ekle", command=hatirlatma_ekle).pack(pady=5)

    # Veteriner Listesi
    tk.Label(pencere, text="Kayıtlı Veterinerlerimiz:").pack(pady=5)
    vets = "1. Ali Hekim Bey (Cerrahi) \n2. Veli Bey (Aşı Uzmanı)"
    tk.Label(pencere, text=vets, fg="blue").pack()

    liste_kutusu = tk.Listbox(pencere, width=50, height=8)
    liste_kutusu.pack(pady=10)

    pencere.mainloop()

if __name__ == "__main__":
    veritabani_kur()
    pencereyi_ac()
