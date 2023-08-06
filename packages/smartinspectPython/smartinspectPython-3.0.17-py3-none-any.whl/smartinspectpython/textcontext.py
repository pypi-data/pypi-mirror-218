"""
Module: textcontent.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

from io import StringIO, TextIOWrapper, BytesIO

# our package imports.
from .dotnetcsharp import ArgumentNullException
from .viewercontext import ViewerContext
from .viewerid import ViewerId

# our package constants.
from .const import (
    TEXTFILE_HEADER_BOM
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class TextContext(ViewerContext):
    """ 
    Is the base class for all viewer contexts which deal with text
    data. A viewer context is the library-side representation of a
    viewer in the Console.

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
        self.__fData:StringIO = StringIO()


    @property
    def ViewerData(self) -> BytesIO:
        """ 
        Overridden.  Returns the actual data which will be displayed
        in the viewer specified by the ViewerId.
        """
        # create stream and write UTF8 BOM (byte order mark).
        stream:BytesIO = BytesIO()
        stream.write(TEXTFILE_HEADER_BOM)

        oldPosition:int = 0

        try:

            # save original stream position.
            oldPosition = self.__fData.tell()
            self.__fData.seek(0)

            # write text content with UTF-8 encoding.
            data:str = self.__fData.read()
            stream.write(data.encode('utf-8'))

        except Exception as ex:

            raise

        finally:

            # restore stream position.
            self.__fData.seek(oldPosition)

        # reset stream position for read, and return to caller.
        stream.seek(0)
        return stream


    def AppendLine(self, line:str) -> None:
        """
        Appends a line to the text data.

        Args:
            line (str):
                The line to append.

        Raises:
            ArgumentNullException:
                The line argument is null.

        This method appends the supplied line and a carriage return
        + linefeed character to the internal text data after it has
        been escaped by the EscapeLine method.
        """
        if (line == None):
            raise ArgumentNullException("line")

        self.__fData.write(self.EscapeLine(line))
        self.__fData.write("\r\n")


    def AppendText(self, text:str) -> None:
        """
        Appends text.

        Args:
            Text (str):
                The text to append.

        Raises:
            ArgumentNullException:
                The text argument is null.
        """
        if (text == None):
            raise ArgumentNullException("text")

        self.__fData.write(text)


    def Dispose(self, disposing:bool) -> None:
        """
        Releases any resources.

        Args:
            disposing (bool):
                True if managed resources should be released and false otherwise.
        """
        if (disposing):
            self.ResetData()


    def EscapeLine(self, line:str) -> str:
        """
        Escapes a line.

        Args:
            line (str):
                The line to escape.

        Returns:
            The escaped line.

        If overridden in derived classes, this method escapes a
        line depending on the viewer format used. The default
        implementation does no escaping.
        """
        # the default implementation does no escaping.
        return line


    def LoadFromFile(self, fileName:str) -> None:
        """
        Loads the text from a file.

        Args:
             (str):
                The name of the file to load the text from.

        Raises:
            ArgumentNullException:
                The filename argument is null.
            IOException:
                An I/O error occurred.
        """
        if (fileName == None):
            raise ArgumentNullException("fileName")

        with open(fileName, 'r') as reader:

            self.LoadFromReader(reader)


    def LoadFromReader(self, reader:TextIOWrapper) -> None:
        """
        Loads the text from a reader.

        Args:
            reader (TextIOWrapper):
                The reader to read the text from.
        
        Raises:
            ArgumentNullException:
                The reader argument is null.
            IOException:
                An I/O error occurred.

        If the supplied text reader supports seeking then the entire
        text reader content will be read and the stream position will be
        restored correctly. Otherwise the data will be read from the
        current position to the end and the original position can
        not be restored.
        """
        if (reader == None):
            raise ArgumentNullException("reader")
        
        oldPosition:int = None

        try:
        
            # save original stream position.
            if (reader.seekable()):
                oldPosition = reader.tell()
                reader.seek(0)

            self.ResetData()
            self.AppendText(reader.read())
        
        finally:
        
            # restore stream position.
            if (reader.seekable() and (oldPosition != None)):
                reader.seek(oldPosition)
    

    def LoadFromStream(self, stream:TextIOWrapper) -> None:
        """
        Loads the text from a stream.
        
        Args:
            stream (TextIOWrapper):
                The stream to load the text from.

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

            self.LoadFromReader(stream.StringIO)
        
        finally:
        
            # restore stream position.
            if (stream.seekable() and (oldPosition != None)):
                stream.seek(oldPosition)


    def LoadFromText(self, text:str) -> None:
        """
        Loads the text.

        Args:
            Text (str):
                The text to load.

        Raises:
            ArgumentNullException:
                The text argument is null.
        """
        if (text == None):
            raise ArgumentNullException("text")

        self.ResetData()
        self.AppendText(text)


    def ResetData(self) -> None:
        """
        Resets the internal data.
        
        This method is intended to reset the internal text data if
        custom handling of data is needed by derived classes.
        """
        self.__fData.seek(0)
        self.__fData.truncate(0)