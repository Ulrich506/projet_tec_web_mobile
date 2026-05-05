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
# Dans ton fichier Python, modifie le KV :
KV = '''
MDScreen:
    md_bg_color: get_color_from_hex("#0e1511")

    # On utilise un layout vertical principal
    MDBoxLayout:
        orientation: 'vertical'

        # 1. Barre de titre (fixe en haut)
        MDTopAppBar:
            title: "MESHGUARD_TERMINAL"
            md_bg_color: get_color_from_hex("#0e1511")
            elevation: 0

        # 2. Zone de messages (prend tout l'espace disponible)
        ScrollView:
            do_scroll_x: False
            MDBoxLayout:
                id: chat_logs
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: "10dp"
                spacing: "10dp"

        # 3. Zone de saisie (fixe juste au-dessus de la nav ou du clavier)
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: "8dp"
            spacing: "8dp"
            md_bg_color: get_color_from_hex("#1a211d")

            MDTextField:
                id: msg_input
                hint_text: "Entrer commande..."
                mode: "fill"
                fill_color_normal: get_color_from_hex("#2f3632")
                # Important pour éviter que le texte soit coupé :
                font_size: "16sp" 

            MDIconButton:
                icon: "send"
                md_bg_color: get_color_from_hex("#10b981")
                on_release: app.send_message()

        # 4. Barre de Navigation (en bas de tout)
        MDBottomNavigation:
            size_hint_y: None
            height: "65dp"
            panel_color: get_color_from_hex("#0e1511")
            
            MDBottomNavigationItem:
                name: 'terminal'
                text: 'Terminal'
                icon: 'terminal'
            
            MDBottomNavigationItem:
                name: 'security'
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