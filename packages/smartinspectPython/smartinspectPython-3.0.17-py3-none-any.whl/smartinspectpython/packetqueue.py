"""
Module: packetqueue.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .packetqueueitem import PacketQueueItem
from .packet import Packet

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class PacketQueue:
    """
    Manages a memory size limited queue of packets.

    This class is responsible for managing a size limited queue
    of packets. This functionality is needed by the protocol
    Protocol.IsValidOption feature. The maximum
    total memory size of the queue can be set with the Backlog
    property. New packets can be added with the Push method. Packets
    which are no longer needed can be retrieved and removed from the
    queue with the Pop method.

    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    _OVERHEAD:int = 24

    
    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        # initialize instance.
        self.__fBacklog:int = 0
        self.__fSize:int = 0
        self.__fCount:int = 0
        self.__fHead:PacketQueueItem = None
        self.__fTail:PacketQueueItem = None


    @property
    def Backlog(self) -> int:
        """ 
        Gets the Backlog property value.

        Represents the total maximum memory size of this queue in bytes.

        Each time a new packet is added with the Push method, it will
        be verified that the total occupied memory size of the queue
        still falls below the supplied Backlog limit. To satisfy this
        constraint, old packets are removed from the queue when necessary.
        """
        return self.__fBacklog
    
    @Backlog.setter
    def Backlog(self, value:int) -> None:
        """ 
        Sets the Backlog property value.
        """
        if value != None:

            self.__fBacklog = value
            self.__Resize()


    @property
    def Count(self) -> int:
        """ 
        Gets the Count property value.

        Returns the current amount of packets in this queue.

        For each added packet this counter is incremented by one
        and for each removed packet (either with the Pop method or
        automatically while resizing the queue) this counter is decremented
        by one. If the queue is empty, this property returns 0.
        """
        return self.__fCount


    def __Resize(self) -> None:
        """
        Removes old packets from the queue (if necessary) when the Backlog
        property value is changed.
        """
        while (self.__fBacklog < self.__fSize):
        
            if (self.Pop() == None):
            
                self.__fSize = 0
                break


    def Clear(self) -> None:
        """
        Removes all packets from this queue.

        Removing all packets of the queue is done by calling the Pop
        method for each packet in the current queue.
        """
        while True:

            if (self.Pop() == None):
                break


    def Pop(self) -> Packet:
        """
        Returns a packet and removes it from the queue.

        Returns:
            The removed packet or null if the queue does not contain any packets.

        If the queue is not empty, this method removes the oldest
        packet from the queue (also known as FIFO) and returns it.
        The total size of the queue is decremented by the size of
        the returned packet (plus some internal management overhead).
        """
        result:Packet = None
        item:PacketQueueItem = self.__fHead

        if (item != None):
        
            result = item.Packet
            self.__fHead = item.Next

            if (self.__fHead != None):
                self.__fHead.Previous = None
            else:
                self.__fTail = None

            self.__fCount = self.__fCount - 1

            size:int = 0
            if (result.Size != None):
                size = result.Size
            self.__fSize = self.__fSize - (size + PacketQueue._OVERHEAD)
        
        return result


    def Push(self, packet:Packet) -> None:
        """
        Adds a new packet to the queue.

        Args:
            packet (Packet):
                The packet to add.

        This method adds the supplied packet to the queue. The size
        of the queue is incremented by the size of the supplied
        packet (plus some internal management overhead). If the total
        occupied memory size of this queue exceeds the Backlog limit
        after adding the new packet, then already added packets will
        be removed from this queue until the Backlog size limit is
        reached again.
        """
        item:PacketQueueItem = PacketQueueItem()
        item.Packet = packet

        if (self.__fTail == None):
        
            self.__fTail = item
            self.__fHead = item
        
        else:
        
            self.__fTail.Next = item
            item.Previous = self.__fTail
            self.__fTail = item
        
        self.__fCount = self.__fCount + 1
        self.__fSize += packet.Size + PacketQueue._OVERHEAD
        self.__Resize()
