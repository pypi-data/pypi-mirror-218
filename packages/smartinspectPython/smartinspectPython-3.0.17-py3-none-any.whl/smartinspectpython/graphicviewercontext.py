"""
Module: graphicviewercontext.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .binarycontext import BinaryContext
from .graphicid import GraphicId

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class GraphicViewerContext(BinaryContext):
    """ 
    Represents the graphic viewer in the Console which can display images.

    The graphic viewer in the Console interprets the LogEntry.Data as picture.

    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    def __init__(self, id:GraphicId) -> None:
        """
        Initializes a new instance of the class.

        Args:
            id (GraphicId):
                The graphic ID to use.
        """

        # initialize base instance.
        super().__init__(id)

        # initialize instance.
        # nothing to do.
