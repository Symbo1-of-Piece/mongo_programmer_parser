from abc import ABC, abstractmethod
from pathlib import Path
from uuid import uuid4
import string
import random

import pandas as pd
    
from types_models import PlateInfo


XLSX_PATH = Path().home() / "auto-programer-db"

if not XLSX_PATH.exists():
    XLSX_PATH.mkdir(parents=True, exist_ok=True)

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
    def export_plate_infos(data: list[PlateInfo], file_name: Path) -> bool:
        pd.DataFrame(data).to_excel(file_name)
        
        
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
    while True:
        if not file.exists():
            return file
        ext = file.suffix
        parent = file.parent
        file_name = file.stem
        file_name += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
        file = parent / (file_name + ext)