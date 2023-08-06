"""
Module: logheader.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""


# our package imports.
from .packet import Packet
from .packettype import PacketType

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class LogHeader(Packet):
    """ 
    Represents the Log Header packet type which is used for storing
    and transferring log metadata.
    
    The LogHeader class is used to store and transfer log metadata.
    After the PipeProtocol or TcpProtocol has established a connection,
    a Log Header packet with the metadata of the current logging
    context is created and written. Log Header packets are used by
    the SmartInspect Router application for its filter and trigger
    functionality.
    
    Threadsafety:
        This class is not guaranteed to be thread-safe. However, instances
        of this class will normally only be used in the context of a single thread.
    """

    _HEADER_SIZE:int = 4

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """

        # initialize the base class.
        super().__init__()

        # initialize instance.
        self.__fHostName:str = ''
        self.__fAppName:str = ''


    @property
    def AppName(self) -> str:
        """ 
        Gets the AppName property value.

        Represents the application name of this Log Header.

        The application name of a Log Header is usually set to the
        name of the application this Log Header is created in.
        """
        return self.__fAppName
    
    @AppName.setter
    def AppName(self, value:str) -> None:
        """ 
        Sets the AppName property value.
        """
        if value != None:
            self.__fAppName = value


    @property
    def Content(self) -> str:
        """
        Gets the Content property value.

        Represents the entire content of this Log Header packet.

        The content of a Log Header packet is a key-value (syntax:
        key=value) list of the properties of this Log Header packet
        (currently only the AppName and the HostName strings).
        Key-value pairs are separated by carriage return and newline
        characters.
        """
        return str.format("hostname={0}\r\nappname={1}\r\n", self.__fHostName, self.__fAppName)


    @property
    def HostName(self) -> str:
        """ 
        Gets the HostName property value.

        Represents the hostname of this Log Header.

        The hostname of a Log Header is usually set to the name of
        the machine this Log Header is sent from.
        """
        return self.__fHostName
    
    @HostName.setter
    def HostName(self, value:str) -> None:
        """ 
        Sets the HostName property value.
        """
        if value != None:
            self.__fHostName = value


    @property
    def PacketType(self) -> PacketType:
        """ 
        Overridden.  Returns PacketType.LogHeader. 
        """
        return PacketType.LogHeader


    @property
    def Size(self) -> int:
        """ 
        Overridden. Returns the total occupied memory size of this Log Header packet (including header length).
        
        The total occupied memory size of this Log Header is the size
        of memory occupied by all strings and any internal data
        structures of this Log Header.  Also note that the data
        is in UTF-8 encoding, so it takes up twice the storage as
        ASCII encoding.
        """
        result:int = (self._HEADER_SIZE +
                    Packet.GetStringSize(self.Content))
        return result
