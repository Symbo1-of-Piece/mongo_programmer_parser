from datetime  import datetime
from threading import Event

import flet as ft

from ui.mod_widgets import MElBut


class PlateInfoRequestLayout(ft.Container):
    
    def __init__(self, request_button_state: Event, get_project_names_button_state: Event, snmac_request_state: Event,
                 *args, **kwargs):
        super().__init__()
        self.snmac_request_state = snmac_request_state
        self.request_button_state = request_button_state
        self.get_project_names_button_state = get_project_names_button_state
        self.project_name_input = ft.Dropdown(label="Проект")
        
        self.start_date_picker = ft.DatePicker()
        self.start_date_label = ft.Text()
        self.start_date_picker.on_change = lambda i: self.update_date_label(
            self.start_date_label, i.control.value.strftime("%Y-%m-%d"))
        self.end_date_picker = ft.DatePicker()
        self.end_date_label = ft.Text()
        self.end_date_picker.on_change = lambda i: self.update_date_label(
            self.end_date_label, i.control.value.strftime("%Y-%m-%d"))
        self.start_date_button = MElBut(
            text="Дата От",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.start_date_picker.pick_date(),
        )
        self.end_date_button = MElBut(
            text="Дата до",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.end_date_picker.pick_date(),
        )
        
    def did_mount(self):
        """Fill projects dropdown with project names from db.
        This is called by flet after the widget is added to the page.
        """
        self.get_project_names_button_state.set()
        
    def build_layout(self, parent: list):
        self.content = ft.Column([
            ft.Row([self.project_name_input, ft.IconButton(ft.icons.REFRESH, on_click=lambda e: self.get_project_names_button_state.set())]),
            self.start_date_picker,
            self.end_date_picker,
            ft.Row([
                ft.Column([
                    self.start_date_button, self.start_date_label
                ]),
                ft.Column([
                    self.end_date_button, self.end_date_label
                ])
            ]),
            
            ft.Text("Получить отчет"),
            ft.Row([
                MElBut(text="Сводная таблица", on_click=lambda e: self.request_button_state.set()),
                MElBut(text="MAC адреса", on_click=lambda e: self.snmac_request_state.set())
            ])
        ])
        parent.append(self)
        
    def build_project_names_dropdown(self, names: str):
        self.project_name_input.options = [
            ft.dropdown.Option(i) for i in names
        ]
        self.update()
    
    def update_date_label(self, label: ft.Text, value: str):
        label.value = value
        label.update()
    
    def get_start_date(self) -> datetime:
        return self.start_date_picker.value
        
    def get_end_date(self) -> datetime:
        return self.end_date_picker.value
    
    def get_project_name(self):
        return self.project_name_input.value
    
    def get_project_names(self):
        ...
