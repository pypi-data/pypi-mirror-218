"""
Module: processfloweventargs.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .processflow import ProcessFlow

# our package constants.
from .const import (
    UNKNOWN_VALUE
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class ProcessFlowEventArgs:
    """
    This class is used by the SmartInspect.ProcessFlow event.

    It has only one public class member named ProcessFlow. This
    member is a property, which just returns the sent packet.

    Threadsafety:
        This class is fully thread-safe.
    """

    def __init__(self, processFlow:ProcessFlow) -> None:
        """
        Initializes a new instance of the class.

        Args:
            processFlow (ProcessFlow):
                The Process Flow packet which caused the event.
        """

        # initialize instance.
        self.__fProcessFlow:ProcessFlow = processFlow


    @property
    def ProcessFlow(self) -> ProcessFlow:
        """
        Returns the ProcessFlow packet, which has just been sent.
        """
        return self.__fWatch


    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        
        Returns:
            A string in the form of "ProcessFlowEventArgs: Type=X, Level=X, Title=\"X\"
        """
        argsType:str = UNKNOWN_VALUE
        title:str = UNKNOWN_VALUE
        level:str = UNKNOWN_VALUE

        if (self.__fProcessFlow != None):
            argsType = self.__fProcessFlow.ProcessFlowType.name
            title = self.__fProcessFlow.Title
            level = self.__fProcessFlow.Level.name

        return str.format("ProcessFlowEventArgs: Type={0}, Level={1}, Title=\"{2}\"", argsType, level, title)


@export
class ProcessFlowEventHandler:
    """
    This is the event handler type for the SmartInspect.ProcessFlowEvent event.
    """

    def __init__(self, sender:object, e:ProcessFlowEventArgs) -> None:
        """
        Initializes a new instance of the class.

        Args:
            sender (object):
                The object which fired the event.
            e (ProcessFlowEventArgs):
                Arguments that contain detailed information related to the event.
        """
