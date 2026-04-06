from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import webbrowser

# Arka plan işlemleri
try:
    from veri_islemleri import veritabani_kur, hayvan_ekle, hayvanlari_goster, kullanici_ekle, kullanici_kontrol
    from safiye import hayvana_ozel_cozum
except ImportError:
    print("HATA: Gerekli Python dosyaları bulunamadı!")

Window.size = (400, 800)

giris_yapan_kullanici = None

# --- KV TASARIMI ---
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
            on_press: 
                app.root.get_screen('oturum_ac').giris_alanlarini_temizle()
                root.manager.current = 'oturum_ac'

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
            text: ' GERİ DÖN'
            size_hint_y: None
            height: 50
            background_color: 0.7, 0.2, 0.2, 1
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
            text: ' GERİ DÖN'
            size_hint_y: None
            height: 50
            background_color: 0.7, 0.2, 0.2, 1
            on_press: root.manager.current = 'ana_sayfa'

<ListeEkrani>:
    name: 'liste_sayfasi'
    SabitArkaplan:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        Label:
            text: ' HAYVANLARIM'
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
                on_press: 
                    app.root.get_screen('hayvan_ekle').alanlari_temizle()
                    root.manager.current = 'hayvan_ekle'
            Button:
                text: 'VETERİNER'
                on_press: root.manager.current = 'vet_bilgi'
            Button:
                text: '← ÇIKIŞ'
                background_color: 0.7, 0.2, 0.2, 1
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
                    multiline: False
                TextInput:
                    id: h_yas
                    hint_text: 'Yaş'
                    size_hint_y: None
                    height: 40
                    multiline: False
                TextInput:
                    id: h_kilo
                    hint_text: 'Kilo'
                    size_hint_y: None
                    height: 40
                    multiline: False
                TextInput:
                    id: h_boy
                    hint_text: 'Boy (cm)'
                    size_hint_y: None
                    height: 40
                    multiline: False
                TextInput:
                    id: h_cinsiyet
                    hint_text: 'Cinsiyet (Erkek/Dişi)'
                    size_hint_y: None
                    height: 40
                    multiline: False
                TextInput:
                    id: h_mama
                    hint_text: 'Mama Markası'
                    size_hint_y: None
                    height: 40
                    multiline: False
                Spinner:
                    id: h_mama_turu
                    text: 'Mama Türü (Kuru/Yaş)'
                    values: ['Kuru', 'Yaş']
                    size_hint_y: None
                    height: 45
                TextInput:
                    id: h_gram
                    hint_text: 'Günlük Gramaj'
                    size_hint_y: None
                    height: 40
                    multiline: False
                TextInput:
                    id: h_saat
                    hint_text: 'Beslenme Saati (Örn: 08:30)'
                    size_hint_y: None
                    height: 40
                    multiline: False
                TextInput:
                    id: h_alerji
                    hint_text: 'Alerjileri (Yoksa Yok yazın)'
                    size_hint_y: None
                    height: 40
                    multiline: False
                TextInput:
                    id: h_asi
                    hint_text: 'Aşı Bilgisi (Örn: Kuduz-Yapıldı)'
                    size_hint_y: None
                    height: 40
                    multiline: False
                Button:
                    text: 'VERİLERİ KAYDET VE ANALİZ ET'
                    size_hint_y: None
                    height: 55
                    background_color: 0.2, 0.7, 0.3, 1
                    on_press: root.kaydet_ve_analiz()
                Button:
                    text: ' VAZGEÇ'
                    size_hint_y: None
                    height: 45
                    background_color: 0.7, 0.2, 0.2, 1
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
        Button:
            text: 'GERİ DÖN'
            size_hint_y: None
            height: 55
            background_color: 0.7, 0.2, 0.2, 1
            on_press: root.manager.current = 'liste_sayfasi'

<VetDestekEkrani>:
    name: 'vet_bilgi'
    SabitArkaplan:
        orientation: 'vertical'
        padding: 30
        spacing: 20
        RelativeLayout:
            size_hint_y: None
            height: 50
            Label:
                text: ' UZMAN VETERİNER'
                bold: True
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            Button:
                text: 'KOMİK \\nVİDEOLAR'
                size_hint: None, None
                size: 100, 50
                pos_hint: {'right': 1, 'top': 1}
                font_size: 12
                background_color: 0.1, 0.6, 0.8, 1
                on_press: root.videolari_goster()
        Label:
            text: 'Ali Hekim Bey\\n Uzman Veteriner Hekim\\nTel: 05xx xxx xx xx'
            halign: 'center'
            font_size: 20
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

# --- PYTHON SINIFLARI ---

