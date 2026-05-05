import hashlib
import time
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, NumericProperty

# Optimisation pour mobile
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
            selected_color_background: 0, 0, 0, 0
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

                    MDBoxLayout:
                        size_hint_y: None
                        height: "80dp"
                        padding: ["10dp", "5dp", "10dp", "5dp"]
                        spacing: "10dp"
                        md_bg_color: get_color_from_hex("#161d19")

                        MDTextField:
                            id: msg_input
                            hint_text: "Entrer commande..."
                            mode: "fill"
                            fill_color_normal: get_color_from_hex("#09100c")
                            font_size: "16sp"
                            text_color_normal: 1, 1, 1, 1
                            pos_hint: {"center_y": .5}

                        MDIconButton:
                            icon: "send"
                            md_bg_color: get_color_from_hex("#4edea3")
                            theme_text_color: "Custom"
                            text_color: 0, 0, 0, 1
                            pos_hint: {"center_y": .5}
                            on_release: app.send_message()

            # --- ONGLET SECURITY (NOUVEAU) ---
            MDBottomNavigationItem:
                name: 'security'
                text: 'Security'
                icon: 'shield-check'

                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "15dp"
                    spacing: "15dp"

                    MDLabel:
                        text: "SECURE NODE MONITOR"
                        halign: "center"
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#4edea3")
                        size_hint_y: None
                        height: "40dp"

                    MDCard:
                        orientation: "vertical"
                        padding: "15dp"
                        size_hint_y: None
                        height: "120dp"
                        md_bg_color: get_color_from_hex("#161d19")
                        radius: 12
                        
                        MDLabel:
                            text: "MESSAGE TRACE ROUTE (REAL-TIME)"
                            bold: True
                            font_style: "Caption"
                        MDLabel:
                            id: trace_path
                            text: "Waiting for packet..."
                            theme_text_color: "Hint"
                            font_name: "Roboto"
                            font_style: "Body2"

                    MDCard:
                        orientation: "vertical"
                        padding: "15dp"
                        size_hint_y: None
                        height: "100dp"
                        md_bg_color: get_color_from_hex("#161d19")
                        radius: 12
                        
                        MDBoxLayout:
                            MDLabel:
                                text: "Integrity Engine"
                                bold: True
                            MDLabel:
                                text: "ACTIVE"
                                halign: "right"
                                text_color: 0, 1, 0, 1
                        MDLabel:
                            text: "Algorithm: SHA-256 Protocol"
                            theme_text_color: "Hint"
                        MDLabel:
                            text: "Status: Secure Connection (Encrypted)"
                            theme_text_color: "Hint"

                    MDBoxLayout:
                        spacing: "10dp"
                        MDRaisedButton:
                            text: "CLEAR LOGS"
                            md_bg_color: get_color_from_hex("#e11d48")
                            on_release: chat_logs.clear_widgets()
                        MDRaisedButton:
                            text: "REFRESH NODE"
                            md_bg_color: get_color_from_hex("#10b981")
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
        msg_input = self.root.ids.msg_input
        if msg_input.text.strip() != "":
            content = msg_input.text
            hash_res = hashlib.sha256(content.encode()).hexdigest()
            
            # Création du message
            new_msg = MessageBubble(
                sender_id="root@meshguard",
                message_text=content,
                hash_val=hash_res,
                side="right"
            )
            
            # Ajout au terminal
            self.root.ids.chat_logs.add_widget(new_msg)
            
            # Mise à jour du "Trace Route" (Chemin du message)
            # Simule le passage par différents nœuds Mesh même hors ligne
            timestamp = time.strftime("%H:%M:%S")
            path_sim = f"[{timestamp}] Client -> Local_Node (ENI) -> MESH_RELAY_01 -> SHA256_VERIFIED -> SUCCESS"
            self.root.ids.trace_path.text = path_sim
            
            msg_input.text = ""

if __name__ == "__main__":
    SecureNodeApp().run()