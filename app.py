from threading import Thread, Event

import flet as ft
import flet_core

from ui.mod_widgets import SettingsScreen
from controllers.plate_info_request_controller import PlateInfoRequestController

VERSION = "0.0.1"

def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO
    page.title = "Auto-programmer DB client v. " + VERSION
    
    page.window_width = 400      
    page.window_height = 350 
    page.theme_mode = flet_core.ThemeMode.DARK
    plate_info_request_controller = PlateInfoRequestController()
    main_column = ft.Column()
    plate_info_request_controller.build_layout(main_column.controls)
    main_column.controls.append(ft.Row(
        [ft.Row(), ft.IconButton(icon=ft.icons.SETTINGS, on_click=show_settings)]
    ))
    page.add(main_column)
    page.update()
    pass


def show_settings(e: ft.ControlEvent, *args):
    popup = ft.AlertDialog(open=True)
    popup_close_event = Event()
    settings_screen = SettingsScreen(popup_close_event)
    popup.content = settings_screen
    e.page.dialog = popup
    e.page.update()
    popup_close_event.wait()
    e.page.dialog.open = False
    e.page.update()

