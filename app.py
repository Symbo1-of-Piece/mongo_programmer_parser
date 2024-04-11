from threading import Thread, Event

import flet as ft
import flet_core

from ui.mod_widgets import SettingsScreen
from controllers.plate_info_request_controller import PlateInfoRequestController

VERSION = "0.0.2"

def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO
    page.title = "Auto-programmer client v. " + VERSION
    page.window_width = 400      
    page.window_height = 450
    page.theme_mode = ft.ThemeMode.DARK
    # page.window_title_bar_hidden = True
    page.window_frameless = True
    plate_info_request_controller = PlateInfoRequestController()
    main_column = ft.Column()
    main_column.controls.append(
        ft.Row([
            ft.Column([
                ft.Text(VERSION),
                ft.Text("Auto-programmer client", size=22, height=35)
                
            ]),
            ft.Container(
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    on_click=lambda i: page.window_close()), 
                alignment=ft.alignment.center_right, expand=True)
            ], 
            width=page.window_width)
    )
    draggable = ft.WindowDragArea(
        ft.Container(main_column,
            bgcolor=ft.colors.BLACK, padding=10), expand=True)
    
    plate_info_request_controller.build_layout(main_column.controls)
    main_column.controls.append(ft.Container(
        content=ft.IconButton(icon=ft.icons.SETTINGS_APPLICATIONS, on_click=show_settings),
        alignment=ft.alignment.bottom_right
    ))
    page.add(draggable)
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

