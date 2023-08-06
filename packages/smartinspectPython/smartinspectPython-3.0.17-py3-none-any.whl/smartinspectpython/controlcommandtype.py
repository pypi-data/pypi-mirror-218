"""
Module: controlcommandtype.py

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
class ControlCommandType(EnumComparable):
    """
    Represents the type of a ControlCommand packet. The type of
    a control command influences the way the Console interprets the packet.

    For example, if a Control Command packet has a type of ClearAll, the entire 
    Console is reset when this packet arrives. Also have a look at the corresponding
    Session.ClearAll method.
    """

    ClearLog = 0
    """
    Instructs the Console to clear all Log Entries.
    """

    ClearWatches = 1
    """
    Instructs the Console to clear all Watches.
    """

    ClearAutoViews = 2
    """
    Instructs the Console to clear all AutoViews.
    """

    ClearAll = 3
    """
    Instructs the Console to reset the whole Console.
    """

    ClearProcessFlow = 4
    """
    Instructs the Console to clear all Process Flow entries.
    """
