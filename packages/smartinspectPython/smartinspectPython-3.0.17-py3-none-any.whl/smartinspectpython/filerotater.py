"""
Module: filerotater.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

from datetime import datetime, timedelta

# our package imports.
from .filerotate import FileRotate

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class FileRotater:
    """
    Responsible for the log file rotate management as used by the
    FileProtocol class.

    This class implements a flexible log file rotate management
    system. For a detailed description of how to use this class,
    please refer to the documentation of the Initialize(DateTime)
    and Update(DateTime) methods and the Mode property.

    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    _DATETIME_MIN_VALUE:datetime = datetime.min  # DateTime.MinValue;   # C# equivalent = 01/01/0001 12:00:00 AM

    def __init__(self) -> None:
        """ 
        Initializes a new instance of the class.
        """

        # initialize instance.
        self.__fMode:FileRotate = FileRotate.NoRotate
        self.__fTimeValue:int = 0


    @property
    def Mode(self) -> FileRotate:
        """ 
        Gets the FileRotate property value.

        Represents the FileRotate mode of this FileRotater object.
    
        Always call the Initialize method after changing this
        property to reinitialize this FileRotater object. For a
        complete list of available property values, please refer
        to the documentation of the FileRotate enum.
        """
        return self.__fMode
    
    @Mode.setter
    def Mode(self, value:FileRotate) -> None:
        """ 
        Sets the FileRotate property value.
        """ 
        if value != None:
            self.__fMode = value


    @staticmethod
    def __GetDays(date:datetime) -> int:
        """
        Returns the number of days between the specified date and the datetime minimum value.

        Args:
            date (datetime):
                Date to find the number of days from.

        Returns:
            The number of days between the specified date and the datetime minimum value.
        """
        return (date - FileRotater._DATETIME_MIN_VALUE).days


    @staticmethod
    def __GetMonday(date:datetime) -> datetime:
        """
        Returns a datetime value for the following Monday from the specified date value.

        Args:
            date (datetime):
                Date to find the next Monday from.

        Returns:
            A datetime value for the following Monday from the specified date value.
        """
        dayofweek:int = date.weekday

        daystoadd:int = 0
        if (dayofweek == 0):    # 0=monday
            daystoadd = 0
        elif (dayofweek == 1):  # 1=tuesday
            daystoadd = -1
        elif (dayofweek == 2):  # 2=wednesday
            daystoadd = -2
        elif (dayofweek == 3):  # 3=thursday
            daystoadd = -3
        elif (dayofweek == 4):  # 4=friday
            daystoadd = -4
        elif (dayofweek == 5):  # 5=saturday
            daystoadd = -5
        elif (dayofweek == 6):  # 6=sunday
            daystoadd = -6
    
        return date + timedelta(days=daystoadd)


    def Initialize(self, now:datetime) -> None:
        """
        Initializes this FileRotater object with a user-supplied timestamp.

        Args:
            now (datetime):
                The user-specified timestamp to use to initialize this object.

        Always call this method after creating a new FileRotater
        object and before calling the Update method the first time.
        For additional information please refer to the Update method.
        """
        self.__fTimeValue = self.GetTimeValue(now);


    def GetTimeValue(self, now:datetime) -> int:
        """
        Determines the amount of time between the specified date and when the next file
        rotation will take place.

        Args:
            now (datetime):
                The date the File Rotation event is calculated from.

        Returns:
            The amount of time between the specified date and when the next file
            rotation will take place.
        """
        timeValue:int = 0

        if (self.__fMode == FileRotate.Hourly):
            timeValue = FileRotater.__GetDays(now) * 24 + now.hour
        elif (self.__fMode == FileRotate.Daily):
            timeValue = FileRotater.__GetDays(now)
        elif (self.__fMode == FileRotate.Weekly):
            timeValue = FileRotater.__GetDays(FileRotater.__GetMonday(now)) 
        elif (self.__fMode == FileRotate.Monthly):
            timeValue = now.year * 12 + now.month
        else:
            timeValue = 0

        return timeValue


    def Update(self, now:datetime) -> bool:
        """
        Updates the date of this FileRotater object and returns
        whether the rotate state has changed since the last call to
        this method or to Initialize.

        Args:
            now (datetime):
                The timestamp to update this object.

        Returns:
            True if the rotate state has changed since the last call to
            this method or to Initialize and false otherwise.

        This method updates the internal date of this FileRotater
        object and returns whether the rotate state has changed since
        the last call to this method or to Initialize. Before calling
        this method, always call the Initialize method.
        """
        timeValue:int = self.GetTimeValue(now)

        if (timeValue != self.__fTimeValue):
        
            self.__fTimeValue = timeValue
            return True
        
        else:
        
            return False
