import flet as ft
import flet_core

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
    page.add(main_column)
    page.update()
    pass

