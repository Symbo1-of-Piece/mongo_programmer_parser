import flet as ft

import db_handles as dbh

class Popup(ft.AlertDialog):

    def __init__(self, page, message: str, *args, **kwargs):
        super().__init__(*args, shape=ft.RoundedRectangleBorder(radius=3.0), **kwargs)
        self.content=ft.Text(message)
        page.dialog = self
        self.open = True
        page.update()
        
        
class MElBut(ft.ElevatedButton):
    
    def __init__(self, **kwargs):
        super(MElBut, self).__init__(color=ft.colors.WHITE, **kwargs)
        
    
class SettingsScreen(ft.Column):
    
    def __init__(self, event, *args, **kwargs):
        super().__init__(**kwargs)
        self.event = event
        self.host_input = ft.TextField(label="HOST:PORT", dense=True, value=dbh.HOST)
        self.login_input = ft.TextField(label="Пользователь", dense=True, value=dbh.USERNAME)
        self.password_input = ft.TextField(
            label="Пароль", dense=True, password=True,
            value=dbh.PASSWORD)
        self.db_input = ft.TextField(label="Название БД", dense=True, value=dbh.DB)
        self.build_layout()
        
    def build_layout(self):
        self.controls.extend([
            self.host_input,
            self.login_input,
            self.password_input,
            self.db_input,
            MElBut(text="Сохранить", on_click=self.save_data)
        ])
        
    def save_data(self, e: ft.ControlEvent):
        host = self.host_input.value.strip()
        if host:
            dbh.set_host(host)
        login = self.login_input.value.strip()
        if login:
            dbh.set_username(login)
        password = self.password_input.value.strip()
        if password:
            dbh.set_password(password)
        db = self.db_input.value.strip()
        if db:
            dbh.set_db(db)
        dbh.dump_access_info()
        self.event.set()
        