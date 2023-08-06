"""
Module: schedulerqueue.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""


# our package imports.
from .schedulerqueueitem import SchedulerQueueItem
from .schedulercommand import SchedulerCommand
from .scheduleraction import SchedulerAction
from .packet import Packet

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SchedulerQueue:
    """
    Manages a queue of scheduler commands.

    This class is responsible for managing a queue of scheduler
    commands. This functionality is needed by the
    Protocol.IsValidOption and the Scheduler class. New commands can 
    be added with the Enqueue method. Commands can be dequeued with 
    Dequeue. This queue does not have a maximum size or count.

    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    OVERHEAD:int = 24

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        # initialize instance.
        self.__fSize:int = 0
        self.__fCount:int = 0
        self.__fHead:SchedulerQueueItem = None
        self.__fTail:SchedulerQueueItem = None


    @property
    def Count(self) -> int:
        """ 
        Returns the current amount of scheduler commands in this queue.

        For each added scheduler command this counter is incremented
        by one and for each removed command (with Dequeue) this
        counter is decremented by one. If the queue is empty, this
        property returns 0.
        """
        return self.__fCount


    @property
    def Size(self) -> int:
        """ 
        Returns the current size of this queue in bytes.

        For each added scheduler command this counter is incremented
        by the size of the command (plus some internal management
        overhead) and for each removed command (with Dequeue) this
        counter is then decremented again. If the queue is empty,
        this property returns 0.
        """
        return self.__fSize


    def __Add(self, item:SchedulerQueueItem) -> None:
        """
        Adds a new scheduler queue item to the queue.

        Args:
            item (SchedulerQueueItem):
                A SchedulerQueueItem to add.
        """
        if (self.__fTail == None):
        
            self.__fTail = item
            self.__fHead = item
        
        else:
        
            self.__fTail.Next = item
            item.Previous = self.__fTail
            self.__fTail = item

        self.__fCount = self.__fCount + 1
        if (item.Command != None):
            self.__fSize = self.__fSize + (item.Command.Size + SchedulerQueue.OVERHEAD);


    def __Remove(self, item:SchedulerQueueItem) -> None:
        """
        Removes a scheduler queue item from the queue.

        Args:
            item (SchedulerQueueItem):
                A SchedulerQueueItem to remove.
        """
        if (item == self.__fHead): # head
        
            self.__fHead = item.Next
            if (self.__fHead != None):
                self.__fHead.Previous = None
            else: # was also tail
                self.__fTail = None
        
        else:
        
            if (item.Previous != None):
            
                item.Previous.Next = item.Next
                if (item.Next == None):  # tail
                    self.__fTail = item.Previous
                else:
                    item.Next.Previous = item.Previous

        self.__fCount = self.__fCount - 1
        if (item.Command != None):
            self.__fSize = self.__fSize - (item.Command.Size + SchedulerQueue.OVERHEAD)


    def Clear(self) -> None:
        """
        Removes all scheduler commands from this queue.

        Removing all scheduler commands of the queue is done by calling
        the Dequeue method for each command in the current queue.
        """
        while True:

            if (self.Dequeue() == None):
                break


    def Dequeue(self) -> SchedulerCommand:
        """
        Returns a scheduler command and removes it from the queue.

        Returns:
            The removed scheduler command or null if the queue does not
            contain any packets.

        If the queue is not empty, this method removes the oldest
        scheduler command from the queue (also known as FIFO) and
        returns it. The total Size of the queue is decremented by
        the size of the returned command (plus some internal
        management overhead).
        """
        item:SchedulerQueueItem = self.__fHead

        if (item != None):
        
            self.__Remove(item)
            return item.Command
        
        else:
            return None


    def Enqueue(self, command:SchedulerCommand) -> None:
        """
        Adds a new scheduler command to the queue.

        Args:
            command (SchedulerCommand):
                The command to add.

        This method adds the supplied scheduler command to the
        queue. The Size of the queue is incremented by the size of
        the supplied command (plus some internal management overhead).
        This queue does not have a maximum size or count.
        """
        item:SchedulerQueueItem = SchedulerQueueItem()
        item.Command = command
        self.__Add(item)


    def Trim(self, size:int) -> bool:
        """
        Tries to skip and remove scheduler commands from this queue.

        Args:
            size (int):
                The minimum amount of bytes to remove from this queue.

        Returns:
            True if enough scheduler commands could be removed and false otherwise.

        This method removes the next WritePacket scheduler commands
        from this queue until the specified minimum amount of bytes
        has been removed. Administrative scheduler commands (connect,
        disconnect or dispatch) are not removed. If the queue is
        currently empty or does not contain enough WritePacket
        commands to achieve the specified minimum amount of bytes,
        this method returns false.
        """
        if (size <= 0):
            return True

        removedBytes:int = 0
        item:SchedulerQueueItem = self.__fHead

        while (item != None):
        
            if ((item.Command != None) and (item.Command.Action == SchedulerAction.WritePacket)):
            
                removedBytes = removedBytes + (item.Command.Size + SchedulerQueue.OVERHEAD)
                self.__Remove(item)

                if (removedBytes >= size):
                    return True

            item = item.Next

        return False
