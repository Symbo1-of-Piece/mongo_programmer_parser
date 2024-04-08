from datetime  import datetime
from threading import Event

import flet as ft


class PlateInfoRequestLayout(ft.Container):
    
    def __init__(self, request_button_state: Event, get_project_names_button_state: Event,
                 *args, **kwargs):
        super().__init__()
        self.request_button_state = request_button_state
        self.get_project_names_button_state = get_project_names_button_state
        self.project_name_input = ft.Dropdown()
        self.start_date_picker = ft.DatePicker()
        self.end_date_picker = ft.DatePicker()
        self.start_date_button = ft.ElevatedButton(
            "Pick start date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.start_date_picker.pick_date(),
        )
        self.end_date_button = ft.ElevatedButton(
            "Pick end date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.end_date_picker.pick_date(),
        )
        
    def build_layout(self, parent: list):
        self.content = ft.Column([
            ft.Row([self.project_name_input, ft.IconButton(ft.icons.REFRESH, on_click=lambda e: self.get_project_names_button_state.set())]),
            self.start_date_picker,
            self.end_date_picker,
            ft.Row([
                self.start_date_button,
                self.end_date_button]),
            ft.ElevatedButton(text="Request", on_click=lambda e: self.request_button_state.set())
        ])
        parent.append(self)
        
    def build_project_names_dropdown(self, names: str):
        self.project_name_input.options = [
            ft.dropdown.Option(i) for i in names
        ]
        self.update()
    
    def get_start_date(self) -> datetime:
        return self.start_date_picker.value
        
    def get_end_date(self) -> datetime:
        return self.end_date_picker.value
    
    def get_project_name(self):
        return self.project_name_input.value
    
    def get_project_names(self):
        ...
