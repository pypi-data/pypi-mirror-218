"""
Module: controlcommand.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

from io import BytesIO
from copy import copy

# our package imports.
from .packet import Packet
from .packettype import PacketType
from .controlcommandtype import ControlCommandType as SIControlCommandType
from .level import Level

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class ControlCommand(Packet):
    """
    Represents the Control Command packet type which is used for
    administrative tasks like resetting or clearing the Console.

    A Control Command can be used for several administrative Console
    tasks. Among other things, this packet type allows you to Session.ClearAll.

    Threadsafety:
        This class is not guaranteed to be thread-safe. However, instances
        of this class will normally only be used in the context of a single thread.
    """

    HEADER_SIZE:int = 8

    def __init__(self, controlCommandType:SIControlCommandType) -> None:
        """ 
        Initializes a new ControlCommand instance with a custom control command type.

        Args:
            controlCommandType (SIControlCommandType):
                The type of the new Control Command describes the way the
                Console interprets this packet. Please see the ControlCommandType
                enum for more information.
        """

        # initialize the base class.
        super().__init__()

        self.__fData:BytesIO = BytesIO()
        self.__fControlCommandType:SIControlCommandType = controlCommandType
        self.Level =Level.Control


    @property
    def ControlCommandType(self) -> SIControlCommandType:
        """ 
        Gets the ControlCommandType property value.

        The type of the Control Command describes the way the Console
        interprets this packet. Please see the ControlCommandType enum
        for more information.
        """
        return self.__fControlCommandType
    
    @ControlCommandType.setter
    def ControlCommandType(self, value:ControlCommandType) -> None:
        """ 
        Sets the ControlCommandType property value.
        """ 
        if value != None:
            self.__fControlCommandType = value


    @property
    def Data(self) -> BytesIO:
        """
        Gets the Data property value.

        This property contains an optional data stream of the Control Command.
        This property can be null if this Control Command does not
        contain additional data.

        <b>Important:</b> Treat this stream as read-only. This means,
        modifying this stream in any way is not supported. Additionally,
        only pass streams which support seeking. Streams which do not
        support seeking cannot be used by this class.
        """
        return self.__fData

    @Data.setter
    def Data(self, value:BytesIO) -> None:
        """ 
        Sets the Data property value.
        """
        if value:
            self.__fData = copy(value)
        else:
            self.__fData.truncate(0)


    @property
    def DataLength(self) -> int:
        """
        Returns the number of bytes used in the Data property.
        Note that this is the actual # of bytes used, and not the # of bytes allocated!
        """
        if (self.__fData != None):
            return self.__fData.getbuffer().nbytes
        return 0


    @property
    def HasData(self) -> bool:
        """
        Returns true if this packet contains optional data; otherwise, false.
        """
        if (self.__fData != None) & (self.__fData.getbuffer().nbytes > 0):
            return True
        return False


    @property
    def PacketType(self) -> PacketType:
        """ 
        Overridden.  Returns PacketType.ControlCommand
        """
        return PacketType.ControlCommand


    @property
    def Size(self) -> int:
        """
        Overridden.  Returns the total occupied memory size of this Control Command packet.

        The total occupied memory size of this Control Command is
        the size of memory occupied the optional Data stream and any
        internal data structures of this Control Command.
        """
        result = (self.HEADER_SIZE)

        if self.HasData:
            result += self.__fData.getbuffer().nbytes
        return result
