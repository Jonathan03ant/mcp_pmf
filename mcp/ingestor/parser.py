from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List
import json 
from pathlib import Path


#---------------------------------------------------#
# Data model                                        #
#---------------------------------------------------#
@dataclass
class FileDetail:
    """
        Key: relative path of the file (ParsedFirmware.files)
        Value: List of symbole names by kind
    """
    path: str