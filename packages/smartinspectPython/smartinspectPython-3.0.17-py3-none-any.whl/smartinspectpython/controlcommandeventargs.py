"""
Module: controlcommandeventargs.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .controlcommand import ControlCommand

# our package constants.
from .const import (
    UNKNOWN_VALUE
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class ControlCommandEventArgs:
    """
    This class is used by the SmartInspect.ControlCommandEvent event.

    Threadsafety:
        This class is fully thread-safe.
    """
    def __init__(self, controlCommand:ControlCommand) -> None:
        """
        Initializes a new instance of the class.

        Args:
            controlCommand (ControlCommand):
                The Control Command packet which caused the event.
        """

        # initialize instance.
        self.__fControlCommand:ControlCommand = controlCommand


    @property
    def ControlCommand(self) -> ControlCommand:
        """
        Returns the ControlCommand item that was processed.
        """
        return self.__fControlCommand


    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        
        Returns:
            A string in the form of "ControlCommandEventArgs: Type=X, Level=X".
        """
        argsType:str = UNKNOWN_VALUE
        level:str = UNKNOWN_VALUE

        if (self.__fControlCommand != None):
            argsType = self.__fControlCommand.ControlCommandType.name
            level = self.__fControlCommand.Level.name

        return str.format("ControlCommandEventArgs: Type={0}, Level={1}", argsType, level)


@export
class ControlCommandEventHandler:
    """
    This is the event handler type for the SmartInspect.ControlCommandEvent event.
    """

    def __init__(self, sender:object, e:ControlCommandEventArgs) -> None:
        """
        Initializes a new instance of the class.

        Args:
            sender (object):
                The object which fired the event.
            e (ControlCommandEventArgs):
                Arguments that contain detailed information related to the event.
        """
