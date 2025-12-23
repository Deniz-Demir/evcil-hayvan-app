from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import webbrowser

# Arka plan işlemleri
try:
    from veri_islemleri import veritabani_kur, hayvan_ekle, hayvanlari_goster
    from safiye import hayvana_ozel_cozum
except ImportError:
    print("HATA: Dosyalar bulunamadı!")

Window.size = (400, 800)

# --------------------------
# KULLANICI BAZLI VERİ
# --------------------------
kullanici_db = {"admin": "Admin123"} # Örnek şifre kriterine uygun güncellendi
giris_yapan_kullanici = None

# --------------------------
# KIVY ARAYÜZÜ (KV TASARIMI)
# --------------------------
arayuz_tasarimi = '''
<SabitArkaplan@BoxLayout>:
    canvas.before:
        Color:
            rgba: 0.05, 0.05, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.2, 0.1, 0.4, 0.6
        Ellipse:
            pos: self.width * -0.3, self.height * 0.7
            size: self.width * 0.9, self.width * 0.9

ScreenManager:
    GirisEkrani:
    KayitOlEkrani:
    OturumAcEkrani:
    ListeEkrani:
    HayvanEkleEkrani:
    RaporEkrani:
    VetDestekEkrani:

<GirisEkrani>:
    name: 'ana_sayfa'
    SabitArkaplan:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        Label:
            text: ' EVCİL HAYVAN\\nTAKİP SİSTEMİ'
            font_size: 32
            bold: True
            halign: 'center'
        Button:
            text: 'YENİ ÜYELİK'
            size_hint_y: None
            height: 60
            background_color: 0.4, 0.2, 0.7, 1
            background_normal: ''
            on_press: root.manager.current = 'uye_ol'
        Button:
            text: 'GİRİŞ YAP'
            size_hint_y: None
            height: 60
            background_color: 0.1, 0.6, 0.8, 1
            background_normal: ''
            on_press: root.manager.current = 'oturum_ac'

<KayitOlEkrani>:
    name: 'uye_ol'
    SabitArkaplan:
        orientation: 'vertical'
        padding: 40
        spacing: 15
        Label:
            text: 'ÜYE KAYIT'
        TextInput:
            id: yeni_ad
            hint_text: 'Kullanıcı Adı'
            multiline: False
        TextInput:
            id: yeni_sifre
            hint_text: 'Şifre (8+ Karakter, Büyük Harf, Rakam)'
            password: True
            multiline: False
        Button:
            text: 'KAYIT OL'
            size_hint_y: None
            height: 55
            on_press: root.uye_kaydet()
        Button:
            text: '← GERİ DÖN'
            size_hint_y: None
            height: 50
            background_color: 0.7, 0.2, 0.2, 1
            background_normal: ''
            on_press: root.manager.current = 'ana_sayfa'

<OturumAcEkrani>:
    name: 'oturum_ac'
    SabitArkaplan:
        orientation: 'vertical'
        padding: 40
        spacing: 15
        Label:
            text: 'SİSTEME GİRİŞ'
        TextInput:
            id: k_ad
            hint_text: 'Kullanıcı Adı'
            multiline: False
        TextInput:
            id: k_sifre
            hint_text: 'Şifre'
            password: True
            multiline: False
        Button:
            text: 'GİRİŞ'
            size_hint_y: None
            height: 55
            on_press: root.giris_yap()
        Button:
            text: '← GERİ DÖN'
            size_hint_y: None
            height: 50
            background_color: 0.7, 0.2, 0.2, 1
            background_normal: ''
            on_press: root.manager.current = 'ana_sayfa'

<ListeEkrani>:
    name: 'liste_sayfasi'
    SabitArkaplan:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        Label:
            text: 'HAYVANLARIM'
            bold: True
            size_hint_y: None
            height: 50
        ScrollView:
            BoxLayout:
                id: hayvan_listesi
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 12
        BoxLayout:
            size_hint_y: None
            height: 60
            spacing: 10
            Button:
                text: 'HAYVAN EKLE'
                on_press: root.manager.current = 'hayvan_ekle'
            Button:
                text: 'VETERİNER'
                on_press: root.manager.current = 'vet_bilgi'
            Button:
                text: '← ÇIKIŞ'
                background_color: 0.7, 0.2, 0.2, 1
                background_normal: ''
                on_press: root.manager.current = 'ana_sayfa'

<HayvanEkleEkrani>:
    name: 'hayvan_ekle'
    SabitArkaplan:
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                padding: 20
                spacing: 8
                size_hint_y: None
                height: self.minimum_height
                Label:
                    text: 'HAYVAN BİLGİ GİRİŞİ'
                    bold: True
                TextInput:
                    id: h_ad
                    hint_text: 'Hayvan Adı'
                    size_hint_y: None
                    height: 40
                TextInput:
                    id: h_yas
                    hint_text: 'Yaş'
                    size_hint_y: None
                    height: 40
                TextInput:
                    id: h_kilo
                    hint_text: 'Kilo'
                    size_hint_y: None
                    height: 40
                TextInput:
                    id: h_boy
                    hint_text: 'Boy (cm)'
                    size_hint_y: None
                    height: 40
                TextInput:
                    id: h_mama
                    hint_text: 'Mama Markası'
                    size_hint_y: None
                    height: 40
                # 3. MADDE: MAMA TÜRÜ SORGUSU (SPINNER)
                Label:
                    text: 'Mama Türünü Seçin:'
                    size_hint_y: None
                    height: 30
                    halign: 'left'
                Spinner:
                    id: h_mama_turu
                    text: 'Seçiniz (Kuru/Yaş)'
                    values: ['Kuru', 'Yaş']
                    size_hint_y: None
                    height: 45
                TextInput:
                    id: h_gram
                    hint_text: 'Günlük Gramaj'
                    size_hint_y: None
                    height: 40
                TextInput:
                    id: h_alerji
                    hint_text: 'Alerjileri (Yoksa Yok yazın)'
                    size_hint_y: None
                    height: 40
                TextInput:
                    id: h_asi
                    hint_text: 'Aşı Bilgisi'
                    size_hint_y: None
                    height: 40
                Button:
                    text: 'VERİLERİ KAYDET'
                    size_hint_y: None
                    height: 55
                    background_color: 0.2, 0.7, 0.3, 1
                    background_normal: ''
                    on_press: root.kaydet_ve_analiz()
                Button:
                    text: '← VAZGEÇ'
                    size_hint_y: None
                    height: 45
                    background_color: 0.7, 0.2, 0.2, 1
                    background_normal: ''
                    on_press: root.manager.current = 'liste_sayfasi'

<RaporEkrani>:
    name: 'rapor_sayfasi'
    SabitArkaplan:
        orientation: 'vertical'
        padding: 20
        Label:
            text: 'ANALİZ RAPORU'
            bold: True
            size_hint_y: None
            height: 50
        ScrollView:
            Label:
                id: rapor_alani
                text: ''
                markup: True
                text_size: self.width - 20, None
                size_hint_y: None
                height: self.texture_size[1]
        Button:
            text: '← GERİ DÖN'
            size_hint_y: None
            height: 55
            on_press: root.manager.current = 'liste_sayfasi'

<VetDestekEkrani>:
    name: 'vet_bilgi'
    SabitArkaplan:
        orientation: 'vertical'
        padding: 30
        spacing: 20
        Label:
            text: 'VETERİNER BİLGİSİ'
            bold: True
            font_size: 24
        # 4. MADDE: ÜNVAN DÜZELTME VE NUMARA GİZLEME
        Label:
            text: '[b]Ali Hekim Bey[/b]\\nUzman Veteriner\\nTel: 05xx xxx xx xx'
            halign: 'center'
            font_size: 20
            markup: True
        Button:
            text: ' YAKINDAKİ VETERİNERLER'
            size_hint_y: None
            height: 65
            on_press: root.harita_ac()
        Button:
            text: '← GERİ'
            size_hint_y: None
            height: 50
            on_press: root.manager.current = 'liste_sayfasi'
'''

