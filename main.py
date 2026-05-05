import hashlib
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty

# Désactivation de la taille fixe pour le mobile
# Window.size = (360, 640) 
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
            title: "MESHGUARD_TERMINAL"
            anchor_title: "left"
            md_bg_color: get_color_from_hex("#0e1511")
            elevation: 0
            specific_text_color: get_color_from_hex("#4edea3")

        ScrollView:
            do_scroll_x: False
            MDBoxLayout:
                id: chat_logs
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: "15dp"
                spacing: "15dp"

        # Zone de saisie stabilisée
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

        # Navigation fixe pour éviter le bug d'affichage
        MDBoxLayout:
            size_hint_y: None
            height: "65dp"
            MDBottomNavigation:
                panel_color: get_color_from_hex("#161d19")
                selected_color_background: 0, 0, 0, 0
                
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
            # Intégrité SHA-256
            hash_res = hashlib.sha256(content.encode()).hexdigest()
            
            new_msg = MessageBubble(
                sender_id="root@meshguard",
                message_text=content,
                hash_val=hash_res,
                side="right"
            )
            
            self.root.ids.chat_logs.add_widget(new_msg)
            msg_input.text = ""

if __name__ == "__main__":
    SecureNodeApp().run()