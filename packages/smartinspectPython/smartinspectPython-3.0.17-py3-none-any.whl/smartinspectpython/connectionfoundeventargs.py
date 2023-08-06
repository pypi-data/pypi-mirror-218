"""
Module: connectionfoundeventargs.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
# none

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class ConnectionFoundEventArgs:
    """
    This class is used by the ConnectionsParser class to inform interested parties 
    that a protocol connection string has been found.

    Threadsafety:
        This class is fully thread-safe.
    """
    def __init__(self, protocol:str, options:str) -> None:
        """
        Initializes a new instance of the class.

        Args:
          protocol (str):
            The protocol name which has been found.
          options (str):
            The options of the new protocol.

        """

        # initialize instance.
        self.__fProtocol:str = protocol
        self.__fOptions:str = options


    @property
    def Options(self) -> str:
        """
        This read-only property returns the key of the option which
        has just been found by a ConnectionsParser object.
        """
        return self.__fOptions


    @property
    def Protocol(self) -> str:
        """
        This read-only property returns the protocol which has just
        been found by a ConnectionsParser object.
        """
        return self.__fProtocol


    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        
        Returns:
            A string in the form of "Protocol Name=NN, Options=OO".
        """
        return str.format("Protocol Name=\"{0}\", Options=\"{1}\"", self.__fProtocol, self.__fOptions)


@export
class ConnectionFoundEventHandler:
    """
    This is the callback type for the ConnectionsParser.Parse method.
    """

    def __init__(self, sender:object, e:ConnectionFoundEventArgs) -> None:
        """
        Initializes a new instance of the class.

        Args:
            sender (object):
                The object which fired the event.
            e (ConnectionFoundEventArgs):
                Arguments that contain detailed information related to the event.
        """
