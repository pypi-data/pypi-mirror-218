"""
Module: watcheventargs.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .watch import Watch

# our package constants.
from .const import (
    UNKNOWN_VALUE
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class WatchEventArgs:
    """
    This class is used by the SmartInspect.WatchEvent event.

    Threadsafety:
        This class is fully thread-safe.
    """

    def __init__(self, watch:Watch) -> None:
        """
        Initializes a new instance of the class.

        Args:
            watch (Watch):
                The Watch item that was processed.
        """

        # initialize instance.
        self.__fWatch:Watch = watch


    @property
    def Watch(self) -> Watch:
        """
        Returns the Watch item that was processed.
        """
        return self.__fWatch


    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        
        Returns:
            A string in the form of "WatchEventArgs: Type=X, Level=X, Name=\"X\", Value=\"X\""
        """
        argsType:str = UNKNOWN_VALUE
        name:str = UNKNOWN_VALUE
        level:str = UNKNOWN_VALUE
        value:str = UNKNOWN_VALUE

        if (self.__fWatch != None):
            argsType = self.__fWatch.WatchType.name
            level = self.__fWatch.Level.name
            name = self.__fWatch.Name
            value = self.__fWatch.Value

        return str.format("WatchEventArgs: Type={0}, Level={1}, Name=\"{2}\", Value=\"{3}\"", argsType, level, name, value)


@export
class WatchEventHandler:
    """
    This is the event handler type for the SmartInspect.WatchEvent event.
    """

    def __init__(self, sender:object, e:WatchEventArgs) -> None:

        """
        Initializes a new instance of the class.

        Args:
            sender (object):
                The object which fired the event.
            e (WatchEventArgs):
                Arguments that contain detailed information related to the event.
        """
        pass
