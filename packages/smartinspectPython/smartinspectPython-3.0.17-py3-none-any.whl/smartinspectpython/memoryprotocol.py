"""
Module: memoryprotocol.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

from io import BytesIO, BufferedWriter

# our package imports.
from .smartinspectexception import SmartInspectException
from .formatter import Formatter as FormatterSI
from .textformatter import TextFormatter
from .binaryformatter import BinaryFormatter
from .protocol import Protocol
from .fileprotocol import FileProtocol
from .connectionsbuilder import ConnectionsBuilder
from .packet import Packet
from .packetqueue import PacketQueue
from .protocolcommand import ProtocolCommand

# our package constants.
from .const import (
    TEXTFILE_HEADER_BOM,
    TEXTFILE_INDENT_DEFAULT,
    TEXTFILE_PATTERN_DEFAULT
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class MemoryProtocol(Protocol):
    """
    Used for writing log data to memory and saving it to a stream
    or another protocol object on request.
    To initiate such a request, use the InternalDispatch method.

    TextProtocol is used for writing plain text log files. This class is used when 
    the 'mem' protocol is specified in the SmartInspect.Connections. See the 
    IsValidOption method for a list of available protocol options.
    
    For a list of available protocol options, please refer to the
    IsValidOption method.

    Threadsafety:
        The public members of this class are thread-safe.
    """

    _DEFAULT_MAXSIZE:int = 2048
    _DEFAULT_ASTEXT:bool = False
    
    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        # initialize base classinstance.
        super().__init__()

        # initialize instance.
        self.__fMaxSize:int = MemoryProtocol._DEFAULT_MAXSIZE
        self.__fIndent:bool = TEXTFILE_INDENT_DEFAULT
        self.__fPattern:str = TEXTFILE_PATTERN_DEFAULT
        self.__fAsText:bool = MemoryProtocol._DEFAULT_ASTEXT
        self.__fFormatter:FormatterSI = None
        self.__fQueue:PacketQueue = None

        # set default options.
        self.LoadOptions()


    @property
    def Name(self) -> str:
        """ 
        Overridden.  Returns "mem".
        """
        return "mem"


    def __FlushToProtocol(self, protocol:Protocol) -> None:
        """
        Args:
            protocol (Protocol):
                The protocol object to flush to.

        References the specified protocol object to call its WritePacket method 
        for each packet in the internal packet queue.
        """
        # write the current content of our queue.
        if (self.__fQueue != None):
      
            packet:Packet = self.__fQueue.Pop()
            while (packet != None):
                protocol.WritePacket(packet)
                packet = self.__fQueue.Pop()


    def __FlushToStream(self, stream:BytesIO) -> None:
        """
        Args:
            stream (BytesIO):
                The stream object to flush to.

        References the specified stream object to call its formatters'
        Format method for each packet in the internal packet queue.
        The necessary header is written first and then the actual packets 
        are appended.

        The header and packet output format can be influenced with
        the "astext" protocol option (see IsValidOption). If the
        "astext" option is true, the header is a UTF8 Byte Order
        Mark and the packets are written in plain text format. If
        the "astext" option is false, the header is the standard
        header for SmartInspect log files and the packets are
        written in the default binary mode. In the latter case, the
        resulting log files can be loaded by the SmartInspect Console.
        """
        # write the necessary file header.
        if (self.__fAsText):
            stream.write(TEXTFILE_HEADER_BOM)
        else:
            stream.write(FileProtocol.SILF)

        # write the current content of our queue using the appropriate formatter.
        if (self.__fQueue != None):
      
            packet:Packet = self.__fQueue.Pop()
            while (packet != None):
                if (self.__fFormatter != None):
                    self.__fFormatter.Format(packet, stream)
                packet = self.__fQueue.Pop()


    def __InitializeFormatter(self) -> None:
        """
        Initializes formatter based upon the "astext" setting.
        """
        if (self.__fAsText):
        
            self.__fFormatter = TextFormatter()
            self.__fFormatter.Pattern = self.__fPattern
            self.__fFormatter.Indent = self.__fIndent
        
        else:
        
            self.__fFormatter = BinaryFormatter()


    def BuildOptions(self, builder:ConnectionsBuilder) -> None:
        """
        Overridden. Fills a ConnectionsBuilder instance with the
        options currently used by this protocol.

        Args:
            builder (ConnectionsBuilder):
                The ConnectionsBuilder object to fill with the current options
                of this protocol.
        """
        # build base class options.
        super().BuildOptions(builder)

        # build options specific to our class.
        builder.AddOptionInteger("maxsize", self.__fMaxSize / 1024)
        builder.AddOptionBool("astext", self.__fAsText)
        builder.AddOptionBool("indent", self.__fIndent)
        builder.AddOptionString("pattern", self.__fPattern)


    def InternalConnect(self) -> None:
        """
        Overridden. Creates and initializes the packet queue.

        This method creates and initializes a new packet queue with
        a maximum size as specified by the Initialize method. For
        other valid options which might affect the behavior of this
        method and protocol, please see the IsValidOption method.
        """
        self.__fQueue = PacketQueue()
        self.__fQueue.Backlog = self.__fMaxSize


    def InternalDisconnect(self):
        """
        Overridden.  Clears the internal queue of packets.

        This method does nothing more than to clear the internal
        queue of packets. After this method has been called, the
        InternalDispatch method writes an empty log unless new
        packets are queued in the meantime.
        """
        if (self.__fQueue != None):
        
            self.__fQueue.Clear()
            self.__fQueue = None


    def InternalDispatch(self, command:ProtocolCommand) -> None:
        """
        Overridden. Implements a custom action for saving the current
        queue of packets of this memory protocol to a stream or
        protocol object.

        Args:
            command (ProtocolCommand):
                The protocol command which is expected to provide the stream
                or protocol object.

        Raises:
            Exception:
                Writing the internal queue of packets to the supplied stream or protocol failed.

        Depending on the supplied command argument, this method does
        the following.

        If the supplied State object of the protocol command is of
        type Stream, then this method uses this stream to write the
        entire content of the internal queue of packets. The necessary
        header is written first and then the actual packets are
        appended.

        The header and packet output format can be influenced with
        the "astext" protocol option (see IsValidOption). If the
        "astext" option is true, the header is a UTF8 Byte Order
        Mark and the packets are written in plain text format. If
        the "astext" option is false, the header is the standard
        header for SmartInspect log files and the packets are
        written in the default binary mode. In the latter case, the
        resulting log files can be loaded by the SmartInspect Console.

        If the supplied State object of the protocol command is of
        type Protocol instead, then this method uses this protocol
        object to call its WritePacket method for each packet in the
        internal packet queue.

        The Action property of the command argument should currently
        always be set to 0. If the State object is not a stream or
        protocol command or if the command argument is null, then
        this method does nothing.
        """
        if (command == None):
            return

        # if supplied object is a protocol then flush queue contents to the protocol.
        if (issubclass(type(command.State), Protocol)):
            protocol:Protocol = command.State
            if (protocol != None):
                self.__FlushToProtocol(protocol)
            return

        # if supplied object is a stream then flush queue contents to stream.
        if (issubclass(type(command.State), BufferedWriter)):
            stream:BytesIO = command.State
            if (stream != None):
                self.__FlushToStream(stream)
            return

        # if none of the above then there is nothing to do!
        raise SmartInspectException("Dispatch State argument was neither a Protocol nor Stream type of object.")


    def InternalWritePacket(self, packet:Packet) -> None:
        """
        Overridden. Writes a packet to the packet queue.

        Args:
            packet (Packet):
                The packet to write.

        This method writes the supplied packet to the internal
        queue of packets. If the size of the queue exceeds the
        maximum size as specified by the Options property, the
        queue is automatically resized and older packets are
        discarded.
        """
        if (self.__fQueue != None):
            self.__fQueue.Push(packet)


    def IsValidOption(self, name:str) -> bool:
        """
        Overridden. Validates if a protocol option is supported.

        Args:
            name (str):
                The option name to validate.

        Returns:
            True if the option is supported and false otherwise.

        The following table lists all valid options, their default values and descriptions for the TEXT protocol.

        Valid Options (default value)              | Description
        ------------------------------------------ | ----------------------------------------------------------------------
        astext (false)                             | Specifies if logging data should be written as text instead of binary.
        indent (false)                             | Indicates if the logging output should automatically be indented like in the Console if 'astext' is set to true.
        maxsize (2048)                             | Specifies the maximum size of the packet queue of this protocol in kilobytes.  Specify size units like this: "1 MB".  Supported units are "KB", "MB" and "GB".
        pattern ("[%timestamp%] %level%: %title%") | Specifies the pattern used to create a text representation of a packet.
    
        If the "astext" option is used for creating a textual output instead of the default binary, the "pattern" string specifies
        the textual representation of a log packet. For detailed information of how a pattern string can look like, please
        have a look at the documentation of the PatternParser class, especially the PatternParser.Pattern property.

        Please note that this protocol DOES NOT support log data encryption.

        For further options which affect the behavior of this protocol, please have a look at the documentation of the
        Protocol.IsValidOption method of the parent class.

        <details>
            <summary>View Sample Code</summary>
        ```python
        from smartinspectpython.siauto import *  # SiAuto, Level, Session

        # the following are sample SI Connections options for this protocol.

        # log messages using all default options (binary log, no indent).
        SiAuto.Si.Connections = "mem()"

        # log messages using max packet queue size of 8 MB.
        SiAuto.Si.Connections = "mem(maxsize=\\"8MB\\")"

        # log messages using text instead of binary.
        SiAuto.Si.Connections = "mem(astext=true)"

        # log messages using indented text and a custom pattern.
        SiAuto.Si.Connections = "mem(astext=true, indent=true, pattern=\"%level% [%timestamp%]: %title%\")"
        ```
        """
        # encryption related options are NOT supported for memory logging.
        if ((name == "encrypt") or (name == "key")):
            return False

        return \
            (name == "maxsize") or \
            (name == "astext") or \
            (name == "pattern") or \
            (name == "indent") or \
            (super().IsValidOption(name))


    def LoadOptions(self) -> None:
        """
        Overridden. Loads and inspects specific options for this protocol.

        This method loads all relevant options and ensures their
        correctness. See IsValidOption for a list of options which
        are recognized by the protocol.
        """
        # load base class options.
        super().LoadOptions()

        # load options specific to our class.
        self.__fMaxSize = self.GetSizeOption("maxsize", MemoryProtocol._DEFAULT_MAXSIZE)
        self.__fAsText = self.GetBooleanOption("astext", MemoryProtocol._DEFAULT_ASTEXT)
        self.__fIndent = self.GetBooleanOption("indent", TEXTFILE_INDENT_DEFAULT)
        self.__fPattern = self.GetStringOption("pattern", TEXTFILE_PATTERN_DEFAULT)

        # initialize formatter based upon the "astext" option value.
        self.__InitializeFormatter()
