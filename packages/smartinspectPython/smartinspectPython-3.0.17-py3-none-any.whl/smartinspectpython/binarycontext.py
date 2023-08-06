"""
Module: binarycontext.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

from io import BytesIO, BufferedReader

# our package imports.
from .dotnetcsharp import ArgumentNullException
from .viewercontext import ViewerContext
from .viewerid import ViewerId

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class BinaryContext(ViewerContext):
    """ 
    This is the base class for all viewer contexts which deal with
    binary data. A viewer context is the library-side representation
    of a viewer in the Console.

    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    def __init__(self, vi:ViewerId) -> None:
        """
        Initializes a new instance of the class.

        Args:
            vi (ViewerId):
                The viewer ID to use.
        """

        # initialize base instance.
        super().__init__(vi)

        # initialize instance.
        self.__fData:BytesIO = BytesIO()


    @property
    def ViewerData(self) -> BytesIO:
        """ 
        Overridden. Returns the actual binary data which will be
        displayed in the viewer specified by the ViewerId.
        """
        return self.__fData


    def __InternalLoadFromStream(self, stream:BufferedReader) -> None:
        """
        Reads all bytes from the stream in 8192 byte chunks, and writes
        them to the internal buffer.

        Args:
            stream (BufferedReader):
                The stream to read from.
        """
        n:int = 0
        buffertmp = bytes(0x2000)

        self.ResetData()
        while True:
            buffertmp = stream.read(len(buffertmp))
            if (len(buffertmp) > 0):
                self.__fData.write(buffertmp)
            else:
                break


    def AppendBytes(self, buffer:bytes) -> None:
        """
        Appends a buffer of data to the stream.

        Args:
            buffer (bytes):
                The buffer to append.
        
        Raises:
            ArgumentNullException:
                The buffer argument is null.
        """
        if (buffer == None):
            raise ArgumentNullException("buffer")
        
        self.__fData.write(buffer)


    def AppendBytesWithOffset(self, buffer:bytes, offset:int, count:int) -> None:
        """
        Appends a buffer of data to the stream, specifying the offset in
        the buffer and the amount of bytes to append.

        Args:
            buffer (bytes):
                The buffer to append.
            offset (int):
                The offset at which to begin appending.
            count (int):
                The number of bytes to append.

        Raises:
            ArgumentNullException:
                The buffer argument is null
            ArgumentException:
                The sum of the offset and count parameters is greater than the actual buffer length.
            ArgumentOutOfRangeException:
                The offset or count parameter is negative.
        """
        if (buffer == None):
            raise ArgumentNullException("buffer")
        
        self.__fData.write(buffer[offset:count])


    def Dispose(self, disposing:bool) -> None:
        """
        Releases any resources.

        Args:
            disposing (bool):
                True if managed resources should be released and false otherwise.
        """
        if (disposing):
            self.ResetData()


    def LoadFromFile(self, fileName:str) -> None:
        """
        Loads the binary data from a file.

        Args:
            fileName (str):
                The name of the file to load the binary data from.

        Raises:
            ArgumentNullException:
                The filename argument is null.
            IOException:
                An I/O error occurred.
        """
        if (fileName == None):
            raise ArgumentNullException("fileName")

        with open(fileName, 'rb') as reader:

            self.__InternalLoadFromStream(reader)


    def LoadFromStream(self, stream:BytesIO) -> None:
        """
        Loads the binary data from a stream.
        
        Args:
            stream (BytesIO):
                The stream to load the binary data from.

        Raises:
            ArgumentNullException:
                The stream argument is null.
            IOException:
                An I/O error occurred.
        
        If the supplied stream supports seeking then the entire
        stream content will be read and the stream position will be
        restored correctly. Otherwise the data will be read from the
        current position to the end and the original position can
        not be restored.
        """
        if (stream == None):
            raise ArgumentNullException("stream")

        oldPosition:int = None

        try:
        
            # save original stream position.
            if (stream.seekable()):
                oldPosition = stream.tell()
                stream.seek(0)

            self.__InternalLoadFromStream(stream)
        
        finally:
        
            # restore stream position.
            if (stream.seekable() and (oldPosition != None)):
                stream.seek(oldPosition)


    def ResetData(self) -> None:
        """
        Resets the internal data stream.

        This method is intended to reset the internal data stream
        if custom handling of data is needed by derived classes.
        """
        self.__fData.seek(0)
        self.__fData.truncate(0)
