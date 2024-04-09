from abc import ABC, abstractmethod
from pathlib import Path
from uuid import uuid4
import string
import random

import pandas as pd
    
from types_models import PlateInfo
from logger import logger


ROOT_FOLDER = Path().home() /  "auto-programer-db"
XLSX_PATH =  ROOT_FOLDER / "reports"
SNMAC_PATH = ROOT_FOLDER / "sn_mac"
    

class FileSaver(ABC):
    
    @staticmethod
    @abstractmethod
    def export_plate_infos(data: list[PlateInfo], file_name: Path) -> bool:
        """Export to file
        
            returns:
                True if saved successfully
        """


class ExcelExporter(FileSaver):
    
    @staticmethod
    def export_plate_infos(data: list[PlateInfo], file_name: Path):

        if not XLSX_PATH.exists():
            XLSX_PATH.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(data)
        writer = pd.ExcelWriter(file_name) 
        df.to_excel(writer, sheet_name='sheet1', index=False, na_rep='NaN')

        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['sheet1'].set_column(col_idx, col_idx, column_length)

        writer.close()



def export_snmac_to_txt(sn_mac_list: list[tuple[str, str]], file_path: Path):
    
    if not file_path.parent.exists:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "w", encoding="utf8") as f:
        f.writelines([f"{i[0]} {i[1]}\n" for i in sn_mac_list if i])


def get_random_name(ext: str):
    
    return str(uuid4()) + ".xlsx"


def sanitize_name(name: Path) -> Path:
    ext = name.suffix
    parent = name.parent
    file_name = name.stem
    
    sanitized_name =  "".join(x for x in file_name if any((x.isalnum(), x in ("_", "-"))))
    return parent / (sanitized_name + ext)


def change_name_if_exists(file: Path) -> Path:
    """if file exists it will generate random additional three  character suffix for file name (before 
    the extension)
    
    argument:
        file:
            type: Path
    
    return:
        unique file Path
    
    """
    if not file.parent.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
    while True:
        if not file.exists():
            return file
        ext = file.suffix
        parent = file.parent
        file_name = file.stem
        file_name += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
        file = parent / (file_name + ext)