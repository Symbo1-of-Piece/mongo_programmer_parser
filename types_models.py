from typing import TypeAlias, Literal
from dataclasses import dataclass


PlateStatus: TypeAlias =  Literal["success", "failed", "nottodo"]


@dataclass
class PlateInfo:
    
    project_name: str
    firmware_name: str
    status: PlateStatus
    serial: str|None = None
    mac: str|None = None