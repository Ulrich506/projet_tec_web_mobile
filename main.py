from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# --- CONFIGURATION CLAVIER ---
# 'resize' force toute l'appli à remonter pour laisser la place au clavier
Window.softinput_mode = 'resize'
Window.clearcolor = get_color_from_hex('#1e1e1e')

class SecureNodeInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=[10, 10], spacing=10, **kwargs)

        # Zone de log (prend tout l'espace restant)
        self.scroll = ScrollView(size_hint=(1, 1)) 
        self.log_output = Label(
            text="[Système] Prêt...\n",
            size_hint_y=None,
            halign='left',
            valign='top',
            font_size='16sp'
        )
        self.log_output.bind(texture_size=self.log_output.setter('size'))
        self.scroll.add_widget(self.log_output)
        self.add_widget(self.scroll)

        # --- CONTAINER INPUT (Style Gemini) ---
        # On agrandit la zone pour que ce soit bien visible
        input_area = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None, height=140)

        self.ip_input = TextInput(
            text='127.0.0.1', 
            size_hint_y=None, height=55,
            font_size='18sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 15]
        )

        msg_line = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height=65)
        
        self.msg_input = TextInput(
            hint_text="Message sécurisé...",
            font_size='18sp',
            background_color=get_color_from_hex('#2d2d2d'),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 18],
            size_hint_x=0.8
        )
        
        self.send_btn = Button(
            text="🚀",
            background_normal='',
            background_color=get_color_from_hex('#0b5ed7'),
            size_hint_x=0.2,
            bold=True
        )

        msg_line.add_widget(self.msg_input)
        msg_line.add_widget(self.send_btn)

        input_area.add_widget(self.ip_input)
        input_area.add_widget(msg_line)
        
        self.add_widget(input_area)

class SecureNodeApp(App):
    def build(self):
        return SecureNodeInterface()

if __name__ == "__main__":
    SecureNodeApp().run()