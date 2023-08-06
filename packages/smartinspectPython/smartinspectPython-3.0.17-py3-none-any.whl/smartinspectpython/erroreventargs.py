"""
Module: erroreventargs.py

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
class ErrorEventArgs:
    """
    Arguments passed to the SmartInspect.ErrorEvent event.

    It has only one public class member named Exception. This member
    is a property, which just returns the occurred exception.

    Threadsafety:
        This class is fully thread-safe.
    """

    def __init__(self, e:Exception) -> None:
        """
        Initializes a new instance of the class.

        Args:
            e (Exception):
                Exception that caused the event.
        """

        # initialize instance.
        self.__fException:Exception = e


    @property
    def Exception(self) -> Exception:
        """
        Exception that caused the event.
        """
        return self.__fException


    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        
        Returns:
            A string in the form of "ErrorEventArgs: Exception Message".
        """
        exMsg:str = UNKNOWN_VALUE

        if (self.__fException != None):
            exMsg = str(self.__fException)

        return "ErrorEventArgs: {0}".format(exMsg)


@export
class ErrorEventHandler:
    """
    Event handler type for the SmartInspect.ErrorEvent event.
    """

    def __init__(self, sender:object, e:ErrorEventArgs) -> None:
        """
        Initializes a new instance of the class.

        Args:
            sender (object):
                The object which fired the event.
            e (ErrorEventArgs):
                Arguments that contain detailed information related to the event.
        """
        pass
