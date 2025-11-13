#!/usr/bin/env python3
"""
TONS - Túnel Online No Server v2.0
App Móvil - Por: Jesus Fritz
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse

import requests
import json
import threading
from datetime import datetime
from api_client import APIClient
from vpn_manager import VPNManager

Window.size = (393, 852)

class TonsApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "TonS"
        self.api = APIClient()
        self.vpn = VPNManager()
        self.token = None
        self.user_id = None
        self.username = None
        self.vpn_active = False
        self.contacts = []
        self.messages = {}
        self.current_chat = None
        
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        if self.api.load_token():
            self.show_main_app()
        else:
            self.show_login()
        return self.root
    
    def show_login(self):
        self.root.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        with main_layout.canvas.before:
            Color(0.96, 0.96, 0.96, 1)
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        title = Label(text="Bienvenido", size_hint_y=0.15, font_size='28sp', bold=True, color=(0, 0, 0, 1))
        subtitle = Label(text="Ingresa tus credenciales", size_hint_y=0.1, font_size='12sp', color=(0.4, 0.4, 0.4, 1))
        
        self.login_user = TextInput(hint_text="Usuario", size_hint_y=0.12, multiline=False, background_color=(0.93, 0.93, 0.93, 1), foreground_color=(0, 0, 0, 1), padding=[15, 15])
        self.login_pass = TextInput(hint_text="Contraseña", password=True, size_hint_y=0.12, multiline=False, background_color=(0.93, 0.93, 0.93, 1), foreground_color=(0, 0, 0, 1), padding=[15, 15])
        
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10, orientation='vertical')
        btn_login = Button(text="Entrar", background_color=(0, 0, 0, 1), color=(1, 1, 1, 1), size_hint_y=0.6, font_size='16sp', bold=True)
        btn_login.bind(on_press=self.on_login)
        btn_register = Button(text="Registrar", background_color=(1, 1, 1, 0), color=(0.2, 0.4, 1, 1), size_hint_y=0.4, font_size='14sp')
        btn_register.bind(on_press=self.show_register)
        btn_layout.add_widget(btn_login)
        btn_layout.add_widget(btn_register)
        
        main_layout.add_widget(title)
        main_layout.add_widget(subtitle)
        main_layout.add_widget(Label(size_hint_y=0.1))
        main_layout.add_widget(self.login_user)
        main_layout.add_widget(self.login_pass)
        main_layout.add_widget(Label(size_hint_y=0.1))
        main_layout.add_widget(btn_layout)
        main_layout.add_widget(Label(size_hint_y=0.2))
        
        self.root.add_widget(main_layout)
    
    def on_login(self, instance):
        username = self.login_user.text.strip()
        password = self.login_pass.text.strip()
        if not username or not password:
            self.show_popup("Error", "Completa usuario y contraseña")
            return
        threading.Thread(target=self._login_thread, args=(username, password), daemon=True).start()
    
    def _login_thread(self, username, password):
        try:
            response = requests.post(f"{self.api.BASE_URL}/api/login", json={"username": username, "password": password}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.token = data['token']
                self.user_id = data['user']['id']
                self.username = data['user']['username']
                self.api.save_token(self.token)
                Clock.schedule_once(self._show_main_app_callback, 0)
            else:
                Clock.schedule_once(lambda dt: self.show_popup("Error", "Credenciales inválidas"), 0)
        except Exception as ex:
            Clock.schedule_once(lambda dt: self.show_popup("Error", str(ex)), 0)
    
    def _show_main_app_callback(self, dt):
        self.show_main_app()
    
    def show_register(self, instance):
        self.root.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        with main_layout.canvas.before:
            Color(0.96, 0.96, 0.96, 1)
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        title = Label(text="Registrarse", size_hint_y=0.1, font_size='24sp', bold=True, color=(0, 0, 0, 1))
        self.reg_user = TextInput(hint_text="Usuario", size_hint_y=0.12, multiline=False, background_color=(0.93, 0.93, 0.93, 1), padding=[15, 15])
        self.reg_pass = TextInput(hint_text="Contraseña", password=True, size_hint_y=0.12, multiline=False, background_color=(0.93, 0.93, 0.93, 1), padding=[15, 15])
        self.reg_name = TextInput(hint_text="Nombre", size_hint_y=0.12, multiline=False, background_color=(0.93, 0.93, 0.93, 1), padding=[15, 15])
        
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        btn_reg = Button(text="Crear", background_color=(0, 0, 0, 1), color=(1, 1, 1, 1), bold=True)
        btn_reg.bind(on_press=self.on_register)
        btn_back = Button(text="Volver", background_color=(0.9, 0.9, 0.9, 1), color=(0, 0, 0, 1))
        btn_back.bind(on_press=lambda x: self.show_login())
        btn_layout.add_widget(btn_reg)
        btn_layout.add_widget(btn_back)
        
        main_layout.add_widget(title)
        main_layout.add_widget(Label(size_hint_y=0.05))
        main_layout.add_widget(self.reg_user)
        main_layout.add_widget(self.reg_pass)
        main_layout.add_widget(self.reg_name)
        main_layout.add_widget(Label(size_hint_y=0.05))
        main_layout.add_widget(btn_layout)
        main_layout.add_widget(Label(size_hint_y=0.4))
        
        self.root.add_widget(main_layout)
    
    def on_register(self, instance):
        username = self.reg_user.text.strip()
        password = self.reg_pass.text.strip()
        name = self.reg_name.text.strip()
        if not all([username, password, name]):
            self.show_popup("Error", "Completa todos los campos")
            return
        threading.Thread(target=self._register_thread, args=(username, password, name), daemon=True).start()
    
    def _register_thread(self, username, password, name):
        try:
            response = requests.post(f"{self.api.BASE_URL}/api/register", json={"username": username, "password": password, "nombre_display": name}, timeout=10)
            if response.status_code == 201:
                data = response.json()
                self.token = data['token']
                self.user_id = data['user']['id']
                self.username = data['user']['username']
                self.api.save_token(self.token)
                Clock.schedule_once(self._show_main_app_callback, 0)
            else:
                Clock.schedule_once(lambda dt: self.show_popup("Error", response.json().get('error', 'Error')), 0)
        except Exception as ex:
            Clock.schedule_once(lambda dt: self.show_popup("Error", str(ex)), 0)
    
    def show_main_app(self):
        self.root.clear_widgets()
        tab_panel = TabbedPanel(size_hint=(1, 1), do_default_tab=False, tab_pos='top_mid')
        
        tab1 = TabbedPanelItem(text='VPN')
        tab1.add_widget(self.create_vpn_screen())
        tab_panel.add_widget(tab1)
        
        tab2 = TabbedPanelItem(text='Chats')
        tab2.add_widget(self.create_chats_screen())
        tab_panel.add_widget(tab2)
        
        tab3 = TabbedPanelItem(text='Perfil')
        tab3.add_widget(self.create_profile_screen())
        tab_panel.add_widget(tab3)
        
        self.root.add_widget(tab_panel)
    
    def create_vpn_screen(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        logo = Label(text="TonS", size_hint_y=0.15, font_size='32sp', bold=True, color=(0, 0, 0, 1))
        layout.add_widget(logo)
        
        vpn_btn_container = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=0.45)
        self.vpn_btn = Button(text="Encender", size_hint=(None, None), size=(200, 200), background_normal='', background_color=(0.15, 0.39, 0.92, 1), color=(1, 1, 1, 1), font_size='18sp', bold=True)
        self.vpn_btn.bind(on_press=self.toggle_vpn)
        vpn_btn_container.add_widget(self.vpn_btn)
        layout.add_widget(vpn_btn_container)
        
        self.vpn_status = Label(text="VPN Desconectado", size_hint_y=0.15, font_size='14sp', color=(0.4, 0.4, 0.4, 1))
        layout.add_widget(self.vpn_status)
        layout.add_widget(Label(size_hint_y=0.25))
        
        return layout
    
    def toggle_vpn(self, instance):
        if not self.vpn_active:
            self.vpn_active = True
            self.vpn.connect()
            self.vpn_btn.background_color = (0.06, 0.71, 0.4, 1)
            self.vpn_btn.text = "Conectado"
            self.vpn_status.text = "VPN Activo\nTu conexión está protegida"
        else:
            self.vpn_active = False
            self.vpn.disconnect()
            self.vpn_btn.background_color = (0.15, 0.39, 0.92, 1)
            self.vpn_btn.text = "Encender"
            self.vpn_status.text = "VPN Desconectado"
    
    def create_chats_screen(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        title = Label(text="Chats", size_hint_y=0.08, font_size='24sp', bold=True, color=(0, 0, 0, 1))
        layout.add_widget(title)
        
        search = TextInput(hint_text="Buscar chats...", size_hint_y=0.08, multiline=False, background_color=(0.95, 0.95, 0.95, 1), padding=[15, 12])
        layout.add_widget(search)
        
        scroll = ScrollView(size_hint=(1, 0.74))
        self.chats_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=[5, 5])
        self.chats_list.bind(minimum_height=self.chats_list.setter('height'))
        scroll.add_widget(self.chats_list)
        layout.add_widget(scroll)
        
        btn_new = Button(text="+ Nuevo chat", size_hint_y=0.1, background_color=(0.15, 0.83, 0.4, 1), color=(1, 1, 1, 1), bold=True)
        btn_new.bind(on_press=self.new_chat)
        layout.add_widget(btn_new)
        
        threading.Thread(target=self._load_contacts, daemon=True).start()
        
        return layout
    
    def _load_contacts(self):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api.BASE_URL}/api/contacts", headers=headers, timeout=10)
            if response.status_code == 200:
                self.contacts = response.json()['contacts']
                Clock.schedule_once(self._update_contacts_ui, 0)
        except Exception as e:
            print(f"Error loading contacts: {e}")
    
    def _update_contacts_ui(self, dt):
        self.chats_list.clear_widgets()
        if not self.contacts:
            self.chats_list.add_widget(Label(text="Sin contactos\nAgrega con el botón verde", color=(0.6, 0.6, 0.6, 1)))
            return
        for contact in self.contacts:
            btn = Button(text=f"{contact['nombre_display']}\n@{contact['username']}", size_hint_y=None, height=70, background_color=(0.97, 0.97, 0.97, 1), color=(0, 0, 0, 1))
            btn.bind(on_press=lambda x, c=contact: self.open_chat(c))
            self.chats_list.add_widget(btn)
    
    def new_chat(self, instance):
        popup = Popup(title="Agregar Contacto", size_hint=(0.9, 0.4))
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="Username:", color=(0, 0, 0, 1)))
        username_input = TextInput(hint_text="username", multiline=False, background_color=(0.95, 0.95, 0.95, 1), size_hint_y=0.3)
        content.add_widget(username_input)
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        btn_add = Button(text="Agregar", background_color=(0.15, 0.83, 0.4, 1), color=(1, 1, 1, 1))
        btn_add.bind(on_press=lambda x: self._add_contact(username_input.text, popup))
        btn_cancel = Button(text="Cancelar", background_color=(0.9, 0.9, 0.9, 1), color=(0, 0, 0, 1))
        btn_cancel.bind(on_press=popup.dismiss)
        btn_layout.add_widget(btn_add)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)
        popup.content = content
        popup.open()
    
    def _add_contact(self, username, popup):
        username = username.strip()
        if not username:
            return
        popup.dismiss()
        threading.Thread(target=self._add_contact_thread, args=(username,), daemon=True).start()
    
    def _add_contact_thread(self, username):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(f"{self.api.BASE_URL}/api/contacts/add", headers=headers, json={"username": username}, timeout=10)
            if response.status_code == 200:
                Clock.schedule_once(lambda dt: self.show_popup("Éxito", f"{username} agregado"), 0)
                Clock.schedule_once(lambda dt: self._reload_chats_after_add(), 0.5)
            else:
                error = response.json().get('error', 'Error')
                Clock.schedule_once(lambda dt: self.show_popup("Error", error), 0)
        except Exception as ex:
            Clock.schedule_once(lambda dt: self.show_popup("Error", str(ex)), 0)
    
    def _reload_chats_after_add(self):
        threading.Thread(target=self._load_contacts, daemon=True).start()
    
    def open_chat(self, contact):
        self.current_chat = contact
        self.show_chat_screen(contact)
    
    def show_chat_screen(self, contact):
        self.root.clear_widgets()
        layout = BoxLayout(orientation='vertical')
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        header = BoxLayout(orientation='horizontal', size_hint_y=0.08, padding=[10, 5])
        btn_back = Button(text="<", size_hint_x=0.15, background_color=(0, 0, 0, 0), color=(0, 0, 0, 1), font_size='20sp')
        btn_back.bind(on_press=lambda x: self.show_main_app())
        header.add_widget(btn_back)
        header.add_widget(Label(text=contact['nombre_display'], size_hint_x=0.7, color=(0, 0, 0, 1), bold=True))
        header.add_widget(Label(size_hint_x=0.15))
        layout.add_widget(header)
        
        scroll = ScrollView(size_hint=(1, 0.82))
        self.messages_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=[10, 10])
        self.messages_list.bind(minimum_height=self.messages_list.setter('height'))
        scroll.add_widget(self.messages_list)
        layout.add_widget(scroll)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, padding=[10, 5], spacing=10)
        self.message_input = TextInput(hint_text="Mensaje", multiline=False, background_color=(0.95, 0.95, 0.95, 1), size_hint_x=0.8)
        btn_send = Button(text="Enviar", size_hint_x=0.2, background_color=(0.15, 0.83, 0.4, 1), color=(1, 1, 1, 1))
        btn_send.bind(on_press=self.send_message)
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(btn_send)
        layout.add_widget(input_layout)
        
        self.root.add_widget(layout)
        self.messages_list.add_widget(Label(text="Chat abierto\n(Mensajes en tiempo real próximamente)", color=(0.6, 0.6, 0.6, 1), size_hint_y=None, height=50))
    
    def send_message(self, instance):
        text = self.message_input.text.strip()
        if not text:
            return
        msg_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=[10, 5])
        msg_layout.add_widget(Label(size_hint_x=0.3))
        msg_label = Label(text=text, color=(1, 1, 1, 1), size_hint_x=0.7)
        msg_layout.add_widget(msg_label)
        self.messages_list.add_widget(msg_layout)
        self.message_input.text = ""
        threading.Thread(target=self._send_message_thread, args=(text,), daemon=True).start()
    
    def _send_message_thread(self, text):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            requests.post(f"{self.api.BASE_URL}/api/messages/send", headers=headers, json={"destinatario_id": self.current_chat['id'], "contenido": text}, timeout=10)
        except:
            pass
    
    def create_profile_screen(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)
        
        layout.add_widget(Label(text=self.username or "Usuario", size_hint_y=0.1, font_size='20sp', bold=True, color=(0, 0, 0, 1)))
        layout.add_widget(Label(text=f"@{self.username or 'usuario'}", size_hint_y=0.08, font_size='14sp', color=(0.6, 0.6, 0.6, 1)))
        layout.add_widget(Label(size_hint_y=0.1))
        
        btn_logout = Button(text="Cerrar sesión", size_hint_y=0.1, background_color=(0.9, 0.2, 0.2, 1), color=(1, 1, 1, 1), bold=True)
        btn_logout.bind(on_press=self.logout)
        layout.add_widget(btn_logout)
        layout.add_widget(Label(size_hint_y=0.64))
        
        return layout
    
    def logout(self, instance):
        self.api.clear_token()
        self.token = None
        self.username = None
        self.user_id = None
        self.show_login()
    
    def show_popup(self, title, message):
        popup = Popup(title=title, size_hint=(0.85, 0.35))
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, color=(0, 0, 0, 1)))
        btn = Button(text="OK", size_hint_y=0.3, background_color=(0.15, 0.39, 0.92, 1), color=(1, 1, 1, 1))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.content = content
        popup.open()
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    TonsApp().run()
