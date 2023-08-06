"""
Module: tokenfactory.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""


# our package imports.
from .tokenSI import TokenSI
from .logentry import LogEntry
from .color import Color
from .utils import static_init

# our package constants.
from .const import (
    DEFAULT_COLOR_OBJECT
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@static_init    # indicate we have a static init method.
@export
class TokenFactory:
    """ 
    Creates instances of Token subclasses.

    This class has only one public method called GetToken, which
    is capable of creating Token objects depending on the given
    argument.
    
    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    # static properties.
    __fTokenClassNames = {}
    __fTokenClasses = {}

    @classmethod
    def static_init(cls) -> None:
        """ 
        Initializes a new instance of the class.
        """
        # Note - at this point, you cannot call any of the static methods in this class,
        # as we are still in the initilization phase!
  
        tokenName:str = ""

        # register all token types.
        tokenName = "%appname%"
        cls.__fTokenClasses[tokenName] = cls.__AppNameToken
        cls.__fTokenClassNames[tokenName] = cls.__AppNameToken.__name__

        tokenName = "%session%"
        cls.__fTokenClasses[tokenName] = cls.__SessionToken
        cls.__fTokenClassNames[tokenName] = cls.__SessionToken.__name__

        tokenName = "%hostname%"
        cls.__fTokenClasses[tokenName] = cls.__HostNameToken
        cls.__fTokenClassNames[tokenName] = cls.__HostNameToken.__name__

        tokenName = "%title%"
        cls.__fTokenClasses[tokenName] = cls.__TitleToken
        cls.__fTokenClassNames[tokenName] = cls.__TitleToken.__name__

        tokenName = "%timestamp%"
        cls.__fTokenClasses[tokenName] = cls.__TimestampToken
        cls.__fTokenClassNames[tokenName] = cls.__TimestampToken.__name__

        tokenName = "%level%"
        cls.__fTokenClasses[tokenName] = cls.__LevelToken
        cls.__fTokenClassNames[tokenName] = cls.__LevelToken.__name__

        tokenName = "%color%"
        cls.__fTokenClasses[tokenName] = cls.__ColorToken
        cls.__fTokenClassNames[tokenName] = cls.__ColorToken.__name__

        tokenName = "%logentrytype%"
        cls.__fTokenClasses[tokenName] = cls.__LogEntryTypeToken
        cls.__fTokenClassNames[tokenName] = cls.__LogEntryTypeToken.__name__

        tokenName = "%viewerid%"
        cls.__fTokenClasses[tokenName] = cls.__ViewerIdToken
        cls.__fTokenClassNames[tokenName] = cls.__ViewerIdToken.__name__

        tokenName = "%thread%"
        cls.__fTokenClasses[tokenName] = cls.__ThreadIdToken
        cls.__fTokenClassNames[tokenName] = cls.__ThreadIdToken.__name__

        tokenName = "%__ProcessIdToken%"
        cls.__fTokenClasses[tokenName] = cls.__ProcessIdToken
        cls.__fTokenClassNames[tokenName] = cls.__ProcessIdToken.__name__


    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        pass


    class __AppNameToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            return logEntry.AppName

    class __SessionToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            return logEntry.SessionName

    class __HostNameToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            return logEntry.HostName

    class __TitleToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            return logEntry.Title
        @property
        def Indent(self) -> bool:
            return True

    class __LevelToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            return str(logEntry.Level)

    class __LogEntryTypeToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            return str(logEntry.LogEntryType)

    class __ViewerIdToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            return str(logEntry.ViewerId)

    class __ThreadIdToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            return str(logEntry.ThreadId)

    class __ProcessIdToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            return str(logEntry.ProcessId)

    class __LiteralToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            return self.Value

    class __TimestampToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            if ((self.Options != None) and (len(self.Options) > 0)):
                try:
                    # try to use a custom format string.
                    return logEntry.Timestamp.ToString(self.Options)
                except Exception as ex:
                    pass    # ignore exceptions.
            #return str.format("yyyy-MM-dd HH:mm:ss.fff", logEntry.Timestamp)
            return logEntry.Timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')   # [:-3] <- drop last 3 of milliseconds if desired.

    class __ColorToken(TokenSI):
        def Expand(self, logEntry:LogEntry) -> str:
            if (logEntry.ColorBG != DEFAULT_COLOR_OBJECT):
                return Color.ValueHex
            else:
                return "<default>"
    

    @staticmethod
    def __CreateInstance(tokenName:str, tokenType:type) -> TokenSI:
        """
        Creates a new class instance of the selected token type.

        Args:
            tokenName (str):
                The token name.
            tokenType (type):
                The token type to search for.

        Returns:
            The token instance created.
        """
        try:

            oInstanceClass = TokenFactory.__fTokenClasses[tokenName]
            oInstanceClassName = TokenFactory.__fTokenClassNames[tokenName]
            oInstanceType = type(oInstanceClassName, (oInstanceClass, object), {})
            oInstance = oInstanceType.__call__()

            return oInstance
         
        finally:

            # exceptions will be handled by calling method.
            pass


    @staticmethod
    def CreateLiteral(value:str) -> TokenSI:
        """
        Creates a LiteralToken instance.

        Args:
            value (str):
                The value to assign to the literal token.

        Returns:
            A LiteralToken object with the value assigned.
        """
        token:TokenSI = TokenFactory.__LiteralToken()
        token.Options = ""
        token.Value = value
        return token


    @staticmethod
    def GetToken(value:str) -> TokenSI:
        """
        Creates instance of Token subclasses.

        Args:
            value (str):
                The original string representation of the token.

        Returns:
            An appropriate Token object for the given string representation of a token.

        This method analyzes and parses the supplied representation of
        a token and creates an appropriate Token object. For example,
        if the value argument is set to "%session%", a Token object
        is created and returned which is responsible for expanding the
        %session% variable. For a list of available tokens and a
        detailed description, please have a look at the PatternParser
        class, especially the PatternParser.Pattern property.
        """
        if (value == None):
            return TokenFactory.CreateLiteral("")

        length:int = len(value)
        if (length <= 2):
            return TokenFactory.CreateLiteral(value)

        # if not a valid token id, then we are done.
        # token id's start and end with a percent sign.
        if ((value[0] != '%') or (value[length - 1] != '%')):
            return TokenFactory.CreateLiteral(value)

        original:str = value
        options:str = ""

        # Extract the token options: %token{options}%
        # examples:
        #   %timestamp{HH:mm:ss.fff}%
        index:int = 0
        if (value[length - 2] == '}'):
        
            index = value.find('{')

            if (index > -1):
            
                index = index + 1
                options = value[index:length - 2]
                value = value.replace("{" + options + "}","")
                length = len(value)
            
        width:str = ""
        index = value.find(",") # .index(",")

        # Extract the token width: %token,width%
        # examples:
        #   %level,8%
        if (index != -1):
        
            index = index + 1
            width = value[index:length - 1]
            value = value.replace("," + width,"")
            length = len(value)

        value = value.lower()
        tokentype:type = TokenFactory.__fTokenClasses[value]

        if (tokentype == None):
            return TokenFactory.CreateLiteral(original);

        token:TokenSI = None
        try:
        
            # create the token and assign the properties.
            token = TokenFactory.__CreateInstance(value, tokentype)
            if (token != None):
            
                token.Options = options;
                token.Value = original;
                token.Width = TokenFactory.ParseWidth(width);
        
        except Exception as ex:
        
            return TokenFactory.CreateLiteral(original)

        return token


    @staticmethod
    def ParseWidth(value:str) -> int:
        """
        Parses the specified value for it's width.

        Args:
            value (str):
                The value to obtain the width of.

        Returns:
            The width of the value.
        """
        if (value == None):
            return 0

        value = value.strip()
        if (len(value) == 0):
            return 0

        width:int = 0

        try:
            width = int(value)
        except Exception as ex:
            width = 0

        return width
