from datetime  import datetime

import flet as ft


class PlateInfoRequestLayout(ft.Container):
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.project_name_input = ft.TextField()
        self.start_date_picker = ft.DatePicker()
        self.end_date_picker = ft.DatePicker()
        
    def build(self, parent: list):
        self.content = ft.Row([
            self.project_name_input,
            self.start_date_picker,
            self.end_date_picker
        ])
        parent.append(self)
    
    def get_start_date(self) -> datetime:
        return self.start_date_picker.value
        
    def get_end_date(self) -> datetime:
        return self.end_date_picker.value
    
    def get_project_name(self):
        return self.project_name_input
    
    def get_project_names(self):
        ...
