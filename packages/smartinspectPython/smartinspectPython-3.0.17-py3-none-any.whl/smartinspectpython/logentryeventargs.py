"""
Module: logentryeventargs.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .logentry import LogEntry

# our package constants.
from .const import (
    UNKNOWN_VALUE
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class LogEntryEventArgs:
    """
    This class is used by the SmartInspect.LogEntry event.
    
    It has only one public class member named LogEntry. This member
    is a property, which just returns the sent packet.

    Threadsafety:
        This class is fully thread-safe.
    """

    def __init__(self, logEntry:LogEntry) -> None:
        """
        Initializes a new instance of the class.

        Args:
            logEntry (LogEntry):
                The Log Entry packet which caused the event.
        """

        # initialize instance.
        self.__fLogEntry:LogEntry = logEntry


    @property
    def LogEntry(self) -> LogEntry:
        """
        Returns the LogEntry packet, which has just been sent.
        """
        return self.__fLogEntry


    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        
        Returns:
            A string in the form of "LogEntryEventArgs: Type=X, Level=X, Title=\"X\".
        """
        argsType:str = UNKNOWN_VALUE
        title:str = UNKNOWN_VALUE
        level:str = UNKNOWN_VALUE

        if (self.__fLogEntry != None):
            argsType = self.__fLogEntry.LogEntryType.name
            title = self.__fLogEntry.Title
            level = self.__fLogEntry.Level.name

        return str.format("LogEntryEventArgs: Type={0}, Level={1}, Title=\"{2}\"", argsType, level, title)


@export
class LogEntryEventHandler:
    """
    This is the event handler type for the SmartInspect.LogEntryEvent event.
    """

    def __init__(self, sender:object, e:LogEntryEventArgs) -> None:
        """
        Initializes a new instance of the class.

        Args:
            sender (object):
                The object which fired the event.
            e (LogEntryEventArgs):
                Arguments that contain detailed information related to the event.
        """
