"""
Module: pipeprotocol.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  
| 2023/06/09 | 3.0.8.0     | Added call to RaiseInfoEvent for the SI Console Server banner.

</details>
"""

from io import BytesIO, BufferedRWPair
import platform

# our package imports.
from .smartinspectexception import SmartInspectException
from .pipehandle import PipeHandle
from .pipestream import PipeStream
from .protocol import Protocol
from .binaryformatter import BinaryFormatter
from .connectionsbuilder import ConnectionsBuilder
from .packet import Packet

# our package constants.
from .const import (
    CLIENT_BANNER,
    SERVER_BANNER_ERROR
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class PipeProtocol(Protocol):
    """
    Used for sending packets to a local SmartInspect Console over a
    named pipe connection.  This protocol only works on Windows-based
    systems, as it utilizes a Win32 API for named pipe access.
    
    This class is used for sending packets through a local named pipe
    to the SmartInspect Console. It is used when the 'pipe' protocol
    is specified in the SmartInspect.Connections.  Please see the 
    IsValidOption method for a list of available protocol options. 
    Please note that this protocol can only be used for local connections. 
    For remote connections to other machines, please use TcpProtocol.

    For a list of available protocol options, please refer to the
    IsValidOption method.

    Threadsafety:
        The public members of this class are thread-safe.
    """

    
    def __init__(self) -> None:
        """ 
        Initializes a new instance of the class.
        """

        # initialize the base class.
        super().__init__()

        # initialize instance.
        self.__fPipeName:str = ""
        self.__fPipeHandle:PipeHandle = None
        self.__fStream:PipeStream = None
        self.__fFormatter:BinaryFormatter = BinaryFormatter()

        # set default options.
        self.LoadOptions()


    @property
    def Name(self) -> str:
        """ 
        Overridden.  Returns "pipe".
        """
        return "pipe"


    def __DoHandShake(self, stream:BufferedRWPair):
        """
        Receives the SmartInspect console server banner, and sends our banner information in reply.

        Args:
            stream (BufferedRWPair):
                Stream to read the server banner from and reply to with our banner.

        Raises:
            SmartInspectException:
                Thrown if an error occurs during the handshake.
        
        Our banner information is displayed in the SI Console Connections log.
        """

        # read the server banner from the Console. 
        serverBanner:str = str(stream.read(0xff), 'utf-8')
           
        # any bytes read?  if not, then this indicates a failure on the server side.
        # doesn't make sense to proceed here.
        if ((serverBanner == None) or (len(serverBanner) == 0)):
            raise SmartInspectException.Create(SERVER_BANNER_ERROR)

        # notify event handler.
        self.RaiseInfoEvent("SI Console Server Banner: \"{0}\"".format(serverBanner.replace("\n","")))

        # send our client banner to the Console server.
        stream.write(str.format(CLIENT_BANNER, self.Name).encode('ascii'))
        stream.flush()


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
        builder.AddOptionString("pipename", self.__fPipeName)


    def InternalConnect(self) -> None:
        """
        Overridden.  Connects to the specified local named pipe.
        
        Raises:
            ProtocolException:
                Establishing the named pipe connection failed.

        This method tries to establish a connection to a local named
        pipe of a SmartInspect Console. 
        """
        # platform check - pipe protocol is only good for Windows platform!
        osname:str = platform.system()
        if (osname != None):
            if (osname.lower() != "windows"):
                raise SmartInspectException("PipeProtocol can only be used with the Windows Operating System.  Use TcpProtocol for other platforms.")

        # open the named pipe and create the stream to read from / write to.
        self.__fPipeHandle:PipeHandle = PipeHandle(self.__fPipeName)
        self.__fStream = PipeStream(self.__fPipeHandle.Handle)

        # exchange banners with the console server.
        self.__DoHandShake(self.__fStream)

        # write a log header packet.
        self._WriteLogHeaderPacket() 


    def InternalDisconnect(self) -> None:
        """
        Overridden.  Closes the connection to the specified local named pipe.
        
        Raises:
            ProtocolException:
                Closing the named pipe handle failed.

        This method closes the named pipe handle if previously created
        and disposes any supplemental objects.
        """
        if (self.__fStream != None):
            if (self.__fStream.writable() or self.__fStream.readable()):
                self.__fStream.close()


    def InternalReconnect(self) -> bool:
        """
        Tries to reconnect to the specified local named pipe.

        Returns:
            True if the reconnect attempt has been successful and false otherwise.

        This method tries to re-establish a connection to the local
        named pipe of a SmartInspect Console. 
        """
        # just call InternalConnect to reconnect for named pipe server.
        self.InternalConnect()

        # indicate reconnect was successful.
        return True


    def InternalWritePacket(self, packet:Packet) -> None:
        """
        Sends a packet to the Console.

        Args:
            packet (Packet):
                The packet to write.

        Raises:
            Exception:
                Sending the packet to the Console failed.

        This method sends the supplied packet to the SmartInspect
        Console over the previously established named pipe connection.
        """
        if (not self.__fStream.writable):
            raise SmartInspectException("Underlying connection stream is no longer writeable, which indicates the connection no longer exists.")

        self.__fFormatter.Format(packet, self.__fStream)
        self.__fStream.flush()


    def IsValidOption(self, name:str) -> bool:
        """
        Overridden. Validates if a protocol option is supported.

        Args:
            name (str):
                The option name to validate.

        Returns:
            True if the option is supported and false otherwise.

        The following table lists all valid options, their default
        values and descriptions for the PIPE protocol.
        
        Valid Options (default value)  | Description
        -----------------------------  | -------------------------------------------------
        - pipename ("smartinspect")    | Specifies the named pipe for sending log packets to the SmartInspect Console.  This value must match the pipe name in the SmartInspect Console options.

        <details>
            <summary>View Sample Code</summary>
        ```python
        from smartinspectpython.siauto import *  # SiAuto, Level, Session

        # the following are sample SI Connections options for this protocol.

        # log messages to SI Console using all default options (pipename=smartinspect).
        SiAuto.Si.Connections = "pipe()"

        # log messages to SI Console using pipe name "sipipe", with asyncronous send enabled.
        SiAuto.Si.Connections = "pipe(pipename=sipipe,reconnect=true,reconnect.interval=10s,async.enabled=true)
        ```
        """
        return \
            (name == "pipename") or \
            (super().IsValidOption(name))


    def LoadOptions(self) -> None:
        """
        Overridden. Loads and inspects specific options for this protocol.

        This method loads all relevant options and ensures their
        correctness. See IsValidOption for a list of options which
        are recognized by this protocol.
        """
        # load base class options.
        super().LoadOptions()

        # load options specific to our class.
        self.__fPipeName = self.GetStringOption("pipename", "smartinspect");
