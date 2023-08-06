"""
Module: processflowtype.py

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
class ProcessFlowType(EnumComparable):
    """
    Represents the type of a ProcessFlow packet. The type of aProcess Flow 
    entry specifies the way the Console interprets this packet.

    For example, if a Process Flow entry has a type of
    ProcessFlowType.EnterThread, the Console interprets this packet as
    information about a new thread of your application.
    """

    EnterMethod = 0
    """
    Instructs the Console to enter a new method.
    """

    LeaveMethod = 1
    """
    Instructs the Console to leave a method.
    """

    EnterThread = 2
    """
    Instructs the Console to enter a new thread.
    """

    LeaveThread = 3
    """
    Instructs the Console to leave a thread.
    """

    EnterProcess = 4
    """
    Instructs the Console to enter a new process.
    """
        
    LeaveProcess = 5
    """
    Instructs the Console to leave a process.
    """
