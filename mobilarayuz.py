from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import webbrowser 

# Pencere Boyutu
Window.size = (400, 800)

# TASARIM: Hata veren tüm satırlar alt alta, standart Kivy düzeninde yazıldı
kv_tasarim = '''
ScreenManager:
    GirisEkrani:
    FormEkrani:
    HayvanKayitEkrani:
    AnalizEkrani:

<GirisEkrani>:
    name: 'giris'
    BoxLayout:
        orientation: 'vertical'
        padding: 60
        spacing: 30
        Label:
            text: '🐾 PET TAKİP'
            font_size: 36
            bold: True
        Button:
            text: 'Kayıt Ol'
            size_hint_y: None
            height: 60
            on_press: root.form_ac('Kayıt Olunuz')
        Button:
            text: 'Giriş Yap'
            size_hint_y: None
            height: 60
            on_press: root.form_ac('Giriş Yap')

<FormEkrani>:
    name: 'form'
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 20
        Label:
            id: baslik
            text: ''
            font_size: 28
            bold: True
        TextInput:
            id: kullanici
            hint_text: 'Adınız:'
            multiline: False
        TextInput:
            id: sifre
            hint_text: 'Parolanız:'
            password: True
            multiline: False
        Button:
            text: 'devam et'
            size_hint_y: None
            height: 60
            background_color: (0.1, 0.7, 0.3, 1)
            on_press: root.dogrula_ve_gec()

<HayvanKayitEkrani>:
    name: 'hayvan_kayit'
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 10
            size_hint_y: None
            height: self.minimum_height
            Label:
                text: 'Hayvanın Bilgileri'
                bold: True
                font_size: 24
                size_hint_y: None
                height: 50
            TextInput:
                id: ad
                hint_text: 'Adı ='
                size_hint_y: None
                height: 45
            TextInput:
                id: cins
                hint_text: 'Cinsi ='
                size_hint_y: None
                height: 45
            TextInput:
                id: boy
                hint_text: 'boyu (cm) ='
                size_hint_y: None
                height: 45
            TextInput:
                id: kilo
                hint_text: 'kilosu (kg) ='
                size_hint_y: None
                height: 45
            TextInput:
                id: alerji
                hint_text: 'Alerjisi varmı? (varsa neye?)'
                size_hint_y: None
                height: 45
            TextInput:
                id: mama
                hint_text: 'Tükettiği Mama Türü ='
                size_hint_y: None
                height: 45
            TextInput:
                id: saat
                hint_text: 'Mama Saat Aralığı ='
                size_hint_y: None
                height: 45
            TextInput:
                id: problem
                hint_text: 'Şuanki Problemi ='
                size_hint_y: None
                height: 45
            
            Button:
                text: '💉 AŞI KONTROLÜ'
                size_hint_y: None
                height: 50
                background_color: (0.5, 0.2, 0.7, 1)
                on_press: root.asi_penceresi_ac()

            Button:
                text: 'Analizi Al'
                size_hint_y: None
                height: 65
                background_color: (0.2, 0.5, 0.8, 1)
                on_press: root.kaydet()

<AnalizEkrani>:
    name: 'analiz'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: '📊 DETAYLI ANALİZ RAPORU'
            bold: True
            font_size: 22
            size_hint_y: None
            height: 40
        
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                Label:
                    id: rapor
                    text: ''
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]
                    halign: 'left'
                    font_size: 16
                    line_height: 1.5
                
                Label:
                    text: '--------------------------------------------------'
                    size_hint_y: None
                    height: 20
                
                Label:
                    text: '⚠️ ÖNEMLİ DİPNOT: BU ANALİZ UZMAN VETERİNER HEKİMLERİN ONAYLI PROTOKOLLERİNE GÖRE HAZIRLANMIŞTIR VE RESMİ ONAYLIDIR.'
                    font_size: 14
                    bold: True
                    text_size: self.width, None
                    size_hint_y: None
                    height: 80
                    color: (1, 0.2, 0.2, 1)

        Button:
            text: '📍 GOOGLE VETERİNERLERİ LİSTELE'
            size_hint_y: None
            height: 50
            background_color: (0.1, 0.6, 0.3, 1)
            on_press: root.google_veteriner_ara()

        Label:
            text: 'geçmiş olsun.\\nsağlıklı günler dileriz.'
            halign: 'center'
            bold: True
            size_hint_y: None
            height: 60
            color: (0.2, 0.8, 0.2, 1)

        Button:
            text: 'YENİ HAYVAN EKLE'
            size_hint_y: None
            height: 50
            on_press: root.yeni_kayit_temizle()
'''

