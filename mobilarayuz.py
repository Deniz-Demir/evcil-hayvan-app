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

kullanici_db = {"admin": "Admin123"} 
giris_yapan_kullanici = None

# KV 
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
            text: '📋 HAYVANLARIM'
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
                    size_hint_y: None
                    height: 40
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
                    id: h_cins
                    hint_text: 'Hayvanın Cinsi'
                    size_hint_y: None
                    height: 40
                TextInput:
                    id: h_mama
                    hint_text: 'Mama Markası'
                    size_hint_y: None
                    height: 40
                Label:
                    text: 'Mama Türünü Seçin:'
                    size_hint_y: None
                    height: 30
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
                    hint_text: 'Aşı Bilgisi (Örn: Kuduz-Yapıldı)'
                    size_hint_y: None
                    height: 40
                Button:
                    text: 'VERİLERİ KAYDET VE ANALİZ ET'
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
            text: ' SAĞLIK RAPORU'
            bold: True
            size_hint_y: None
            height: 50
        ScrollView:
            Label:
                id: rapor_alani
                text: 'Analiz yükleniyor...'
                markup: True
                text_size: self.width - 20, None
                size_hint_y: None
                height: self.texture_size[1]
                color: 1, 1, 1, 1
        Button:
            text: '← LİSTEYE GERİ DÖN'
            size_hint_y: None
            height: 55
            background_normal: ''
            on_press: root.manager.current = 'liste_sayfasi'

<VetDestekEkrani>:
    name: 'vet_bilgi'
    SabitArkaplan:
        orientation: 'vertical'
        padding: 30
        spacing: 20
        Label:
            text: ' UZMAN VETERİNER'
            bold: True
        Label:
            text: 'Ali Hekim Bey\\nUzman Veteriner Hekim\\nTel: 05xx xxx xx xx'
            halign: 'center'
            font_size: 20
            markup: True
        Button:
            text: ' YAKINDAKİ VETERİNERLER (MAPS)'
            size_hint_y: None
            height: 65
            on_press: root.harita_ac()
        Button:
            text: '← GERİ'
            size_hint_y: None
            height: 50
            on_press: root.manager.current = 'liste_sayfasi'
'''

class GirisEkrani(Screen): pass

class KayitOlEkrani(Screen):
    def uye_kaydet(self):
        ad, sifre = self.ids.yeni_ad.text.strip(), self.ids.yeni_sifre.text.strip()
        if len(sifre) < 8 or not any(c.isupper() for c in sifre) or not any(c.isdigit() for c in sifre):
            self.pencere("Hata", "Şifre kriterlere uygun değil!")
            return
        kullanici_db[ad] = sifre
        self.manager.current = 'oturum_ac'

    def pencere(self, baslik, mesaj):
        Popup(title=baslik, content=Label(text=mesaj), size_hint=(0.8, 0.4)).open()

class OturumAcEkrani(Screen):
    def giris_yap(self):
        global giris_yapan_kullanici
        ad, sifre = self.ids.k_ad.text.strip(), self.ids.k_sifre.text.strip()
        if ad in kullanici_db and kullanici_db[ad] == sifre:
            giris_yapan_kullanici = ad 
            self.manager.current = 'liste_sayfasi'

class ListeEkrani(Screen):
    def on_enter(self):
        self.ids.hayvan_listesi.clear_widgets()
        veriler = hayvanlari_goster(giris_yapan_kullanici)
        for h in veriler:
            btn = Button(
                text=f"🐾 {h[1].upper()} ({h[4]})",
                size_hint_y=None, height=85,
                background_color=(0.3, 0.3, 0.5, 1),
                background_normal='', color=(1, 1, 1, 1), bold=True
            )
            btn.bind(on_press=lambda x, h_id=h[0]: self.raporu_getir(h_id))
            self.ids.hayvan_listesi.add_widget(btn)

    def raporu_getir(self, h_id):
        sonuc = hayvana_ozel_cozum(h_id)
        self.manager.get_screen('rapor_sayfasi').ids.rapor_alani.text = sonuc
        self.manager.current = 'rapor_sayfasi'

class HayvanEkleEkrani(Screen):
    def kaydet_ve_analiz(self):
        try:
            # Aşı bilgisini (h_asi) doğrudan veritabanına ve analiz motoruna gönderiyoruz
            yeni_id = hayvan_ekle(
                giris_yapan_kullanici,
                self.ids.h_ad.text,
                int(self.ids.h_yas.text or 0),
                float(self.ids.h_kilo.text or 0),
                float(self.ids.h_boy.text or 0),
                self.ids.h_cins.text,
                self.ids.h_mama.text,
                self.ids.h_mama_turu.text,
                self.ids.h_gram.text,
                "08:00",
                self.ids.h_alerji.text,
                "Yok",
                "Ali Hekim",
                self.ids.h_asi.text, # AŞI VERİSİ BURADA AKTARILIYOR
                "Normal"
            )
            # Rapor sayfasına veriyi yükle ve geçiş yap
            rapor = hayvana_ozel_cozum(yeni_id)
            self.manager.get_screen('rapor_sayfasi').ids.rapor_alani.text = rapor
            self.manager.current = 'rapor_sayfasi'
        except Exception as e:
            print(f"Hata: {e}")

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
