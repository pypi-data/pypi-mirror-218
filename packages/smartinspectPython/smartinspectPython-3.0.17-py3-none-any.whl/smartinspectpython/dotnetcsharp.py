"""
Module: dotnetcsharp.py

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
from datetime import datetime
from .utils import export


@export
def Ticks(dt:datetime) -> int:
    """
    Returns the number of ticks for a given datetime.
    """
    return int((dt - datetime(1, 1, 1)).total_seconds() * 10000000)


@export
class ArgumentNullException(Exception):
    """
    The exception that is thrown when a null reference is passed to a method that does not accept it as a valid argument.
    """

    def __init__(self, paramName:str) -> None:
        """
        Initializes a new instance of the class with the name of the parameter that causes this exception.
        """
        super().__init__(self)

        # initialize instance.
        self.__paramName = paramName
        self.__message = "The \"{0}\" parameter is required, and cannot be null / None.".format(paramName)


    @property
    def Message(self) -> str:
        """ 
        Gets the error message and the parameter name, or only the error message if no parameter name is set.
        """
        return self.__message
    
    @property
    def paramName(self) -> str:
        """ 
        Gets the name of the parameter that causes this exception.
        """
        return self.__paramName
    
    def __str__(self) -> str:
        """ 
        Gets the error message and the parameter name, or only the error message if no parameter name is set.
        """
        return "ArgumentNullException: " + self.__message
    
@export
class ArgumentOutOfRangeException(Exception):
    """
    The exception that is thrown when the value of an argument is outside the allowable range of values as defined by the invoked method.
    """

    def __init__(self, paramName:str) -> None:
        """
        Initializes a new instance of the class with the name of the parameter that causes this exception.
        """
        super().__init__(self)

        # initialize instance.
        self.__paramName = paramName
        self.__message = "The \"{0}\" parameter is outside the allowable range of values as defined by the invoked method.".format(paramName)


    @property
    def Message(self) -> str:
        """ 
        Gets the error message and the parameter name, or only the error message if no parameter name is set.
        """
        return self.__message
    
    @property
    def paramName(self) -> str:
        """ 
        Gets the name of the parameter that causes this exception.
        """
        return self.__paramName
    
    def __str__(self) -> str:
        """ 
        Gets the error message and the parameter name, or only the error message if no parameter name is set.
        """
        return "ArgumentNullException: " + self.__message
        