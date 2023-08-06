"""
Module: dataviewercontext.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

from io import StringIO

# our package imports.
from .textcontext import TextContext
from .viewerid import ViewerId

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class DataViewerContext(TextContext):
    """ 
    Represents the data viewer in the Console which can display simple
    and unformatted text.

    The data viewer in the Console interprets the LogEntry.Data as text
    and displays it in a read-only text field.

    You can use the DataViewerContext class for creating custom log
    methods around Session.LogCustomContext(string, LogEntryType, ViewerContext)
    for sending custom text data.
    
    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class with a Data ViewerId value.
        """

        # initialize base instance.
        super().__init__(ViewerId.Data)

        # initialize instance.
        # nothing to do.
