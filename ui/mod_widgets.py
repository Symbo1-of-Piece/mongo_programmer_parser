import flet as ft


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