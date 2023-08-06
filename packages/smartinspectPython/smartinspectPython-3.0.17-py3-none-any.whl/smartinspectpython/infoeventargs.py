"""
Module: infoeventargs.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package constants.
from .const import (
    UNKNOWN_VALUE
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class InfoEventArgs:
    """
    Arguments passed to the SmartInspect.InfoEvent event.

    It has only one public class property named Message.

    Threadsafety:
        This class is fully thread-safe.
    """

    def __init__(self, message:str) -> None:
        """
        Initializes a new instance of the class.

        Args:
            message (str):
                Informational message to convey.
        """

        # initialize instance.
        self.__fMessage:Exception = message


    @property
    def Message(self) -> str:
        """
        Informational message to convey.
        """
        return self.__fMessage


    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        
        Returns:
            A string in the form of "InfoEventArgs: Message".
        """
        msg:str = UNKNOWN_VALUE

        if (self.__fMessage != None):
            msg = self.__fMessage

        return "InfoEventArgs: {0}".format(msg)


@export
class InfoEventHandler:
    """
    Event handler type for the SmartInspect.InfoEvent event.
    """

    def __init__(self, sender:object, e:InfoEventArgs) -> None:
        """
        Initializes a new instance of the class.

        Args:
            sender (object):
                The object which fired the event.
            e (InfoEventArgs):
                Arguments that contain detailed information related to the event.
        """
        pass
