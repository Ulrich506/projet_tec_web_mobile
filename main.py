from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Style sombre Bootstrap/Gemini
Window.clearcolor = get_color_from_hex('#1e1e1e')

class SecureNodeInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=[15, 10], spacing=15, **kwargs)

        # --- Zone des Logs (Maillage) ---
        # On lui donne un size_hint_y élevé pour qu'elle prenne toute la place
        self.scroll = ScrollView(size_hint=(1, 1)) 
        self.log_output = Label(
            text="[Système] Prêt. En attente de messages...\n",
            size_hint_y=None,
            halign='left',
            valign='top',
            font_size='16sp',
            color=get_color_from_hex('#d1d1d1')
        )
        self.log_output.bind(texture_size=self.log_output.setter('size'))
        self.scroll.add_widget(self.log_output)
        self.add_widget(self.scroll)

        # --- Zone de saisie (Plus grande, style Gemini) ---
        # On utilise une structure verticale pour empiler IP et Message
        input_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=160)

        # Champ IP : Plus haut et texte plus grand
        self.ip_input = TextInput(
            text='127.0.0.1', 
            multiline=False, 
            font_size='18sp',
            size_hint_y=None, height=55,
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=(1, 1, 1, 1),
            padding=[15, 15],
            hint_text="🌐 Adresse IP"
        )

        # Ligne Message + Bouton (Style Input Group)
        msg_line = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=65)
        
        self.msg_input = TextInput(
            hint_text="Écrivez votre message sécurisé...", 
            multiline=False,
            font_size='18sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=(1, 1, 1, 1),
            padding=[15, 18],
            size_hint_x=0.8
        )
        
        self.send_btn = Button(
            text="🚀", # Icône Bootstrap Style
            background_normal='',
            background_color=get_color_from_hex('#0b5ed7'), # Bleu Bootstrap Primary
            size_hint_x=0.2,
            bold=True
        )

        msg_line.add_widget(self.msg_input)
        msg_line.add_widget(self.send_btn)

        input_container.add_widget(self.ip_input)
        input_container.add_widget(msg_line)
        
        self.add_widget(input_container)

class SecureNodeApp(App):
    def build(self):
        return SecureNodeInterface()

if __name__ == "__main__":
    SecureNodeApp().run()