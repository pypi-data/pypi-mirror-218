"""
Module: filtereventargs.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .packet import Packet

# our package constants.
from .const import (
    UNKNOWN_VALUE
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class FilterEventArgs:
    """
    This class is used by the SmartInspect.Filter event.

    Threadsafety:
        This class is fully thread-safe.
    """
    def __init__(self, packet:Packet) -> None:
        """
        Initializes a new instance of the class.

        Args:
            packet (Packet):
                The packet which caused the event.
        """

        # initialize instance.
        self.__fCancel:bool = False
        self.__fPacket:Packet = packet


    @property
    def Packet(self) -> Packet:
        """
        This read-only property returns the packet, which caused
        the event.
        """
        return self.__fPacket


    @property
    def Cancel(self) -> bool:
        """ 
        Gets the Cancel property value.

        This property can be used to cancel the processing of certain
        packets during the SmartInspect.Filter event.
        """
        return self.__fCancel
    

    @Cancel.setter
    def Cancel(self, value:bool) -> None:
        """ 
        Sets the Cancel property value.
        """
        if value != None:
            self.__fCancel = value


    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        
        Returns:
            A string in the form of "FilterEventArgs: PacketType=X, Size=N".
        """
        argsType:str = UNKNOWN_VALUE
        size:int = 0

        if (self.__fPacket != None):
            argsType = self.__fPacket.PacketType.name
            size = self.__fPacket.Size

        return str.format("FilterEventArgs: PacketType={0}, Size={1}", argsType, size)


@export
class FilterEventHandler:
    """
    This is the event handler type for the SmartInspect.Filter event.
    """

    def __init__(self, sender:object, e:FilterEventArgs) -> None:
        """
        Initializes a new instance of the class.

        Args:
            sender (object):
                The object which fired the event.
            e (FilterEventArgs):
                Arguments that contain detailed information related to the event,
                and canceling of its processing.
        """
