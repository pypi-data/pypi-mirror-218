"""
Module: optionfoundeventargs.py

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
class OptionFoundEventArgs:
    """
    This class is used by the OptionsParser class to inform interested parties 
    that a protocol option has been found.

    Threadsafety:
        This class is fully thread-safe.
    """
    def __init__(self, protocol:str, key:str, value:str) -> None:
        """
        Initializes a new instance of the class.

        Args:
          protocol (str):
            The protocol name of the new option.
          key (str):
            The key of the new option.
          value (str):
            The value of the new option.
        """

        # initialize instance.
        self.__fProtocol:str = protocol
        self.__fKey:str = key
        self.__fValue:str = value


    @property
    def Protocol(self) -> str:
        """
        This read-only property returns the protocol name of the option
        which has just been found by a OptionsParser object.
        """
        return self.__fProtocol


    @property
    def Key(self) -> str:
        """
        This read-only property returns the key of the option which
        has just been found by a OptionsParser object.
        """
        return self.__fKey


    @property
    def Value(self) -> str:
        """
        This read-only property returns the value of the option which
        has just been found by a OptionsParser object.
        """
        return self.__fValue


    def __str__(self) -> str:
        """
        Returns a string representation of the object.
        
        Returns:
            A string in the form of "Protocol Name=NN, Key=KK, Value=VV".
        """
        return str.format("Protocol Name=\"{0}\", Key=\"{1}\", Value=\"{2}\"", self.__fProtocol, self.__fKey, self.__fValue)


@export
class OptionFoundEventHandler:
    """
    This is the callback type for the OptionsParser.Parse method.
    """

    def __init__(self, sender:object, e:OptionFoundEventArgs) -> None:
        """
        Initializes a new instance of the class.

        Args:
            sender (object):
                The object which fired the event.
            e (OptionFoundEventArgs):
                Arguments that contain detailed information related to the event.
        """
