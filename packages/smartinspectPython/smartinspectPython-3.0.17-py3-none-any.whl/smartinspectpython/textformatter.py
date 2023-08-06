"""
Module: textformatter.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

from io import BytesIO

# our package imports.
from .formatter import Formatter
from .binaryformatter import BinaryFormatter
from .patternparser import PatternParser
from .packet import Packet
from .packettype import PacketType

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class TextFormatter(Formatter):
    """
    Responsible for creating a text representation of a packet and
    writing it to a stream.

    This class creates a text representation of a packet and writes
    it to a stream. The representation can be influenced with the
    Pattern property. The Compile method preprocesses a packet and
    computes the required size of the packet. The Write method writes
    the preprocessed packet to the supplied stream.

    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """

        # initialize instance.
        self.__fLine = []
        self.__fParser:PatternParser = PatternParser()


    @property
    def Indent(self) -> bool:
        """ 
        Gets the Indent property value.

        Indicates if this formatter should automatically intend log
        packets like in the Views of the SmartInspect Console.

        Log Entry packets of type EnterMethod increase the indentation
        and packets of type LeaveMethod decrease it.
        """
        return self.__fParser.Indent
    
    @Indent.setter
    def Indent(self, value:bool) -> None:
        """ 
        Sets the Indent property value.
        """
        if value != None:
            self.__fParser.Indent = value


    @property
    def Pattern(self) -> str:
        """
        Gets the Pattern property value.

        Represents the pattern used to create a text representation
        of a packet.

        For detailed information of how a pattern string can look like,
        please have a look at the documentation of the PatternParser
        class, especially the PatternParser.Pattern property.
        """
        return self.__fParser.Pattern

    @Pattern.setter
    def Pattern(self, value:str) -> None:
        """
        Sets the Pattern property value.
        """
        self.__fParser.Pattern = value


    def Compile(self, packet:Packet) -> int:
        """
        Overridden. Preprocesses (or compiles) a packet and returns the
        required size for the compiled result.

        Args:
            packet (Packet):
                The packet to compile.

        Returns:
            The size for the compiled result.

        This method creates a text representation of the supplied
        packet and computes the required size. The resulting
        representation can be influenced with the Pattern property.
        To write a compiled packet, call the Write method. Please
        note that this method only supports LogEntry objects and
        ignores any other packet. This means, for packets other
        than LogEntry, this method always returns 0.
        """
        if (packet.PacketType == PacketType.LogEntry):
        
            line:str = self.__fParser.Expand(packet) + "\r\n"
            self.__fLine = BinaryFormatter._EncodeString(line)
            return len(self.__fLine)
        
        else:
        
            self.__fLine = None
            return 0


    def Write(self, stream:BytesIO) -> None:
        """
        Overridden. Writes a previously compiled packet to the supplied stream.
        
        Args:
            stream (BytesIO):
                The stream to write the packet to.

        Raises:
            IOException:
                An I/O error occurred while trying to write the compiled packet.

        This method writes the previously computed text representation
        of a packet (see Compile) to the supplied stream object.
        If the return value of the Compile method was 0, nothing is written.
        """
        if (self.__fLine != None):

            stream.write(self.__fLine)
