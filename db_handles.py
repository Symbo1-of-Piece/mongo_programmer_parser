import json
from pathlib import Path

from pymongo import MongoClient
from pymongo.collection import Collection
from bson import json_util
from collections import Counter
import os
from logger import logger
from file_saver import ROOT_FOLDER

ACCESS_PATH = ROOT_FOLDER / "dbaccess.txt"

if ACCESS_PATH.exists():
    with open(ACCESS_PATH, encoding="utf8") as f:
        try:
            data: dict = json.load(f)
        except Exception as e:
            logger.error(e)
            raise e

        HOST = data["HOST"]
        USERNAME = data["USERNAME"]
        PASSWORD = data["PASSWORD"]
        DB = data["DB"]
else:
    HOST = "192.168.55.179:27017"
    USERNAME = "dev"
    PASSWORD = "mongo9181"
    DB = "auto-programmer-db"


def dump_access_info():
    if not ACCESS_PATH.parent.exists():
        ACCESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ACCESS_PATH, "w", encoding="utf8") as f:
        json.dump({
            "HOST": HOST,
            "USERNAME": USERNAME,
            "PASSWORD": PASSWORD,
            "DB": DB
        }, f, ensure_ascii=False)


def set_host(host: str):
    global HOST
    HOST = host

def set_username(user: str):
    global USERNAME
    USERNAME = user
    

def set_password(password: str):
    global PASSWORD
    PASSWORD = password


def set_db(db: str):
    global DB
    DB = db
    

def get_fw_collection() -> tuple[MongoClient, Collection]:
    global firmware_collection
    if PASSWORD:
        client = MongoClient(HOST, username=USERNAME, password=PASSWORD)
    else:
        client = MongoClient(HOST)
    db = client[DB]
    firmware_collection = db['firmware_projects_arch']
    collection_list = db.list_collection_names()

    if collection_list is not None:
        print("Подключение к MongoDB успешно")
    else:
        print("Не удалось подключиться к MongoDB.")
    return client, firmware_collection


def find_unique_project_names(collection, timestamp:str = None):
    """
    Функция для поиска уникальных имен проектов.
    
    Parameters:
        firmware_collection(pymongo.collection.Collection): Коллекция MongoDB, из которой нужно извлечь данные. 
        timestamp(str, optional): опциональный параметр, при наличии которого будет фильтрация только за указанную дату
                        (по умолчанию за все время)
        
    Returns:
       unique_project_names(list): возвращает список с уникальными именами проектов
        
    Example_usage: 
        find_unique_project_names(firmware_collection)
        find_unique_project_names(firmware_collection, '2024-03-21')
        
    """
    query = {}
    if timestamp:
        query['timestamp'] = {'$regex': timestamp}

    unique_project_names = firmware_collection.distinct('project_name', query)
    return unique_project_names


def find_documents(query:dict):
    """
    Функция для поиска документов по заданному запросу.
    
    Parameters:
        query(dict): объект типа словарь, содержащий условие поиска
        
    Returns:
        json_documents: итерируемый объект JSON, содержащий документы, удовлетворяющие запросу
        
    Example_usage: 
        find_documents({"project_name":"td_ble_523"})
    """
    cursor = list(firmware_collection.find(query))
    if cursor:
        json_documents = json_util.dumps(cursor)
        return json_documents
    else:
        return 'Документы не найдены'
    
    
def get_data_for_report(collection, start_date, end_date, project_name):
    """
    Функция для возврата информации для отчета: название проекта, прошивка, дата, микроконтроллер

    Parameters:
        collection (pymongo.collection.Collection): Коллекция MongoDB, из которой нужно извлечь данные. 
        start_date (str): Начальная дата в формате 'YYYY-MM-DD'.
        end_date (str): Конечная дата в формате 'YYYY-MM-DD'.
        project_name(str): Имя проекта
        
    Returns:
       data_for_report (list): JSON-подобный список словарей, содержащий информацию для отчета.
       
    Example_usage:
        get_data_for_report(firmware_collection, "2024-03-22", "2024-03-24", "td_ble_523")

    """
    query = {'project_name' : project_name,
             'timestamp' : {'$gte': start_date,
                           '$lte': end_date}}
    projection = {'_id': 0, 'plates': 1, 'firmware_settings.path_to_firmware': 1,
                  'firmware_settings.device': 1, 'project_name': 1, 'timestamp': 1}

    cursor = collection.find(query, projection)
    report = []
    for document in cursor:
        one_file_report = {}
        project_name = document.get('project_name', '')
        timestamp = document.get('timestamp', '')
        firmware_settings = document.get('firmware_settings', {})
        microcontroller_type = firmware_settings.get('device', '')
        path_to_firmware = firmware_settings.get('path_to_firmware', '')
        firmware_file = os.path.basename(path_to_firmware)
        
        plates = document.get('plates', {})
        for plate_info in plates.values():
            serial_number = plate_info.get('serial_number')
            mac_address = plate_info.get('mac_address')
            status = plate_info.get("status")
            one_file_report = {
                'project_name': project_name,
                'timestamp': timestamp,
                'status': status,
                'serial_number': serial_number,
                'mac_address': mac_address,
                'microcontroller_type': microcontroller_type,
                'firmware_file': firmware_file
            }
            report.append(one_file_report)
    return report


def get_serial_mac_pairs(collection, start_date: str, end_date: str, project_name) -> list[tuple[str, str]]:
    """
    Функция для извлечения списка пар серийный номер - MAC-адрес за указанный промежуток времени.

    Parameters:
        collection (pymongo.collection.Collection): Коллекция MongoDB, из которой нужно извлечь данные. 
        start_date (str): Начальная дата в формате 'YYYY-MM-DD'.
        end_date (str): Конечная дата в формате 'YYYY-MM-DD'.
        
    Returns:
       serial_mac_pairs (list): Список, который содержит пары значений serial_number, mac_address.
       
    Example_usage:
        get_serial_mac_pairs(firmware_collection, "2024-03-20", "2024-03-24")

    """
    query = {
        'project_name' : project_name,
        'timestamp': {'$gte': start_date,
                           '$lte': end_date}
             }
    projection = {'_id': 0, 'plates': 1}

    cursor = collection.find(query, projection)

    serial_mac_pairs = []
    for document in cursor:
        plates = document.get('plates', {})
        for plate_info in plates.values():
            serial_number = plate_info.get('serial_number')
            mac_address = plate_info.get('mac_address')
            serial_mac_pairs.append((serial_number, mac_address)) 
    return serial_mac_pairs