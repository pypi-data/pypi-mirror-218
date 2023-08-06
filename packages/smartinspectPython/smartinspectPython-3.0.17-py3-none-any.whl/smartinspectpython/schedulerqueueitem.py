"""
Module: schedulerqueueitem.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""


# our package imports.
from .schedulercommand import SchedulerCommand

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SchedulerQueueItem:
    """
    SchedulerQueue item class.
    """
    
    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        self.Command:SchedulerCommand = None
        """
        Scheduler command stored by this queue item.
        """
        self.Next:SchedulerQueueItem = None
        """
        The next scheduler queue item in the queue.
        """
        self.Previous:SchedulerQueueItem = None
        """
        The previous scheduler queue item in the queue.
        """
