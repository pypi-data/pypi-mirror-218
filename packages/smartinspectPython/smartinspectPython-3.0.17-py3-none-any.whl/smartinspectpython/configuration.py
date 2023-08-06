"""
Module: configuration.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

import _threading_local

# our package imports.
from .dotnetcsharp import ArgumentNullException, ArgumentOutOfRangeException
from .color import Color
from .lookuptable import LookupTable
from .level import Level

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class Configuration:
    """ 
    Responsible for handling the SmartInspect configuration and loading
    it from a file.
    
    This class is responsible for loading and reading values from a
    SmartInspect configuration file. For more information, please refer
    to the SmartInspect.LoadConfiguration method.

    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        self.__fItems:LookupTable = LookupTable()
        self.__fIndexedKeys = []
        self.__fLock:object = _threading_local.RLock()


    @property
    def Count(self) -> int:
        """
        Returns the number of key/value pairs of this SmartInspect
        configuration.
        """
        return self.__fItems.Count


    def Contains(self, key:str) -> bool:
        """
        Tests if the configuration contains a value for a given key. 

        Args:
            key (str):
                The key to test for.

        Returns:
            True if a value exists for the given key; otherwise, false.
        """
        return self.__fItems.Contains(key)


    def Clear(self) -> None:
        """
        Removes all key/value pairs of the configuration.
        """
        self.__fIndexedKeys.clear()
        self.__fItems.Clear()


    def LoadFromFile(self, fileName:str) -> None:
        """
        Loads the configuration from a file.

        Args:
            fileName (str):
                The name of the file to load the configuration from.
        
        Raises:
            IOException:
                An I/O error occurred while trying to load the configuration or if the
                specified file does not exist.
            ArgumentNullException:
                The fileName argument is null.

        This method loads key/value pairs separated with a '='
        character from a file. Empty, unrecognized lines or lines
        beginning with a ';' character are ignored.
        """
        if (fileName == None):
            raise ArgumentNullException("fileName")

        # clear all configuration data.
        self.Clear()

        with open(fileName, 'r') as reader:

            # process the file line-by-line, ignoring any lines
            # that start with a semi-colon (comments).
            # The EOF char is an empty string.
            line:str = reader.readline()
            while line != '':

                line = line.strip()
                if (len(line) > 0) and (not line.startswith(";")):
                    self.Parse(line)

                line = reader.readline()


    def Parse(self, pair:str) -> None:
        """
        Parses a line read from a configuration file, adding the
        found key and value to the configuration variables table.

        Args:
            pair (str):
                String that contains a KEY=VALUE pair.
        """
        
        # is this a KEY=VALUE format?  if not, then we are done.
        index:int = pair.find('=')
        if (index == -1):
            return

        # get the key and value portions.
        key:str = pair[0:index].strip()
        value:str = pair[index + 1:].strip()

        # fold key value to lower-case for comparison later.
        key = key.lower()

        # does key already existin the index?  if not, then add it.
        if (not self.__fItems.Contains(key)):
            self.__fIndexedKeys.append((key,value))

        # add / update the item value.
        self.__fItems.Put(key, value)


    def ReadBoolean(self, key:str, defaultValue:bool) -> bool:
        """
        Returns a boolean value of an element for a given key.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (bool):
                The value to return if the given key is unknown.

        Returns:
            Either the value converted to a bool for the given key if an
            element with the given key exists or defaultValue otherwise.

        Raises:
            ArgumentNullException:
                The key argument is null.

        This method returns a bool value of true if the found value
        of the given key matches either "true", "1" or "yes" and false
        otherwise. If the supplied key is unknown, the defaultValue
        argument is returned.
        """
        return self.__fItems.GetBooleanValue(key, defaultValue)


    def ReadColor(self, key:str, defaultValue:Color) -> Color:
        """
        Returns a Color value of an element for a given key.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (Color):
                The value to return if the given key is unknown or if the
                found value has an invalid format.

        Returns:
            Either the value converted to a Color value for the given key
            if an element with the given key exists and the found value
            has a valid format or defaultValue otherwise.

        Raises:
            ArgumentNullException:
                The key argument is null.
        
        The element value must be specified as hexadecimal string.
        To indicate that the element value represents a hexadecimal
        string, the element value must begin with "0x", "&amp;H" or "$".
        A '0' nibble is appended if the hexadecimal string has an odd
        length.
        
        The hexadecimal value must represent a three or four byte
        integer value. The hexadecimal value is handled as follows.

        Bytes |  Format
        ----- |  ----------
        3     |  RRGGBB
        4     |  AARRGGBB
        Other |  Ignored
        
        A stands for the alpha channel and R, G and B represent the
        red, green and blue channels, respectively. If the value is not
        given as hexadecimal value with a length of 6 or 8 characters
        excluding the hexadecimal prefix identifier or if the value
        does not have a valid hexadecimal format, this method returns
        defaultValue.
        """
        return self.__fItems.GetColorValue(key, defaultValue)


    def ReadInteger(self, key:str, defaultValue:bool) -> bool:
        """
        Returns a integer value of an element for a given key.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (bool):
                The value to return if the given key is unknown.

        Returns:
            Either the value converted to an int for the given key if an
            element with the given key exists and the found value is a
            valid int or defaultValue otherwise.

        Raises:
            ArgumentNullException:
                The key argument is null.

        This method returns the defaultValue argument if either the
        supplied key is unknown or the found value is not a valid int.
        Only non-negative int values are recognized as valid. 
        """
        return self.__fItems.GetIntegerValue(key, defaultValue)


    def ReadKey(self, index:int) -> str:
        """
        Returns a key of this SmartInspect configuration for a
        given index.

        Args:
            index (int):
                The index in this SmartInspect configuration.

        Returns:
            A key of this SmartInspect configuration for the given index.

        Raises:
            ArgumentOutOfRangeException:
                The index argument is not a valid index of this SmartInspect configuration.

        To find out the total number of key/value pairs in this
        SmartInspect configuration, use Count. To get the value for
        a given key, use ReadString.
        """
        if (index > len(self.__fIndexedKeys)):
            raise ArgumentOutOfRangeException("index")

        for i in range(len(self.__fIndexedKeys)):
            if (i == index):
                value:str = str(self.__fIndexedKeys[index][0])
                return value
        return None


    def ReadLevel(self, key:str, defaultValue:Level) -> Level:
        """
        Returns a Level value of an element for a given key.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (Level):
                The value to return if the given key is unknown.

        Returns:
            Either the value converted to the corresponding Level value for
            the given key if an element with the given key exists and the
            found value is a valid Level value or defaultValue otherwise.

        Raises:
            ArgumentNullException:
                The key argument is null.

        This method returns the defaultValue argument if either the
        supplied key is unknown or the found value is not a valid Level
        value. Please see the Level enum for more information on the
        available values.  
        """
        return self.__fItems.GetLevelValue(key, defaultValue)


    def ReadString(self, key:str, defaultValue:str) -> str:
        """
        Returns a string value of an element for a given key.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (str):
                The value to return if the given key is unknown.

        Returns:
            Either the value for a given key if an element with the 
            given key exists or defaultValue otherwise.

        Raises:
            ArgumentNullException:
                The key argument is null.
        """
        value:str = self.__fItems.GetStringValue(key, defaultValue)
        if (value == None) or (len(value) == 0):
            value = defaultValue
        return value
