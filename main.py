from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Background sombre (Bootstrap Dark Mode)
Window.clearcolor = get_color_from_hex('#212529')

class SecureNodeInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        # Header
        self.add_widget(Label(
            text="SECURE NODE",
            font_size='26sp',
            bold=True,
            color=get_color_from_hex('#f8f9fa'), # White
            size_hint_y=None, height=60
        ))

        # Zone de logs (Simulée ici par un Label dans un ScrollView)
        self.log_area = Label(
            text="[System] Initializing AES-256...\n[Network] Listening on port 5001...",
            halign='left', valign='top',
            color=get_color_from_hex('#adb5bd') # Gray
        )
        self.add_widget(self.log_area)

        # IP Input
        self.ip_input = TextInput(
            text="127.0.0.1", multiline=False,
            size_hint_y=None, height=50,
            background_color=get_color_from_hex('#343a40'),
            foreground_color=(1, 1, 1, 1),
            padding=[10, 10]
        )
        self.add_widget(self.ip_input)

        # Ligne Message + Bouton (Bootstrap Input Group)
        input_group = BoxLayout(orientation='horizontal', spacing=0, size_hint_y=None, height=55)
        
        self.msg_input = TextInput(
            hint_text="Type message...",
            multiline=False,
            background_color=get_color_from_hex('#343a40'),
            foreground_color=(1, 1, 1, 1),
            size_hint_x=0.8
        )
        
        # Le bouton "Bootstrap Success"
        self.send_btn = Button(
            text="Send",
            background_normal='',
            background_color=get_color_from_hex('#198754'), # Bootstrap Success Green
            size_hint_x=0.2,
            bold=True
        )
        
        input_group.add_widget(self.msg_input)
        input_group.add_widget(self.send_btn)
        self.add_widget(input_group)

class SecureNodeApp(App):
    def build(self):
        return SecureNodeInterface()

if __name__ == "__main__":
    SecureNodeApp().run()