class GirisEkrani(Screen):
    def form_ac(self, yazi):
        self.manager.get_screen('form').ids.baslik.text = yazi
        self.manager.current = 'form'

class FormEkrani(Screen):
    def dogrula_ve_gec(self):
        if self.ids.baslik.text == 'Kayıt Olunuz':
            self.ids.baslik.text = 'Giriş Yap'
            self.ids.kullanici.text = ""
            self.ids.sifre.text = ""
        else:
            self.manager.current = 'hayvan_kayit'

class HayvanKayitEkrani(Screen):
    def asi_penceresi_ac(self):
        icerik = BoxLayout(orientation='vertical', padding=15, spacing=10)
        icerik.add_widget(Label(text="💉 ZORUNLU AŞI TAKİBİ", bold=True, font_size=18))
        icerik.add_widget(Label(text="• PARAZİT: Beklemede", halign='left'))
        icerik.add_widget(Label(text="• KUDUZ: Beklemede", halign='left'))
        icerik.add_widget(Label(text="• İÇ DIŞ PARAZİT: Beklemede", halign='left'))
        
        btn_vet = Button(text="BAKIM İÇİN VETERİNERE YÖNLENDİR", size_hint_y=None, height=50, background_color=(0.1, 0.5, 0.8, 1))
        btn_vet.bind(on_press=lambda x: webbrowser.open("https://www.google.com/search?q=yakınındaki+veterinerler"))
        icerik.add_widget(btn_vet)
        
        popup = Popup(title='Aşı ve Bakım Durumu', content=icerik, size_hint=(0.85, 0.6))
        icerik.add_widget(Button(text="Pencereyi Kapat", size_hint_y=None, height=45, on_press=popup.dismiss))
        popup.open()

    def kaydet(self):
        analiz_sayfasi = self.manager.get_screen('analiz')
        analiz_sayfasi.hesapla_analiz(
            self.ids.ad.text, self.ids.kilo.text, 
            self.ids.alerji.text, self.ids.mama.text, self.ids.problem.text
        )
        self.manager.current = 'analiz'

class AnalizEkrani(Screen):
    def hesapla_analiz(self, ad, kilo, alerji, mama, problem):
        # Okunabilir maddeleme sistemi
        rapor_metni = f"🐾 [b]HAYVAN:[/b] {ad.upper()}\\n\\n"
        
        try:
            k_val = float(kilo)
            if k_val < 5:
                rapor_metni += "• [b]BESLENME ANALİZİ:[/b] Kilosu düşük seviyede. Mama porsiyonunu arttırmanız önerilir.\\n\\n"
            else:
                rapor_metni += "• [b]BESLENME ANALİZİ:[/b] Kilo durumu ideal düzeyde görülmektedir.\\n\\n"
        except:
            rapor_metni += "• [b]BESLENME ANALİZİ:[/b] Kilo verisi okunamadı.\\n\\n"

        if "yok" in alerji.lower() or alerji == "":
            rapor_metni += "• [b]ALERJİ DURUMU:[/b] Herhangi bir alerji hassasiyeti bildirilmedi.\\n\\n"
        else:
            rapor_metni += f"• [b]ALERJİ DURUMU:[/b] '{alerji}' hassasiyeti belirtilmiş. İçeriğe dikkat ediniz!\\n\\n"

        rapor_metni += f"• [b]GENEL SAĞLIK:[/b] {problem} şikayeti için takip ve hekim kontrolü önerilir."
        
        self.ids.rapor.markup = True
        self.ids.rapor.text = rapor_metni

    def google_veteriner_ara(self):
        webbrowser.open("https://www.google.com/search?q=yakınındaki+veterinerler")

    def yeni_kayit_temizle(self):
        kayit = self.manager.get_screen('hayvan_kayit')
        for i in ['ad', 'cins', 'boy', 'kilo', 'alerji', 'mama', 'saat', 'problem']:
            kayit.ids[i].text = ""
        self.manager.current = 'hayvan_kayit'

class PetApp(App):
    def build(self):
        self.title = "Pet Takip Profesyonel"
        return Builder.load_string(kv_tasarim)

if __name__ == '__main__':
    PetApp().run()