# --------------------------
# SCREEN SINIFLARI (MANTIK)
# --------------------------
class GirisEkrani(Screen): pass

class KayitOlEkrani(Screen):
    def uye_kaydet(self):
        ad = self.ids.yeni_ad.text.strip()
        sifre = self.ids.yeni_sifre.text.strip()
        
        # 2. MADDE: ŞİFRE ŞARTLARI
        buyuk_harf = any(c.isupper() for c in sifre)
        rakam = any(c.isdigit() for c in sifre)
        
        if len(sifre) < 8 or not buyuk_harf or not rakam:
            self.popup("Hata", "Şifre kriterlere uygun değil!\n- En az 8 karakter\n- En az 1 büyük harf\n- En az 1 rakam")
            return

        if ad in kullanici_db:
            self.popup("Hata", "Bu kullanıcı adı zaten kayıtlı!")
            return

        kullanici_db[ad] = sifre
        self.manager.current = 'oturum_ac'
        self.popup("Başarılı", "Kayıt tamamlandı! Giriş yapabilirsiniz.")

    def popup(self, baslik, mesaj):
        pop = Popup(title=baslik, content=Label(text=mesaj), size_hint=(0.8, 0.4))
        pop.open()

class OturumAcEkrani(Screen):
    def giris_yap(self):
        global giris_yapan_kullanici
        ad, sifre = self.ids.k_ad.text.strip(), self.ids.k_sifre.text.strip()
        if ad in kullanici_db and kullanici_db[ad] == sifre:
            giris_yapan_kullanici = ad 
            self.manager.current = 'liste_sayfasi'
        else:
            self.popup("Hata", "Hatalı kullanıcı adı veya şifre!")

    def popup(self, baslik, mesaj):
        pop = Popup(title=baslik, content=Label(text=mesaj), size_hint=(0.8, 0.3))
        pop.open()

