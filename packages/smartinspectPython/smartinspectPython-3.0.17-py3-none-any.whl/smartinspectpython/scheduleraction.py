"""
Module: scheduleraction.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .enumcomparable import *

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SchedulerAction(Enum):
    """
    Represents a scheduler action to execute when a protocol is
    operating in asynchronous mode. For general information about
    the asynchronous mode, please refer to Protocol.IsValidOption.
    """

    Connect = 0
    """
    Represents a connect protocol operation. This action is
    enqueued when the Protocol.Connect method is called and
    the protocol is operating in asynchronous mode.
    """

    WritePacket = 1
    """
    Represents a write protocol operation. This action is
    enqueued when the Protocol.WritePacket method is called
    and the protocol is operating in asynchronous mode.
    """

    Disconnect = 2
    """
    Represents a disconnect protocol operation. This action
    is enqueued when the Protocol.Disconnect method is called
    and the protocol is operating in asynchronous mode.
    """

    Dispatch = 3
    """
    Represents a dispatch protocol operation. This action is
    enqueued when the Protocol.Dispatch method is called and
    the protocol is operating in asynchronous mode.
    """
