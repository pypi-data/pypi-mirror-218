"""
Module: patternparser.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""


# our package imports.
from .logentry import LogEntry
from .logentrytype import LogEntryType
from .tokenSI import TokenSI
from .tokenfactory import TokenFactory

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class PatternParser:
    """
    Capable of parsing and expanding a pattern string as used in the
    TextProtocol and TextFormatter classes.

    The PatternParser class is capable of creating a text
    representation of a LogEntry object (see Expand). The string
    representation can be influenced by setting a pattern string.
    Please see the Pattern property for a description.

    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    _SPACES:str = "   "
    
    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        self.__fPosition:int = 0
        self.__fPattern:str = ""
        self.__fTokens = []
        self.__fIndent:bool = False
        self.__fIndentLevel:int = 0
        self.__fBuilder = ""


    @property
    def Indent(self) -> bool:
        """ 
        Gets the Indent property value.

        Indicates if the Expand method should automatically intend
        log packets like in the Views of the SmartInspect Console.

        Log Entry packets of type EnterMethod increase the indentation
        and packets of type LeaveMethod decrease it.
        """
        return self.__fIndent
    

    @Indent.setter
    def Indent(self, value:bool) -> None:
        """ 
        Sets the Indent property value.
        """
        if value != None:
            self.__fIndent = value


    @property
    def Pattern(self) -> str:
        """
        Gets the Pattern property value.

        Represents the pattern string for this PatternParser object.

        The pattern string influences the way a text representation of
        a LogEntry object is created. A pattern string consists of a
        list of so called variable and literal tokens. When a string
        representation of a LogEntry object is created, the variables
        are replaced with the actual values of the LogEntry object.

        Variables have a unique name, are surrounded with '%' characters
        and can have an optional options string enclosed in curly
        braces like this: %name{options}%.

        You can also specify the minimum width of a value like this:
        %name,width%. Width must be a valid positive or negative
        integer. If the width is greater than 0, formatted values will
        be right-aligned. If the width is less than 0, they will be
        left-aligned.

        The following table lists the available variables together with
        the corresponding LogEntry property.

        Variable       | Corresponding Property
        -------------- | ------------------------------------------
        %appname%      | LogEntry.AppName
        %color%        | LogEntry.ColorBG
        %hostname%     | LogEntry.HostName
        %level%        | Packet.Level
        %logentrytype% | LogEntry.LogEntryType
        %process%      | LogEntry.ProcessId
        %session%      | LogEntry.SessionName
        %thread%       | LogEntry.ThreadId
        %timestamp%    | LogEntry.Timestamp
        %title%        | LogEntry.Title
        %viewerid%     | LogEntry.ViewerId

        For the time-stamp token, you can use the options string to
        pass a custom date/time format string. This can look as follows:
        %timestamp{HH:mm:ss.fff}%

        The format string must be a valid Python DateTime format
        string. The default format string used by the time-stamp token
        is "yyyy-MM-dd HH:mm:ss.fff".

        Literals are preserved as specified in the pattern string. When
        a specified variable is unknown, it is handled as literal.

        # Examples:
        `"[%timestamp%] %level,8%: %title%"`

        `"[%timestamp%] %session%: %title% (Level: %level%)"`
        """
        return self.__fPattern

    @Pattern.setter
    def Pattern(self, value:str) -> None:
        """
        Sets the Pattern property value.
        """
        self.__fPosition = 0
        self.__fIndentLevel = 0

        if (value != None):
            self.__fPattern = value.strip()
        else:
            self.__fPattern = ""

        self.__Parse()


    def __Next(self) -> TokenSI:
        """
        Gets the next token in the list.

        Returns:
            A Token object that represents the next token found, or null 
            if no more tokens to process.
        """
        length:int = len(self.__fPattern)

        if (self.__fPosition < length):
        
            isVariable:bool = False
            pos:int = self.__fPosition

            if (self.__fPattern[pos] == '%'):
            
                isVariable = True
                pos = pos + 1

            while (pos < length):
            
                if (self.__fPattern[pos] == '%'):
                
                    if (isVariable):

                        pos=pos + 1
                    
                    break
                
                pos = pos + 1
            
            value:str = self.__fPattern[self.__fPosition: pos]
            self.__fPosition = pos

            return TokenFactory.GetToken(value)
        
        else:
        
            return None
        

    def __Parse(self) -> None:
        """
        Creates a string representation of a variable or literal token.
        """
        self.__fTokens.clear()
        token:TokenSI = self.__Next()
        while (token != None):
        
            self.__fTokens.append(token)
            token = self.__Next()


    def Expand(self, logEntry:LogEntry) -> str:
        """
        Creates a text representation of a LogEntry by applying a
        user-specified Pattern string.

        Args:
            logEntry (LogEntry):
                The LogEntry whose text representation should be computed by
                applying the current Pattern string. All recognized variables
                in the pattern string are replaced with the actual values of
                this LogEntry.

        Returns:
            The text representation for the supplied LogEntry object.
        """
        if (len(self.__fTokens) == 0):
            return ""

        self.__fBuilder = ""
        if (logEntry.LogEntryType == LogEntryType.LeaveMethod):
            if (self.__fIndentLevel > 0):
                self.__fIndentLevel = self.__fIndentLevel - 1

        for tokenptr in range(len(self.__fTokens)):

            token:TokenSI = self.__fTokens[tokenptr]

            if (self.__fIndent and token.Indent):
                for i in range(self.__fIndentLevel):
                    self.__fBuilder += PatternParser._SPACES

            expanded:str = token.Expand(logEntry)
            if (expanded != None):

                if (token.Width < 0):
                    
                    # Left-aligned
                    self.__fBuilder += expanded

                    pad:int = -token.Width - len(expanded)

                    for i in range(pad):
                        self.__fBuilder += ' '
                    
                elif (token.Width > 0):
                    
                    pad:int = token.Width - len(expanded)

                    for i in range(pad):
                        self.__fBuilder += ' '

                    # Right-aligned 
                    self.__fBuilder += expanded
                    
                else:
                    
                    self.__fBuilder += expanded
                    
        if (logEntry.LogEntryType == LogEntryType.EnterMethod):
            self.__fIndentLevel = self.__fIndentLevel + 1

        return self.__fBuilder
