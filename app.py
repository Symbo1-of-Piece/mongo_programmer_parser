import flet as ft

from controllers.plate_info_request_controller import PlateInfoRequestController


def main(page: ft.Page):
    plate_infor_request_controller = PlateInfoRequestController()
    main_column = ft.Column()
    plate_infor_request_controller.build_layout(main_column.controls)
    page.add(main_column)
    page.update()
    pass

