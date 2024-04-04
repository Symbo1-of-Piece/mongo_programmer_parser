from typing import TypeAlias, Literal
from dataclasses import dataclass


PlateStatus: TypeAlias =  Literal["success", "failed", "nottodo"]


@dataclass
class PlateInfo:
    
    project_name: str
    timestamp : str
    firmware_name: str
    status: PlateStatus
    serial: int|None = None
    mac: str|None = None
    cycle_time: int|0 = None
    microcontroller_type: str = None
    firmware_file: str = None