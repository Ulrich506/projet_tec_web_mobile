import hashlib
from datetime import datetime
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.utils import get_color_from_hex

# Configuration de la fenêtre (simulation mobile)
Window.size = (360, 640)
Window.softinput_mode = 'resize'

# --- INTERFACE EN LANGAGE KV (Design MeshGuard) ---
KV = '''
<MessageBubble>:
    orientation: "vertical"
    padding: "12dp"
    size_hint_x: 0.8
    radius: [15, 15, 15, 0] if self.side == "left" else [15, 15, 0, 15]
    md_bg_color: get_color_from_hex("#1e293b") if self.side == "left" else get_color_from_hex("#0f172a")
    line_color: get_color_from_hex("#4cd7f6") if self.side == "left" else get_color_from_hex("#4edea3")
    pos_hint: {"left": 1} if self.side == "left" else {"right": 1}
    size_hint_y: None
    height: self.minimum_height

    MDLabel:
        text: root.sender_id
        font_style: "Caption"
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#4cd7f6") if root.side == "left" else get_color_from_hex("#4edea3")
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: root.message_text
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        size_hint_y: None
        height: self.texture_size[1]
        font_name: "Roboto"

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

        # Toolbar supérieure
        MDTopAppBar:
            title: "MeshGuard Terminal"
            anchor_title: "left"
            right_action_items: [["account-circle", lambda x: None]]
            md_bg_color: get_color_from_hex("#0e1511")
            elevation: 2

        # Zone des messages (Scroll)
        ScrollView:
            MDBoxLayout:
                id: chat_logs
                orientation: 'vertical'
                padding: "10dp"
                spacing: "15dp"
                size_hint_y: None
                height: self.minimum_height

        # Zone d'Input (Style Cyber)
        MDBoxLayout:
            size_hint_y: None
            height: "80dp"
            padding: "10dp"
            spacing: "10dp"
            md_bg_color: get_color_from_hex("#1a211d")

            MDTextField:
                id: msg_input
                hint_text: "root@meshguard:~# Enter message"
                mode: "fill"
                fill_color_normal: get_color_from_hex("#2f3632")
                text_color_normal: 1, 1, 1, 1
                hint_text_color_normal: get_color_from_hex("#bbcabf")

            MDIconButton:
                icon: "send"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                md_bg_color: get_color_from_hex("#10b981")
                on_release: app.send_message()

        # Navigation Basse
        MDBottomNavigation:
            size_hint_y: None
            height: "65dp"
            selected_color_background: 0, 0, 0, 0
            text_color_active: get_color_from_hex("#4edea3")

            MDBottomNavigationItem:
                name: 'screen 1'
                text: 'Terminal'
                icon: 'terminal'

            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'Security'
                icon: 'shield'
'''

class MessageBubble(MDCard):
    # Propriétés pour les bulles de message
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
        msg_input = self.root.ids.msg_input
        if msg_input.text.strip() != "":
            # 1. Calcul du SHA-256
            content = msg_input.text
            hash_res = hashlib.sha256(content.encode()).hexdigest()
            
            # 2. Création de la bulle (Outgoing)
            new_msg = MessageBubble(
                sender_id="root@meshguard",
                message_text=content,
                hash_val=hash_res,
                side="right"
            )
            
            # 3. Ajout à l'interface
            self.root.ids.chat_logs.add_widget(new_msg)
            msg_input.text = ""

if __name__ == "__main__":
    SecureNodeApp().run()