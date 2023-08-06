"""
Module: packettype.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""


# our package imports.
from .enumcomparable import EnumComparable

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class PacketType(EnumComparable):
    """
    Represents the type of a packet. In the SmartInspect concept,
    there are multiple packet types each serving a special purpose.
    For a good starting point on packets, please have a look at the
    documentation of the Packet class.
    """

    ControlCommand = 1
    """
    Identifies a packet as Control Command. Please have a look
    at the documentation of the ControlCommand class for more
    information about this packet type.
    """

    LogEntry = 4
    """
    Identifies a packet as Log Entry. Please have a look at the
    documentation of the LogEntry class for information about
    this packet type.
    """

    Watch = 5
    """
    Identifies a packet as Watch. Please have a look at the
    documentation of the Watch class for information about
    this packet type.
    """

    ProcessFlow = 6
    """
    Identifies a packet as Process Flow entry. Please have a
    look at the documentation of the ProcessFlow class for
    information about this packet type.
    """

    LogHeader = 7
    """
    Identifies a packet as Log Header. Please have a look
    at the documentation of the LogHeader class for information
    about this packet type.
    """
