import flet as ft
from threading import Event, Thread
from uuid import uuid4
from datetime import datetime

from ui.plate_info_request_layout import PlateInfoRequestLayout
from ui import mod_widgets as mw
import db_handles as dbh
from logger import logger
import file_saver as fs


class PlateInfoRequestController:
    
    def __init__(self):
        self.plate_info_request_button_state = Event()
        self.get_project_names_button_state = Event()
        self.snmac_request_button_state = Event()
        self.layout = PlateInfoRequestLayout(
            self.plate_info_request_button_state, self.get_project_names_button_state,
            self.snmac_request_button_state)
        Thread(target=self.get_project_names_button_state_monitor, daemon=True).start()
        Thread(target=self.plate_info_request_button_state_monitor, daemon=True).start()
        Thread(target=self.snmac_request_button_state_monitor, daemon=True).start()
        
    def get_project_names(self):
        ...
        
    def build_layout(self, place: list):
        self.layout.build_layout(place)
        
    def get_project_names_button_state_monitor(self):
        # logger.debug(f"{self} start dropdown monitor")
        while True:
            try:
                self.get_project_names_button_state.wait()
                self.fill_projects_dropdown()
            except Exception as e:
                logger.exception(e)
            finally:
                self.get_project_names_button_state.clear()
                
    def fill_projects_dropdown(self):
        client, collection = dbh.get_fw_collection()
        names = dbh.find_unique_project_names(collection)
        client.close()
        self.layout.build_project_names_dropdown(names)
                
    def plate_info_request_button_state_monitor(self):
        while True:
            try:
                self.plate_info_request_button_state.wait()
                client, collection = dbh.get_fw_collection()
                try:
                    start_date = self.layout.get_start_date().strftime("%Y-%m-%d")
                    end_date = self.layout.get_end_date().strftime("%Y-%m-%d")
                except AttributeError:
                    mw.Popup(self.layout.page, f"Дата не выбрана")
                    continue
                name = self.layout.get_project_name()
                plates_info = dbh.get_data_for_report(
                    collection,
                    start_date, end_date,
                    name)
                if not plates_info:
                    mw.Popup(self.layout.page, f"Прошивок {name} за период {start_date} - {end_date} не найдено")
                    continue
                client.close()
                name = f"{name}_{start_date}_{end_date}.xlsx"
                path = fs.XLSX_PATH / name
                path = str(fs.change_name_if_exists(fs.sanitize_name(path)))
                fs.ExcelExporter.export_plate_infos(plates_info, path)
                mw.Popup(self.layout.page, f"Файл {path} успешно сохранен")
            except Exception as e:
                logger.exception(e)
            finally:
                self.plate_info_request_button_state.clear()
                
    def snmac_request_button_state_monitor(self):
        while True:
            try:
                self.snmac_request_button_state.wait()
                client, collection = dbh.get_fw_collection()
                try:
                    start_date = self.layout.get_start_date().strftime("%Y-%m-%d")
                    end_date = self.layout.get_end_date().strftime("%Y-%m-%d")
                except AttributeError:
                    mw.Popup(self.layout.page, f"Дата не выбрана")
                    continue
                name = self.layout.get_project_name()
                snmac_list = dbh.get_serial_mac_pairs(collection, start_date, end_date, name)
                if not snmac_list:
                    mw.Popup(self.layout.page, f"В {name} за период {start_date} - {end_date} MAC адресов не найдено")
                    continue
                client.close()
                file_name = (f"{name}_{snmac_list[0][0]}_{snmac_list[-1][0]}"
                        f"_{start_date}_{end_date}.txt")
                path = fs.SNMAC_PATH / name / file_name
                path = fs.change_name_if_exists(fs.sanitize_name(path))
                fs.export_snmac_to_txt(snmac_list, path)
                mw.Popup(self.layout.page, f"Файл {path} успешно сохранен")
            except Exception as e:
                logger.exception(e)
            finally:
                self.snmac_request_button_state.clear()