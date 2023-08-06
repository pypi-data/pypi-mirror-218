"""
Module: protocolexception.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .smartinspectexception import SmartInspectException

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class ProtocolException(SmartInspectException):
    """
    Used to report any errors concerning the protocol classes.
    """

    def __init__(self, message:str, protocol:str, options:str, *args, **kwargs) -> None:
        """
        Initializes a new instance of the class.

        Args:
            message (str):
                The exception message.
            protocol (str):
                The protocol name value.
            options (str):
                The protocol options string.
        """

        # initialize base class.
        super().__init__(message, *args, **kwargs)

        # initialize instance.
        self.__fProtocolName:str = protocol
        self.__fProtocolOptions:str = options


    @property
    def ProtocolName(self) -> str:
        """ 
        Gets the ProtocolName property value.
        """
        return self.__fProtocolName
    

    @property
    def ProtocolOptions(self) -> str:
        """ 
        Gets the ProtocolOptions property value.
        """
        return self.__fProtocolOptions
