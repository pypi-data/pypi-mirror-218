"""
Module: textprotocol.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

from io import BytesIO

# our package imports.
from .formatter import Formatter as FormatterSI
from .textformatter import TextFormatter
from .fileprotocol import FileProtocol
from .connectionsbuilder import ConnectionsBuilder

# our package constants.
from .const import (
    TEXTFILE_HEADER_BOM,
    TEXTFILE_INDENT_DEFAULT,
    TEXTFILE_PATTERN_DEFAULT
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class TextProtocol(FileProtocol):
    """
    Used for writing customizable plain text log files.

    This class is used for writing plain text log files. This class is used when 
    the 'text' protocol is specified in the SmartInspect.Connections. 
    
    For a list of available protocol options, please refer to the
    IsValidOption method.

    Threadsafety:
        The public members of this class are thread-safe.
    """
    
    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """

        # initialize instance.
        # note that we have to declare these BEFORE calling the base init, as
        # we are overriding the "Formatter" property and we have to define the
        # the underlying value (e.g. "__fFormatter") first!
        self.__fIndent:bool = TEXTFILE_INDENT_DEFAULT
        self.__fPattern:str = TEXTFILE_PATTERN_DEFAULT
        self.__fFormatter:FormatterSI = None

        # initialize base classinstance.
        super().__init__()


    @property
    def DefaultFileName(self) -> str:
        """
        Returns the default filename for this log file protocol.

        The standard implementation of this method returns the string
        "log.txt" here. Derived classes can change this behavior by
        overriding this method.

        """
        return "log.txt"


    @property
    def Formatter(self) -> FormatterSI:
        """
        Returns the formatter for this log file protocol.

        The standard implementation of this method returns an instance
        of the BinaryFormatter class. Derived classes can change this
        behavior by overriding this method.
        """
        if (self.__fFormatter == None):
            self.__fFormatter = TextFormatter()

        return self.__fFormatter


    @property
    def Name(self) -> str:
        """ 
        Overridden.  Returns "text".
        """
        return "text"


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
        builder.AddOptionBool("indent", self.__fIndent)
        builder.AddOptionString("pattern", self.__fPattern)


    def IsValidOption(self, name:str) -> bool:
        """
        Overridden. Validates if a protocol option is supported.

        Args:
            name (str):
                The option name to validate.

        Returns:
            True if the option is supported and false otherwise.

        The following table lists all valid options, their default
        values and descriptions for the TEXT protocol.

        Valid Options (default value)              | Description
        ------------------------------------------ | -----------------------------------------------------------------
        indent (false)                             | Indicates if the logging output should automatically be indented like in the Console.
        pattern ("[%timestamp%] %level%: %title%") | Specifies the pattern used to create a text representation of a packet.

        Please note that this protocol DOES NOT support log file encryption.

        For further options which affect the behavior of this protocol, please have a look at the documentation of the
        Protocol.IsValidOption method of the parent class.

        <details>
            <summary>View Sample Code</summary>
        ```python
        from smartinspectpython.siauto import *  # SiAuto, Level, Session

        # the following are sample SI Connections options for this protocol.

        # log messages using all default options ("log.sil", no indent).
        SiAuto.Si.Connections = "text()"

        # log messages using all default options ("log.sil", no indent).
        SiAuto.Si.Connections = "text(filename=\\"log.txt\\")"

        # log messages (appending) to file 'mylog.txt'.
        SiAuto.Si.Connections = "text(filename=\\"mylog.txt\\", append=true)"

        # log messages to rotating log file 'mylog.txt', that creates a new log 
        # file every week.  since maxparts is not specified, log files will continue 
        # to accumulate and must be manually deleted.
        SiAuto.Si.Connections = "text(filename=\\"mylog.txt\\", append=true, rotate=weekly"

        # log messages to rotating log file 'mylog.txt', that creates a new log 
        # file every week; keep only 7 log files, automatically deleting outdated files.
        SiAuto.Si.Connections = "text(filename=\\"mylog.txt\\", append=true, rotate=weekly, maxparts=7)"

        # log messages to file "mylog.txt" using a custom pattern.
        SiAuto.Si.Connections = "text(filename=\\"mylog.txt\\", append=true, pattern=\"%level% [%timestamp%]: %title%\")"

        # log messages to rotating default file 'mylog.txt', that do not 
        # exceed 16MB in size.
        SiAuto.Si.Connections = "text(maxsize=\\"16MB\\")"
        ```
        """
        # encryption related options are NOT supported for text logging.
        if ((name == "encrypt") or (name == "key")):
            return False

        return \
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
        self.__fPattern = self.GetStringOption("pattern", TEXTFILE_PATTERN_DEFAULT)
        self.__fIndent = self.GetBooleanOption("indent", TEXTFILE_INDENT_DEFAULT)
        self.Formatter.Pattern = self.__fPattern
        self.Formatter.Indent = self.__fIndent


    def WriteFooter(self, stream:BytesIO) -> None:
        """
        Intended to write the footer of a log file.

        Args:
            stream (BytesIO):
                The stream to which the footer should be written to.

        The implementation of this method does nothing. Derived
        class may change this behavior by overriding this method.
        """
        pass


    def WriteHeader(self, stream:BytesIO, size:int) -> int:
        """
        Overridden.  Intended to write the header of a log file.

        Args:
            stream (BytesIO):
                The stream to which the header should be written to.
            size (int):
                Specifies the current size of the supplied stream.
        
        Returns:
            The new size of the stream after writing the header. If no
            header is written, the supplied size argument is returned.

        The implementation of this method writes the standard UTF8
        BOM (byte order mark) to the supplied stream in order to
        identify the log file as text file in UTF8 encoding. Derived
        classes may change this behavior by overriding this method.
        """
        if (size == 0):
            stream.write(TEXTFILE_HEADER_BOM)
            stream.flush()
            return len(TEXTFILE_HEADER_BOM)
        else:
            return size
