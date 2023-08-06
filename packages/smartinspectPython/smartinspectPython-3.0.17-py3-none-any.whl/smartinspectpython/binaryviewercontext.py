"""
Module: binaryviewercontext.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .binarycontext import BinaryContext
from .viewerid import ViewerId

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class BinaryViewerContext(BinaryContext):
    """ 
    Represents the binary viewer in the Console which can display binary
    data in a read-only hex editor.

    The binary viewer in the Console interprets the SmartInspect.LogEntry.Data
    as binary data and displays it in a read-only hex editor.

    You can use the BinaryViewerContext class for creating custom log
    methods around Session.LogCustomContext(string, LogEntryType, ViewerContext)
    for sending custom binary data.
    
    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class with a Binary ViewerId value.
        """

        # initialize base instance.
        super().__init__(ViewerId.Binary)

        # initialize instance.
        # nothing to do.
