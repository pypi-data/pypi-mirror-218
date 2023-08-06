"""
Module: tcpprotocol.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  
| 2023/06/09 | 3.0.8.0     | Added call to RaiseInfoEvent for the SI Console Server banner.

</details>
"""

from io import BufferedRWPair, BytesIO
import socket

# our package imports.
from .smartinspectexception import SmartInspectException
from .formatter import Formatter
from .binaryformatter import BinaryFormatter
from .protocol import Protocol
from .connectionsbuilder import ConnectionsBuilder
from .packet import Packet

# our package constants.
from .const import (
    SERVER_BANNER_ERROR,
    CLIENT_BANNER
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class TcpProtocol(Protocol):
    """
    Used for sending packets to the SmartInspect Console over a TCP
    socket connection.
    
    This class is used for sending packets over a TCP connection to
    the Console. It is used when the 'tcp' protocol is specified in
    the SmartInspect.Connections property. Please see the IsValidOption 
    method for a list of available protocol options.
    

    For a list of available protocol options, please refer to the
    IsValidOption method.

    Threadsafety:
        The public members of this class are thread-safe.
    """
    
    _SERVER_ANSWER_SIZE:int = 2
    """ Expected server response length. """


    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """

        # initialize base classinstance.
        super().__init__()

        # initialize instance.
        self.__fSocket:socket = None
        self.__fStream:BytesIO = BytesIO()
        self.__fFormatter:Formatter = BinaryFormatter()
        self.__fAnswer:bytes("  ", 'ascii')
        self.__fTcpHostName:str = "127.0.0.1"
        self.__fTcpPort:int = 4228
        self.__fTcpTimeout:int = 30000

        # set default options.
        self.LoadOptions()


    @property
    def Name(self) -> str:
        """ 
        Overridden.  Returns "tcp".
        """
        return "tcp"


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

        n:int = 0
        serverBanner:str = ""

        # read the server banner from the Console. 
        #while ((n = self.__fStream.read(1)) != '\n'):
        while (n != -1):

            # read server response 1-byte at a time.
            n = stream.read(1)
            
            # any bytes read?  if not, then this indicates a failure on the server side.
            # doesn't make sense to proceed here.
            if (n == -1):
                raise SmartInspectException.Create(SERVER_BANNER_ERROR)

            # append the byte read to the server banner string.
            serverBanner += str(n, encoding='utf-8')

            # end of banner?
            if (n == b'\n'):
                break

        # notify event handler.
        self.RaiseInfoEvent("SI Console Server Banner: \"{0}\"".format(serverBanner.replace("\r\n","")))

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
        builder.AddOptionString("host", self.__fTcpHostName)
        builder.AddOptionInteger("port", self.__fTcpPort)
        builder.AddOptionInteger("timeout", self.__fTcpTimeout)


    def IsValidOption(self, name:str) -> bool:
        """
        Overridden. Validates if a protocol option is supported.

        Args:
            name (str):
                The option name to validate.

        Returns:
            True if the option is supported and false otherwise.

        The following table lists all valid options, their default
        values and descriptions for the TCP protocol.
        
        Valid Options (default value)  | Description
        -----------------------------  | -------------------------------------------------
        host ("127.0.0.1")             | Specifies the TCP host name or ip address that the SI Console is listening on.
        port (4228)                    | Specifies the TCP port number that the SI Console is listening on.
        timeout (30000)                | Specifies the connect, receive and send timeout in milliseconds.

        <details>
            <summary>View Sample Code</summary>
        ```python
        from smartinspectpython.siauto import *  # SiAuto, Level, Session

        # the following are sample SI Connections options for this protocol.

        # log messages using all default options (localhost, port 4228, 30s timeout).
        SiAuto.Si.Connections = "tcp()"

        # log messages using localhost, port 4228, 30s timeout, asynchronous processing.
        SiAuto.Si.Connections = "tcp(host=localhost,port=4228,timeout=30000,reconnect=true,reconnect.interval=10s,async.enabled=true)
        ```
        """
        return \
            (name == "host") or \
            (name == "port") or \
            (name == "timeout") or \
            (super().IsValidOption(name))


    def InternalConnect(self) -> None:
        """
        Overridden.  Creates and connects a TCP socket.

        This method tries to connect a TCP socket to a SmartInspect
        Console. The hostname and port can be specified by passing
        the "hostname" and "port" options to the Initialize method.
        Furthermore, it is possible to specify the connect timeout
        by using the "timeout" option.
        
        Raises:
            Exception:
                Creating or connecting the socket failed.
        """
        # create a new socket for this connection.
        self.__fSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set send / receive timeout, and connect to the server.
        self.__fSocket.settimeout(self.__fTcpTimeout / 1000.0)
        self.__fSocket.connect((self.__fTcpHostName, self.__fTcpPort))  # <- host and port has to be specified as tuple format - e.g. (host,port) 

        # get a reference to the socket buffer stream.
        self.__fStream = self.__fSocket.makefile('rwb', buffering=0x2000)

        # exchange banners with the console server.
        self.__DoHandShake(self.__fStream)

        # write a log header packet.
        self._WriteLogHeaderPacket() 


    def InternalDisconnect(self):
        """
        Overridden.  Closes the TCP socket connection.

        This method closes the underlying socket handle if previously
        created and disposes any supplemental objects.

        Raises:
            Exception:
                Closing the TCP socket failed.
        """
        if (self.__fStream.writable or self.__fStream.readable):
            self.__fStream.close()

        if (self.__fSocket != None):
            self.__fSocket.close()
            self.__fSocket = None


    def InternalWritePacket(self, packet:Packet):
        """
        Sends a packet to the Console.

        Args:
            packet (Packet):
                The packet to write.

        Raises:
            Exception:
                Sending the packet to the Console failed.

        This method sends the supplied packet to the SmartInspect
        Console and waits for a valid response.
        """
        if (not self.__fStream.writable):
            raise SmartInspectException("Underlying connection stream is no longer writeable, which indicates the connection no longer exists.")

        self.__fFormatter.Format(packet, self.__fStream)
        self.__fStream.flush()

        # read server response ("OK" if successful).
        self.__fAnswer = self.__fStream.read(TcpProtocol._SERVER_ANSWER_SIZE)
        if (len(self.__fAnswer) != TcpProtocol._SERVER_ANSWER_SIZE):
            raise SmartInspectException("Could not read server answer correctly: Connection has been closed unexpectedly.")


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
        self.__fTcpHostName = self.GetStringOption("host", "127.0.0.1")
        self.__fTcpPort = self.GetIntegerOption("port", 4228)
        self.__fTcpTimeout = self.GetIntegerOption("timeout", 30000)
