"""
Module: sourceviewercontext.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""


# our package imports.
from .textcontext import TextContext
from .sourceid import SourceId

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SourceViewerContext(TextContext):
    """ 
    Represents the source viewer in the Console which can display text
    data as source code with syntax highlighting.

    The source viewer in the Console interprets the LogEntry.Data
    as source code and displays it in a read-only
    text editor with syntax highlighting.
    
    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    def __init__(self, id:SourceId) -> None:
        """
        Initializes a new instance of the class.

        Args:
            id (SourceId):
                The source ID to use.
        """

        # initialize base instance.
        super().__init__(id)

        # initialize instance.
        # nothing to do.
