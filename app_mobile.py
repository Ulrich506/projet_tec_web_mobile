from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from cryptography.fernet import Fernet
import socket
import threading

# Réglage spécial pour le clavier Android
Window.softinput_mode = "resize"

KEY = b'PtiW1Y8fYyJrPg8M3fqIMeYZVzp_U-u691LGKDRjCLE='
cipher = Fernet(KEY)

class SecureNodeApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1)
        self.root = BoxLayout(orientation='vertical', padding=10)

        # Header fixe
        self.header = Label(
            text="[b]SECURE NODE V1[/b]", markup=True,
            size_hint_y=None, height=50, color=(0, 1, 0.6, 1)
        )

        # Console d'affichage
        self.scroll = ScrollView(size_hint_y=1)
        self.log = Label(
            text="> Tunnel chiffré prêt...", markup=True,
            halign='left', valign='top', size_hint_y=None
        )
        self.log.bind(texture_size=self.log.setter('size'))
        self.scroll.add_widget(self.log)

        # Barre de saisie (Message + Bouton)
        self.input_area = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=5)
        self.msg_input = TextInput(
            hint_text="Message...", multiline=False,
            background_color=(0.15, 0.15, 0.15, 1), foreground_color=(1, 1, 1, 1)
        )
        self.send_btn = Button(text=">", size_hint_x=None, width=70, background_color=(0, 0.6, 0.4, 1))
        self.send_btn.bind(on_press=self.send_msg)

        self.input_area.add_widget(self.msg_input)
        self.input_area.add_widget(self.send_btn)

        self.root.add_widget(self.header)
        self.root.add_widget(self.scroll)
        self.root.add_widget(self.input_area)

        # Configuration Réseau
        self.pc_ip = "192.168.0.101" # À MODIFIER SELON TON PC
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind(('0.0.0.0', 5005))
            threading.Thread(target=self.recv_thread, daemon=True).start()
        except: pass

        return self.root

    def recv_thread(self):
        while True:
            try:
                data, _ = self.sock.recvfrom(1024)
                msg = cipher.decrypt(data).decode()
                Clock.schedule_once(lambda dt: self.add_log(f"[color=00ffff]<< {msg}[/color]"))
            except: pass

    def add_log(self, text):
        self.log.text += f"\n{text}"
        self.log.text_size = (self.scroll.width - 20, None)
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0))

    def send_msg(self, instance):
        if self.msg_input.text:
            try:
                token = cipher.encrypt(self.msg_input.text.encode())
                self.sock.sendto(token, (self.pc_ip, 5001))
                self.add_log(f">> {self.msg_input.text}")
                self.msg_input.text = ""
            except: pass

if __name__ == '__main__':
    SecureNodeApp().run()