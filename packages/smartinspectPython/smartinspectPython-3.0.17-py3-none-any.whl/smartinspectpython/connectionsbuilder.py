"""
Module: connectionsbuilder.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .dotnetcsharp import ArgumentNullException
from .level import Level
from .filerotate import FileRotate

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class ConnectionsBuilder:
    """
    Assists in building a SmartInspect connections string.

    The ConnectionsBuilder class assists in creating connections
    strings as used by the SmartInspect.Connections property. For
    general information about connections strings, please refer to
    the SmartInspect.Connections property.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        self.__fHasOptions:bool = False
        self.__fBuilder:str = ""  # StringBuilder


    @property
    def Connections(self) -> bool:
        """
        Get the Connections property value.

        This read-only property returns the connections string which
        has previously been built with the BeginProtocol, AddOption
        and EndProtocol methods.
        """
        return self.__fBuilder


    def AddOptionBool(self, key:str, value:bool) -> None:
        """
        Adds a new boolean option to the current protocol section.

        Args:
            key (str):
                Option key name to add.
            value (bool):
                Option key boolean value to add.
        """
        valuestring = "false"
        if (value):
            valuestring = "true"
        self.AddOptionString(key, valuestring)

    
    def AddOptionFileRotate(self, key:str, value:FileRotate) -> None:
        """
        Adds a new file rotate option to the current protocol section.

        Args:
            key (str):
                Option key name to add.
            value (FileRotate):
                Option key FileRotate value to add.
        """
        valuestring = str(value.name.lower())
        self.AddOptionString(key, valuestring)


    def AddOptionInteger(self, key:str, value:int) -> None:
        """
        Adds a new integer option to the current protocol section.

        Args:
            key (str):
                Option key name to add.
            value (int):
                Option key integer value to add.
        """
        valuestring = str(value)
        self.AddOptionString(key, valuestring)


    def AddOptionLevel(self, key:str, value:Level) -> None:
        """
        Adds a new level option to the current protocol section.

        Args:
            key (str):
                Option key name to add.
            value (Level):
                Option key Level value to add.
        """
        valuestring = str(value.name.lower())
        self.AddOptionString(key, valuestring)


    def AddOptionString(self, key:str, value:str) -> None:
        """
        Adds a new string option to the current protocol section.

        Args:
            key (str):
                Option key name to add.
            value (str):
                Option key string value to add.

        This method adds a new string option to the current protocol
        section. The supplied value argument is properly escaped if
        necessary.
        """
        if (key == None):
            raise ArgumentNullException("key")
        if (value == None):
            raise ArgumentNullException("value")

        if (self.__fHasOptions):
            self.__fBuilder += ", "

        self.__fBuilder += key
        self.__fBuilder += "=\""
        self.__fBuilder += self.Escape(value)
        self.__fBuilder += "=\""
        self.__fHasOptions = True


    def BeginProtocol(self, protocolName:str) -> None:
        """
        Begins a new protocol section.

        Args:
            protocolName (str):
                The protocol name (e.g. file, text, tcp, etc).

        This method begins a new protocol with the supplied name.
        All subsequent protocol options are added to this protocol
        until the new protocol section is closed by calling the
        EndProtocol method.
        """
        if (protocolName == None):
            raise ArgumentNullException("protocolName")

        if (len(self.__fBuilder) != 0):
            self.__fBuilder += ", "

        self.__fBuilder += protocolName
        self.__fBuilder += "("
        self.__fHasOptions = False


    def Clear(self) -> None:
        """
        Clears this ConnectionsBuilder instance by removing all
        protocols and their options.
    
        After this method has been called, the Connections property
        returns an empty string.
        """
        self.__fBuilder = ""


    def EndProtocol(self) -> None:
        """
        Ends the current protocol section.
        This method ends the current protocol. To begin a new protocol
        section, use the BeginProtocol method.
        """
        self.__fBuilder += ")"


    def Escape(self, value:str) -> str:
        """
        Replaces any backslash characters in the value with double-backslash characters.

        Args:
            value (str):
                The value to escape.

        Returns:
            The escaped value.
        """
        return value.replace("\\", "\\\\")
