# denızden hayvan verilerini kullanarak akıllı öneri ve takip sistemleri sunmak
#Hayvanın yaş ve kilosuna görekullanılacak sabit mama önerilerini tutmak
#denizden alınma verıkatmanı

from veri_katmani import( veritabani_kur, hayvan_ekle,hayvanlari_goster)
mama_veritabani=[
    {"yas": "yavru", "kilo": "kucuk", "mama": "Yavru Mini Mama", "miktar": "Günde 3 öğün"},
    {"yas": "yavru", "kilo": "orta", "mama": "Yavru Orta Irk Mama", "miktar": "Günde 2 öğün"},
    {"yas": "yavru", "kilo": "buyuk", "mama": "Yavru Büyük Irk Mama", "miktar": "Günde 2 öğün"},
    {"yas": "yetiskin", "kilo": "kucuk", "mama": "Adult Mini", "miktar": "Günde 2 öğün"},
    {"yas": "yetiskin", "kilo": "orta", "mama": "Adult Orta Irk", "miktar": "Günde 2 öğün"},
    {"yas": "yetiskin", "kilo": "buyuk", "mama": "Adult Büyük Irk", "miktar": "Günde 1-2 öğün"}
]
asi_kayitlari={}
#yasına ve kılosuna uygun mam ve mıktarını onerıcek 
oneriler=()
hayvan_bilgisi=()
def  mama_onerisi(hayvan_bilgisi):
    for mama in mama_veritabani:    ##Hayvanın yaşı ve kilosuna uygun mama var mı diye,
        if(
            mama["yas"]==hayvan_bilgisi["yas"] and mama ["kilo"]== hayvan_bilgisi["kilo"]
        ):
            return{
                "onerilen_mama":mama["mama"],"miktar":mama["miktar"],"alerji":hayvan_bilgisi["alerji"]

            }
    return "uygun hayvan bulunamadı"
oneriler=mama_onerisi(hayvan_bilgisi)
print("mama önerisi : ", oneriler)

#bir hayvana yeni aşı kaydı eklemek yada kayıtlı hayvana
#kmlik numarası ,ad ,tarih 

def asi_ekle(hayvan_id,asi_adi,tarih):
    if hayvan_id not in asi_kayitlari:
        asi_kayitlari[hayvan_id]=[]
    asi_kayitlari[hayvan_id].append({
        "asi": asi_adi,
        "tarih":tarih
    })
#hayvanın  tüm aşı geçmişini görüntülemek için 

def asi_listele(hayvan_id):
    return asi_kayitlari.get(hayvan_id,"Bu hayvan için kayıtlı aşı bulunmamaktadır.")

#kullanıcının arayüzünde gösterilecek hatırlatma mesajı 
def hatirlatma_oluştur(tur,mesaj):
    return  {"hatırlatma_turu":tur,"mesaj":mesaj}


if __name__=="__main__":
    veritabani_kur()

#### Denizden alınan 13 tane hayvan ekleme
hayvan_ekle ("Pamuk","yavru","orta","disi",
             "erkek","yok","","Vetenıer Ali",
             "günlük yürüyüş",
            "kuduz","sağlıklı","sağlıksız",
            "hayır"
            )
hayvanlar=hayvanlari_goster()

for i in hayvanlar:
    hayvan_id=i[0]
    yas=i[2]
    kilo=i[3]
    hayvan_bilgisi={
        "yas":yas,
        "kilo":kilo,
        "alerji":"yok"
    }
asi_ekle("H001", "Kuduz", "12.05.2025")
asi_ekle("H001", "Parazit", "20.06.2025")

def hatirlatma_olustur(tur, mesaj):
    return f"{tur.upper()} HATIRLATMASI → {mesaj}"      #tur.upper "mama" "MAMA" yapar,return bu metni geri döndürür


#hatırlatmanın sabah oglen ve aksam ıcın 
zaman_mesajlari = {
    "sabah": "Sabah",
    "ogle": "Öğle",
    "aksam": "Akşam"
}

