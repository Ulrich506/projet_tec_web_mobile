import hashlib
import time
import socket
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty

Window.softinput_mode = 'resize'

KV = '''
<MessageBubble>:
    orientation: "vertical"
    padding: "12dp"
    size_hint_x: 0.8
    size_hint_y: None
    height: self.minimum_height
    radius: [15, 15, 15, 2] if root.side == "left" else [15, 15, 2, 15]
    md_bg_color: get_color_from_hex("#1e293b") if root.side == "left" else get_color_from_hex("#005236")
    line_color: get_color_from_hex("#4cd7f6") if root.side == "left" else get_color_from_hex("#4edea3")
    line_width: 1
    pos_hint: {"left": 1} if root.side == "left" else {"right": 1}

    MDLabel:
        text: root.sender_id
        font_style: "Caption"
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#4cd7f6") if root.side == "left" else get_color_from_hex("#4edea3")
        size_hint_y: None
        height: self.texture_size[1]
        bold: True

    MDLabel:
        text: root.message_text
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: root.hash_val
        font_style: "Overline"
        theme_text_color: "Hint"
        size_hint_y: None
        height: self.texture_size[1]

MDScreen:
    md_bg_color: get_color_from_hex("#0e1511")

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "TEC WEB MOBIL - Terminal"
            anchor_title: "left"
            md_bg_color: get_color_from_hex("#0e1511")
            elevation: 0
            specific_text_color: get_color_from_hex("#4edea3")

        MDBoxLayout:
            orientation: 'vertical'
            
            ScrollView:
                do_scroll_x: False
                MDBoxLayout:
                    id: chat_logs
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "15dp"
                    spacing: "15dp"

            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: "130dp"
                padding: "10dp"
                spacing: "8dp"
                md_bg_color: get_color_from_hex("#1a211d")

                MDTextField:
                    id: ip_address
                    hint_text: "IP PC Destination"
                    mode: "fill"
                    fill_color_normal: get_color_from_hex("#09100c")
                    size_hint_y: None
                    height: "40dp"
                    text_color_normal: 1, 1, 1, 1

                MDBoxLayout:
                    spacing: "10dp"
                    MDTextField:
                        id: msg_input
                        hint_text: "Entrer message..."
                        mode: "fill"
                        fill_color_normal: get_color_from_hex("#09100c")
                        text_color_normal: 1, 1, 1, 1

                    MDIconButton:
                        icon: "send"
                        md_bg_color: get_color_from_hex("#4edea3")
                        theme_text_color: "Custom"
                        text_color: 0, 0, 0, 1
                        on_release: app.send_message()
'''

class MessageBubble(MDCard):
    sender_id = StringProperty()
    message_text = StringProperty()
    hash_val = StringProperty()
    side = StringProperty()

    def __init__(self, sender_id, message_text, hash_val, side="left", **kwargs):
        super().__init__(**kwargs)
        self.sender_id = sender_id
        self.message_text = message_text
        self.hash_val = f"SHA256: {hash_val[:16]}..."
        self.side = side

class SecureNodeApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def send_message(self):
        ip_dest = self.root.ids.ip_address.text.strip()
        msg = self.root.ids.msg_input.text.strip()
        port = 5001 
        
        if msg != "" and ip_dest != "":
            h = hashlib.sha256(msg.encode()).hexdigest()
            
            # --- LOGIQUE RÉSEAU CORRIGÉE ---
            try:
                # On utilise UDP (SOCK_DGRAM) pour éviter les blocages de connexion
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2) # Évite que l'APK freeze si le réseau est lent
                sock.sendto(msg.encode('utf-8'), (ip_dest, port))
                sock.close()
                
                # Affichage si succès
                new_msg = MessageBubble(sender_id=f"VERS: {ip_dest}", message_text=msg, hash_val=h, side="right")
                self.root.ids.chat_logs.add_widget(new_msg)
                self.root.ids.msg_input.text = ""
            except Exception as e:
                # En cas d'erreur (IP mal tapée ou réseau coupé)
                error_msg = MessageBubble(sender_id="ERREUR RÉSEAU", message_text=str(e), hash_val="FAILED", side="left")
                self.root.ids.chat_logs.add_widget(error_msg)

if __name__ == "__main__":
    SecureNodeApp().run()