class GirisEkrani(Screen): pass

class KayitOlEkrani(Screen):
    def uye_kaydet(self):
        ad, sifre = self.ids.yeni_ad.text.strip(), self.ids.yeni_sifre.text.strip()
        if not ad or not sifre:
            self.pencere("Hata", "Alanlar boş bırakılamaz!")
            return
        if len(sifre) < 8 or not any(c.isupper() for c in sifre) or not any(c.isdigit() for c in sifre):
            self.pencere("Hata", "Şifre kriterlere uygun değil!")
            return
        
        if kullanici_ekle(ad, sifre):
            self.pencere("Başarılı", "Kayıt tamamlandı.")
            self.manager.current = 'oturum_ac'
        else:
            self.pencere("Hata", "Kullanıcı adı alınmış!")

    def pencere(self, baslik, mesaj):
        Popup(title=baslik, content=Label(text=mesaj), size_hint=(0.8, 0.4)).open()

class OturumAcEkrani(Screen):
    def giris_alanlarini_temizle(self):
        self.ids.k_ad.text = ""
        self.ids.k_sifre.text = ""

    def giris_yap(self):
        global giris_yapan_kullanici
        ad, sifre = self.ids.k_ad.text.strip(), self.ids.k_sifre.text.strip()
        if kullanici_kontrol(ad, sifre):
            giris_yapan_kullanici = ad 
            self.manager.current = 'liste_sayfasi'
        else:
            Popup(title="Hata", content=Label(text="Hatalı giriş!"), size_hint=(0.8, 0.4)).open()

class ListeEkrani(Screen):
    def on_enter(self):
        self.ids.hayvan_listesi.clear_widgets()
        veriler = hayvanlari_goster(giris_yapan_kullanici)
        for h in veriler:
            btn = Button(text=f" {h[1].upper()} ({h[4]})", size_hint_y=None, height=85)
            btn.bind(on_press=lambda x, h_id=h[0]: self.raporu_getir(h_id))
            self.ids.hayvan_listesi.add_widget(btn)

    def raporu_getir(self, h_id):
        sonuc = hayvana_ozel_cozum(h_id)
        self.manager.get_screen('rapor_sayfasi').ids.rapor_alani.text = sonuc
        self.manager.current = 'rapor_sayfasi'

class HayvanEkleEkrani(Screen):
    def alanlari_temizle(self):
        for key in self.ids: self.ids[key].text = ""

    def kaydet_ve_analiz(self):
        try:
            if not self.ids.h_ad.text: return
            yeni_id = hayvan_ekle(
                giris_yapan_kullanici, self.ids.h_ad.text,
                int(self.ids.h_yas.text or 0), float(self.ids.h_kilo.text or 0),
                float(self.ids.h_boy.text or 0), self.ids.h_cinsiyet.text,
                self.ids.h_mama.text, self.ids.h_mama_turu.text,
                self.ids.h_gram.text, self.ids.h_saat.text,
                self.ids.h_alerji.text, "Cins", "Ali Hekim",
                self.ids.h_asi.text, "Normal"
            )
            self.manager.get_screen('rapor_sayfasi').ids.rapor_alani.text = hayvana_ozel_cozum(yeni_id)
            self.manager.current = 'rapor_sayfasi'
        except Exception as e: print(f"Hata: {e}")

class RaporEkrani(Screen): pass

class VetDestekEkrani(Screen):
    def harita_ac(self):
        webbrowser.open("https://www.google.com/search?q=yakındaki+veterinerler")

    def videolari_goster(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="KOMİK VİDEOLAR (24+ Saat Ekran Süresi)", bold=True, size_hint_y=None, height=40))
        
        btn1 = Button(text="Video 1: veteriner ali hekim bey", size_hint_y=None, height=50)
        btn1.bind(on_press=lambda x: webbrowser.open("https://www.youtube.com/shorts/NppxX55dphQ?feature=share"))
        
        btn2 = Button(text="Video 2: hanimisiguttimottişim", size_hint_y=None, height=50)
        btn2.bind(on_press=lambda x: webbrowser.open("https://www.youtube.com/shorts/7Pr3cuOuSss?feature=share"))
        
        content.add_widget(btn1)
        content.add_widget(btn2)
        
        popup = Popup(title="HAYVAN NEŞESİ", content=content, size_hint=(0.8, 0.5))
        close_btn = Button(text="Kapat", size_hint_y=None, height=45)
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

class HayvanTakipSistemi(App):
    def build(self):
        veritabani_kur()
        return Builder.load_string(arayuz_tasarimi)

if __name__ == '__main__':
    HayvanTakipSistemi().run()
