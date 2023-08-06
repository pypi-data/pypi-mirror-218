"""
Module: sessioninfo.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""


# our package imports.
from .level import Level
from .color import Color

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SessionInfo:
    """ 
    Contains session information (internal use only).
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        self.HasName:bool = False
        self.Name:str = ""
        self.HasColor:bool = False
        self.ColorBG:Color = None
        self.HasLevel:bool = False
        self.Level:Level = None
        self.HasActive:bool = False
        self.Active:bool = False
