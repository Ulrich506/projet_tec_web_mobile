import hashlib
import time
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty

# Configuration pour que l'interface monte avec le clavier
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
            title: "TEC WEB MOBIL"
            anchor_title: "left"
            md_bg_color: get_color_from_hex("#0e1511")
            elevation: 0
            specific_text_color: get_color_from_hex("#4edea3")

        MDBottomNavigation:
            id: panel
            panel_color: get_color_from_hex("#161d19")
            text_color_active: get_color_from_hex("#4edea3")

            # --- ONGLET TERMINAL ---
            MDBottomNavigationItem:
                name: 'terminal'
                text: 'Terminal'
                icon: 'terminal'

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

                    # Zone de saisie double (IP + Message)
                    MDBoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: "130dp"
                        padding: "10dp"
                        spacing: "8dp"
                        md_bg_color: get_color_from_hex("#1a211d")

                        MDTextField:
                            id: ip_address
                            hint_text: "IP Destinataire (ex: 192.168.1.5)"
                            mode: "fill"
                            fill_color_normal: get_color_from_hex("#09100c")
                            size_hint_y: None
                            height: "40dp"
                            text_color_normal: 1, 1, 1, 1

                        MDBoxLayout:
                            spacing: "10dp"
                            MDTextField:
                                id: msg_input
                                hint_text: "Entrer commande..."
                                mode: "fill"
                                fill_color_normal: get_color_from_hex("#09100c")
                                text_color_normal: 1, 1, 1, 1

                            MDIconButton:
                                icon: "send"
                                md_bg_color: get_color_from_hex("#4edea3")
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                on_release: app.send_message()

            # --- ONGLET SECURITY (Schéma de Trajet) ---
            MDBottomNavigationItem:
                name: 'security'
                text: 'Security'
                icon: 'shield-network'

                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "20dp"
                    spacing: "10dp"

                    MDLabel:
                        text: "MESH TOPOLOGY TRACKER"
                        halign: "center"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#4edea3")

                    # Schéma visuel simplifié
                    MDCard:
                        orientation: "vertical"
                        padding: "15dp"
                        md_bg_color: get_color_from_hex("#161d19")
                        radius: 15
                        
                        MDLabel:
                            id: schema_visual
                            text: "● (YOU)\\n  │\\n  ▼\\n○ (NODE_ENI)\\n  │\\n  ▼\\n✸ (RELAY_MESH)\\n  │\\n  ▼\\n◎ (TARGET_IP)"
                            halign: "center"
                            font_name: "Roboto"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#4edea3")

                    MDLabel:
                        id: trace_details
                        text: "Status: Idle\\nLast Packet: None"
                        halign: "center"
                        theme_text_color: "Hint"
                        font_style: "Caption"
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
        ip = self.root.ids.ip_address.text
        msg = self.root.ids.msg_input.text
        
        if msg.strip() != "" and ip.strip() != "":
            # SHA-256 Intégrité
            h = hashlib.sha256(msg.encode()).hexdigest()
            
            # Ajout à l'interface
            new_msg = MessageBubble(
                sender_id=f"TO: {ip}",
                message_text=msg,
                hash_val=h,
                side="right"
            )
            self.root.ids.chat_logs.add_widget(new_msg)
            
            # Mise à jour du Schéma de trajet (Vertical/Etoile)
            t = time.strftime("%H:%M:%S")
            self.root.ids.schema_visual.text = f"● (YOU)\\n  │\\n  ▼\\n○ (NODE_ENI)\\n  │  [OK]\\n  ▼\\n✸ (RELAY_MESH)\\n  │  [HASH:{h[:4]}]\\n  ▼\\n◎ ({ip})"
            self.root.ids.trace_details.text = f"Status: PACKET DELIVERED\\nTime: {t}\\nTarget: {ip}"
            
            self.root.ids.msg_input.text = ""

if __name__ == "__main__":
    SecureNodeApp().run()