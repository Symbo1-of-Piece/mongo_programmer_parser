from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd
    
from types_models import PlateInfo


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
        ...