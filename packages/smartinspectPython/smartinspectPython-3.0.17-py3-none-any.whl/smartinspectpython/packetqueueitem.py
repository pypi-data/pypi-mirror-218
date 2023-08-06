"""
Module: packetqueueitem.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .packet import Packet

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class PacketQueueItem:
    """
    PacketQueue item class.
    """
    
    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        self.Packet:Packet = None
        """
        Packet stored by this queue item.
        """
        self.Next:PacketQueueItem = None
        """
        The next packet queue item in the queue.
        """
        self.Previous:PacketQueueItem = None
        """
        The previous packet queue item in the queue.
        """
   