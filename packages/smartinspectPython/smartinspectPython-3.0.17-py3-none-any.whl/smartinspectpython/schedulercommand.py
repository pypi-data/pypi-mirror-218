"""
Module: schedulercommand.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .scheduleraction import SchedulerAction

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SchedulerCommand():
    """
    Represents a scheduler command as used by the Scheduler class
    and the asynchronous protocol mode.

    This class is used by the Scheduler class to enqueue protocol
    operations for later execution when operating in asynchronous
    mode. For detailed information about the asynchronous protocol 
    mode, please refer to Protocol.IsValidOption.

    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """

        # initialize instance.
        self.__fAction:SchedulerAction = SchedulerAction.Connect
        self.__fState:object = None


    @property
    def Action(self) -> SchedulerAction:
        """
        Gets the Action property value.

        Represents the scheduler action to execute. Please refer
        to the documentation of the SchedulerAction enum for more
        information about possible values.
        """
        return self.__fAction
    
    @Action.setter
    def Action(self, value:SchedulerAction):
        """
        Sets the Action property value.
        """
        if (value != None):
            self.__fAction = value


    @property
    def Size(self) -> int:
        """
        Gets the Size property value.

        Calculates and returns the total memory size occupied by
        this scheduler command.

        This read-only property returns the total occupied memory
        size of this scheduler command. This functionality is used by
        the Protocol.IsValidOption to track the total size of scheduler commands.
        """
        if (self.__fAction != SchedulerAction.WritePacket):
            return 0

        if (self.__fState != None):
            return self.__fState.Size
        
        return 0


    @property
    def State(self) -> object:
        """
        Gets the State property value.

        Represents the optional scheduler command state object which
        provides additional information about the scheduler command.
        This property can be null.
        """
        return self.__fState
    
    @State.setter
    def State(self, value:object):
        """
        Sets the State property value.
        """
        self.__fState = value
