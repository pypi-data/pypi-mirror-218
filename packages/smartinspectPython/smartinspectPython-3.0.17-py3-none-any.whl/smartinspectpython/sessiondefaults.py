"""
Module: sessiondefaults.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

import _threading_local

# our package imports.
from .level import Level as SILevel
from .session import Session
from .color import Color

# our package constants.
from .const import (
    DEFAULT_COLOR_VALUE
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SessionDefaults:
    """ 
    Specifies the default property values for newly created sessions.
    
    This class is used by the SmartInspect class to customize the
    default property values for newly created sessions. Sessions
    that will be created by or passed to the AddSession method of
    the SmartInspect class will be automatically configured with
    the values of the SmartInspect.SessionDefaults property.

    Threadsafety:
        This class is fully thread-safe.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        self.__fLock = _threading_local.RLock()
        self.__fActive:bool = True
        self.__fColorBG:Color = Color(DEFAULT_COLOR_VALUE)
        self.__fLevel:SILevel = SILevel.Debug


    @property
    def Active(self) -> bool:
        """ 
        Gets the Active property value.

        Represents the default Active property for newly created sessions.
        
        Please see Session.Active for general information about the
        active status of sessions.
        """
        return self.__fActive
    

    @Active.setter
    def Active(self, value: bool) -> None:
        """ 
        Sets the Active property value.
        """
        if value != None:
            self.__fActive = value


    @property
    def ColorBG(self) -> Color:
        """
        Gets the ColorBG property value.

        Represents the default background Color property for newly created sessions.
        
        Please see Session.ColorBG for general information about the
        background color of sessions.
        """
        with self.__fLock:

            return self.__fColorBG;  # not atomic


    @ColorBG.setter
    def ColorBG(self, value: Color) -> None:
        """ 
        Sets the ColorBG property value.
        """
        with self.__fLock:

            self.__fColorBG = value   # Not atomic


    @property
    def Level(self) -> SILevel:
        """ 
        Gets the Level property value.

        Represents the default Level property for newly created
        sessions.

        Please see Session.Level for general information about the
        log level of sessions.
        """
        return self.__fLevel


    @Level.setter
    def Level(self, value:SILevel) -> None:
        """ 
        Sets the Level property value.
        """
        if value != None:
            self.__fLevel = value


    def Assign(self, session:Session) -> None:
        """
        Sets various properties of the specified session with like-named 
        properties of the session defaults.

        Args:
            session (Session):
                Session whose properties will be set from session defaults.
        """
        session.Active = self.Active
        session.Level = self.Level
        session.ColorBG = self.ColorBG