def hatirlatma_olustur(tur, zaman, mesaj):
    zaman = zaman.lower()

    if zaman not in zaman_mesajlari:
        return "Geçersiz zaman seçimi"

    return f"{zaman_mesajlari[zaman]} {tur.upper()} HATIRLATMASI : {mesaj}"

hatirlatma=[]#bos lıste ıcın 
def hatirlatma_ekle(tur, zaman, mesaj):
    hatirlatma = hatirlatma_olustur(tur, zaman, mesaj)
    hatirlatma.append(hatirlatma_ekle)

def gunluk_hatirlatma_olustur():
    pass

gunluk_hatirlatma_olustur(
    "mama",
    {
        "sabah": "Kuru mama ver",
        "ogle": "Su kabını kontrol et",
        "aksam": "Yaş mama ver"
    }
)


print("Aşı Kayıtları:", asi_listele("H001"))
print("Hatırlatma:", hatirlatma_olustur("mama", "Akşam mama saati")) #cıkdısı

# Aşı,randevu ve özel notları ve  tkınter kednı kutuphanesınden kıvy desteklı
import tkinter as tk
def listeyi_guncelle():       #fonksiypnu tanımlamak ıcın bos beklemesı ıcın pass yazmadan uyarı verıyor.
    pass


#girilen bilgileri saklamak için de
randevular=[]
notlar=[]


not_ekle = tk.Entry()
not_ekle.pack()

#aşı ile vetenierin bilgisini listeye klemek için boşda durankları 
def randevu_ekle():
    randevu=randevu_ekle.get()
    if randevu:   #Arayüzdeki randevu yazı kutusunun içindeki 
        randevular.append(randevu)  #listeye ekleyıp guncellemek ıcınde alttakı 
        listeyi_güncelle()
        randevu_ekle.delete(0,tk.END) #Yazı kutusunu temizliyor

#  Özel durumu not olarak eklemek
def not_ekle():
    not_metni = not_ekle.get()
    if not_metni:
        notlar.append(not_metni)
        listeyi_guncelle()
        not_ekle.delete(0, tk.END)
#ekrandaki  listeyi guncel tutmak içinde lısteyı guncelle kullanıp yazıları sılıcek kutunun ıcınden 

def liste_kutusu():
    pass

def listeyi_guncelle():
    liste_kutusu.delete(0,tk.END) #0ın baslangıc tk.END  listenin son satırı,tüm eski yazıları siliyor

    liste_kutusu.insert(tk.END, "Aşı / Veteriner Randevuları:")
    for j in randevular:
        liste_kutusu.insert(tk.END, "- " + j)
    liste_kutusu.insert(tk.END, "")
    liste_kutusu.insert(tk.END, "Özel Notlar:")

    for k in notlar:
        liste_kutusu.insert(tk.END, "- " + k)
# Listenin içeriğini sıfırlayıp randevu ve notları başlıklarıyla birlikte yeniden eklemek için de arayuze pencere ekledık8
 #arayüz gemını yardımıyla
pencere = tk.Tk()                                                    #tek bir ana penceresi
pencere.title("Hayvan Takip Sistemi - safiye")                       #sayfanın baslıgı
pencere.geometry("400x400")                                         #genişliği 400 yüksekliğini 400 kare şeklinde yanı

tk.Label(pencere, text="Aşı / Veteriner Randevusu").pack()           #Kullanıcıya ne girmesi gerektiğini söyler .pack()  pencereye yerleştir
randevu_entry = tk.Entry(pencere, width=40)
randevu_entry.pack()
tk.Button(pencere, text="Randevu Ekle", command=randevu_ekle).pack(pady=5)          #buton seklinse olucak,butona basılınca bu fonksiyonunu çagırır command
#pack payd baslıgına bır bosluk ekler
  
tk.Label(pencere, text="Özel Not").pack()
not_ekle = tk.Entry(pencere, width=40)
not_ekle.pack()

tk.Button(pencere, text="Not Ekle", command=not_ekle).pack(pady=5)

liste_kutusu = tk.Listbox(pencere, width=50, height=12)
liste_kutusu.pack(pady=10)
#uygulamaıcın
pencere.mainloop()