class ListeEkrani(Screen):
    def on_enter(self):
        self.ids.hayvan_listesi.clear_widgets()
        # 1. MADDE: Sadece giriş yapanın hayvanları
        veriler = hayvanlari_goster(giris_yapan_kullanici)
        
        if not veriler:
            self.ids.hayvan_listesi.add_widget(Label(text="Henüz hayvan eklemediniz.", size_hint_y=None, height=40))
            return

        for h in veriler:
            btn = Button(
                text=f"🐾 {h[1].upper()} ({h[4]})",
                size_hint_y=None, height=85,
                background_color=(0.3, 0.3, 0.5, 1),
                background_normal='', bold=True
            )
            btn.bind(on_press=lambda x, h_id=h[0]: self.rapor_yukle(h_id))
            self.ids.hayvan_listesi.add_widget(btn)

    def rapor_yukle(self, h_id):
        sonuc = hayvana_ozel_cozum(h_id)
        self.manager.get_screen('rapor_sayfasi').ids.rapor_alani.text = sonuc
        self.manager.current = 'rapor_sayfasi'

class HayvanEkleEkrani(Screen):
    def kaydet_ve_analiz(self):
        mama_turu = self.ids.h_mama_turu.text
        if mama_turu == 'Seçiniz (Kuru/Yaş)':
            self.popup("Hata", "Lütfen mama türünü seçin!")
            return

        try:
            # DÜZELTİLEN KISIM: Tam olarak 15 parametre gönderiliyor
            yeni_id = hayvan_ekle(
                giris_yapan_kullanici,           # 1 (sahip_id)
                self.ids.h_ad.text,              # 2 (ad)
                int(self.ids.h_yas.text or 0),   # 3 (yas)
                float(self.ids.h_kilo.text or 0),# 4 (kilo)
                float(self.ids.h_boy.text or 0), # 5 (boy)
                "Bilinmiyor",                    # 6 (cinsiyet)
                self.ids.h_mama.text,            # 7 (mama_marka)
                mama_turu,                       # 8 (mama_tur)
                self.ids.h_gram.text,            # 9 (miktar)
                "08:00",                         # 10 (saat)
                self.ids.h_alerji.text,          # 11 (alerji)
                "Yok",                           # 12 (urun)
                "Ali Hekim",                     # 13 (vet)
                self.ids.h_asi.text,             # 14 (asi)
                "Normal"                         # 15 (durum)
            )
            self.manager.current = 'liste_sayfasi'
        except Exception as e:
            self.popup("Hata", f"Veri hatası: {str(e)}")

    def popup(self, baslik, mesaj):
        pop = Popup(title=baslik, content=Label(text=mesaj), size_hint=(0.8, 0.3))
        pop.open()

class RaporEkrani(Screen): pass

class VetDestekEkrani(Screen):
    def harita_ac(self):
        webbrowser.open("https://www.google.com/search?q=yakındaki+veterinerler")

class HayvanTakipSistemi(App):
    def build(self):
        veritabani_kur()
        return Builder.load_string(arayuz_tasarimi)

if __name__ == '__main__':
    HayvanTakipSistemi().run()
