"""
Module: binaryformatter.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

from io import BytesIO
from datetime import datetime
import struct

# our package imports.
from .formatter import Formatter
from .packet import Packet
from .packettype import PacketType
from .controlcommand import ControlCommand
from .logheader import LogHeader
from .logentry import LogEntry
from .processflow import ProcessFlow
from .watch import Watch
from .color import Color

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class BinaryFormatter(Formatter):
    """
    Responsible for formatting and writing a packet in the standard
    SmartInspect binary format.

    This class formats and writes a packet in the standard binary
    format which can be read by the SmartInspect Console. The
    Compile method preprocesses a packet and computes the required
    size of the packet. The Write method writes the preprocessed
    packet to the supplied stream.

    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    MAX_STREAM_CAPACITY:int = 10 * 1024 * 1024
    MAX_BUFFER_SIZE:int = 8192

    TICKS_EPOCH:int = 621355968000000000   # number of seconds since 01/01/1970 (epoch date)
    MICROSECONDS_PER_DAY:int = 86400000000 # number of microseconds in 1 day
    DAY_OFFSET_DELPHI_DEFAULT:int = 25569  # number of days between 01/01/1970 (epoch date) and 12/30/1899 (Delphi default date)

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """

        # initialize instance.
        self.__fSize:int = 0
        self.__fBuffer:BytesIO = BytesIO(bytes(BinaryFormatter.MAX_BUFFER_SIZE))
        self.__fStream:BytesIO = BytesIO()
        self.__fPacket:Packet = None


    def _CompileControlCommand(self) -> None:
        """
        Compiles a ControlCommand packet, writing the packet's data to the data stream.
        """

        controlCommand:ControlCommand = self.__fPacket

        self._WriteInt(controlCommand.ControlCommandType.value)
        self._WriteStreamLength(controlCommand.Data)

        if controlCommand.HasData:
            self._CopyStream(self.__fStream, controlCommand.Data, controlCommand.DataLength)


    def _CompileLogEntry(self) -> None:
        """
        Compiles a LogEntry packet, writing the packet's data to the data stream.
        """

        logEntry:LogEntry = self.__fPacket

        appName:bytes = BinaryFormatter._EncodeString(logEntry.AppName)
        sessionName:bytes = BinaryFormatter._EncodeString(logEntry.SessionName)
        title:bytes = BinaryFormatter._EncodeString(logEntry.Title)
        hostName:bytes = BinaryFormatter._EncodeString(logEntry.HostName)

        self._WriteInt(logEntry.LogEntryType.value)
        self._WriteInt(logEntry.ViewerId.value)
        self._WriteDataLength(appName)
        self._WriteDataLength(sessionName)
        self._WriteDataLength(title)
        self._WriteDataLength(hostName)
        self._WriteStreamLength(logEntry.Data)
        self._WriteUInt(logEntry.ProcessId)
        self._WriteUInt(logEntry.ThreadId)
        self._WriteTimestamp(logEntry.Timestamp)
        self._WriteColor(logEntry.ColorBG)
        self._WriteData(appName)
        self._WriteData(sessionName)
        self._WriteData(title)
        self._WriteData(hostName)

        if logEntry.HasData:
            self._CopyStream(self.__fStream, logEntry.Data, logEntry.DataLength)


    def _CompileLogHeader(self) -> None:
        """
        Compiles a LogHeader packet, writing the packet's data to the data stream.
        """

        logHeader:LogHeader = self.__fPacket

        content = BinaryFormatter._EncodeString(logHeader.Content)
        self._WriteDataLength(content)
        self._WriteData(content)


    def _CompileProcessFlow(self) -> None:
        """
        Compiles a ProcessFlow packet, writing the packet's data to the data stream.
        """

        processFlow:ProcessFlow = self.__fPacket

        title:bytes = BinaryFormatter._EncodeString(processFlow.Title)
        hostname:bytes = BinaryFormatter._EncodeString(processFlow.HostName)

        self._WriteInt(processFlow.ProcessFlowType.value)
        self._WriteDataLength(title)
        self._WriteDataLength(hostname)
        self._WriteInt(processFlow.ProcessId)
        self._WriteInt(processFlow.ThreadId)
        self._WriteTimestamp(processFlow.Timestamp)
        self._WriteData(title)
        self._WriteData(hostname)


    def _CompileWatch(self) -> None:
        """
        Compiles a Watch packet, writing the packet's data to the data stream.
        """

        watch:Watch = self.__fPacket

        name:bytes = BinaryFormatter._EncodeString(watch.Name)
        value:bytes = BinaryFormatter._EncodeString(watch.Value)

        self._WriteDataLength(name)
        self._WriteDataLength(value)
        self._WriteInt(watch.WatchType.value)
        self._WriteTimestamp(watch.Timestamp)
        self._WriteData(name)
        self._WriteData(value)


    def _CopyStream(self, toStream, fromStream, count) -> None:
        """
        Copies bytes from one stream to another.
        """
        # reset from stream position to zero
        fromStreamPos:int = fromStream.tell()
        fromStream.seek(0)

        while (count > 0):

            toRead:int = 0

            # set # of bytes to copy - limit max to size of our buffer.
            if (count > BinaryFormatter.MAX_BUFFER_SIZE):
                toRead = BinaryFormatter.MAX_BUFFER_SIZE
            else:
                toRead = count

            # copy bytes from the FROM stream to our temporary buffer.
            self.__fBuffer = fromStream.read(toRead)

            # copy bytes from temporary buffer to the TO stream.
            if (toRead > 0):
                bytesWritten:int = toStream.write(self.__fBuffer)
                count = count - toRead
            else:
                break


    @staticmethod
    def _EncodeString(value:str) -> bytes:
        """
        Encodes a string with UTF-8 encoding, returning a byte array.
        """
        if (value != None):
            return value.encode('utf-8')
        else:
            return None


    @staticmethod
    def _EncodeStringAscii(value:str) -> bytes:
        """
        Encodes a string with ASCII encoding, returning a byte array.
        """
        if (value != None):
            return value.encode('ascii')
        else:
            return None


    def _ResetStream(self) -> None:

        if self.__fSize > BinaryFormatter.MAX_STREAM_CAPACITY:
            # Reset the stream capacity if the previous packet
            # was very big. This ensures that the amount of memory
            # can shrink again after a big packet has been sent.
            self.__fStream.truncate(0)
        else:
            # Only reset the position. This should ensure better
            # performance since no reallocations are necessary.
            self.__fStream.seek(0)


    def _WriteColor(self, value:Color) -> None:
        """
        Store color as Delphi Integer (32bit signed, little endian).
        """
        colorValue:int = value.R | value.G << 8 | value.B << 16 | value.A << 24
        self._WriteInt(colorValue)


    def _WriteData(self, value:bytes) -> None:
        """
        Store byte array.
        """
        if (value != None):
            self.__fStream.write(value)


    def _WriteDataLength(self, value:bytes) -> None:
        """
        Store length of byte array as Delphi Integer (32bit signed, little endian).
        """
        if (value != None):
            self._WriteInt(len(value))
        else:
            self._WriteInt(0)


    def _WriteDouble(self, value:float) -> None:
        """
        Store as Delphi Integer (64bit unsigned, little endian) to internal stream.
        """
        self._WriteDoubleToStream(self.__fStream, value)


    def _WriteDoubleToStream(self, stream:BytesIO, value:float) -> None:
        """
        Store as Delphi Double (64bit signed, little endian) to specified stream.
        """
        stream.write(struct.pack('<d', value))


    def _WriteInt(self, value:int) -> None:
        """
        Store as Delphi Integer (32bit signed, little endian) to internal stream.
        """
        self._WriteIntToStream(self.__fStream, value)


    def _WriteIntToStream(self, stream:BytesIO, value:int) -> None:
        """
        Store as Delphi Integer (32bit signed, little endian) to specified stream.
        """
        # ensure we don't exceed the size range for 4 bytes of data!
        # this can happen for ThreadId and ProcessId values!
        if (value >= -2147483647) and (value <= 2147483648):
            stream.write(struct.pack('<l', value))
        elif (value >= 0) and (value <= 4294967295):
            stream.write(struct.pack('<L', value))
        else:
            # value would exceed the byte size the console is expecting - zero it out!
            stream.write(struct.pack('<L', 0))


    def _WriteShort(self, value:int) -> None:
        """
        Store as Delphi Word (16bit unsigned, little endian).
        """
        self._WriteShortToStream(self.__fStream, value)


    def _WriteShortToStream(self, stream:BytesIO, value:int) -> None:
        """
        Store as Delphi Word (16bit unsigned, little endian) to specified stream.
        """
        stream.write(struct.pack('<H', value))


    def _WriteStreamLength(self, value:BytesIO) -> None:
        """
        Store length of stream as Delphi Integer (32bit signed, little endian).
        """
        if (value != None):
            self._WriteInt(value.getbuffer().nbytes)
        else:
            self._WriteInt(0)


    def _WriteTimestamp(self, value:datetime) -> None:
        """
        Store as Delphi TDatetime (8-byte double, little endian).
        """

        # Calculate current time-stamp:
        # A time-stamp is represented by a double. The integral
        # part of the from is the number of days that have
        # passed since 12/30/1899. The fractional part of the
        # from is the fraction of a 24 hour day that has elapsed.

        # Delphi is expecting a timestamp that is calculated from Delphi default time, which
        # is the number of seconds from a starting date of 12/30/1899.

        us:int = 0
        timestamp:float = 0
        timestamp2:float = 0

        # convert datetime value to raw ticks (# seconds since 1/1/0001).
        ticks:float = (value - datetime(1, 1, 1)).total_seconds() * 10000000

        # convert raw ticks value to epoch ticks (# seconds since 1/1/1970).
        us = int((ticks - BinaryFormatter.TICKS_EPOCH) / 10)

        # convert epoch ticks to Delphi default date ticks (# seconds since 12/30/1899).
        timestamp = int(us / BinaryFormatter.MICROSECONDS_PER_DAY + BinaryFormatter.DAY_OFFSET_DELPHI_DEFAULT)
        timestamp2 = timestamp + float((us % BinaryFormatter.MICROSECONDS_PER_DAY) / BinaryFormatter.MICROSECONDS_PER_DAY)

        # write timestamp to data stream.
        self._WriteDouble(timestamp2)


    def _WriteUInt(self, value:int) -> None:
        """
        Store as Delphi Cardinal (32bit unsigned, little endian).
        """
        #self.__fStream.write(struct.pack('<L', value))
        self._WriteIntToStream(self.__fStream, value)
    

    def Compile(self, packet:Packet) -> int:
        """
        Overridden. Preprocesses (or compiles) a packet and returns the
        required size for the compiled result.

        Args:
            packet
                The packet to compile.

        Returns:
            The size for the compiled result.

        This method preprocesses the supplied packet and computes the
        required binary format size. To write this compiled packet,
        call the Write method.
        """

        self._ResetStream()
        self.__fPacket = packet

        if packet.PacketType is PacketType.LogEntry:
            self._CompileLogEntry()
        elif packet.PacketType is PacketType.LogHeader:
            self._CompileLogHeader()
        elif packet.PacketType is PacketType.Watch:
            self._CompileWatch()
        elif packet.PacketType is PacketType.ControlCommand:
            self._CompileControlCommand()
        elif packet.PacketType is PacketType.ProcessFlow:
            self._CompileProcessFlow()

        self.__fSize = self.__fStream.tell()
        return self.__fSize + Packet.PACKET_HEADER_SIZE


    def Write(self, stream:BytesIO) -> None:
        """
        Overridden. Writes a previously compiled packet to the supplied stream.
        
        Args:
            stream
                The stream to write the packet to.

        Raises:
            IOException
                An I/O error occurred while trying to write the compiled packet.

        This method writes the previously compiled packet (see Compile)
        to the supplied stream object. If the return value of the
        Compile method was 0, nothing is written.
        """

        if (self.__fSize > 0):
            self._WriteShortToStream(stream, int(self.__fPacket.PacketType.value))
            self._WriteIntToStream(stream, self.__fSize)
            self._CopyStream(stream, self.__fStream, self.__fSize)
