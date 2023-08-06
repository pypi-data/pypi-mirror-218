"""
Module: webviewercontext.py

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
class WebViewerContext(TextContext):
    """ 
    Represents the web viewer in the Console which can display HTML
    text content as web pages.

    The web viewer in the Console interprets the LogEntry.Data
    as an HTML website.
    
    Threadsafety:
        This class is not guaranteed to be thread-safe.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class with a ViewerId.Web.
        """

        # initialize base instance.
        super().__init__(ViewerId.Web)

        # initialize instance.
        # nothing to do.
