"""
Module: sourceid.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""


# our package imports.
from .enumcomparable import EnumComparable
from .viewerid import ViewerId

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SourceId(EnumComparable):
    """
    Used in the LogSource methods of the Session class to specify
    the type of source code.
    """

    Html = ViewerId.HtmlSource.value
    """
    Instructs the Session.LogSource methods to use syntax highlighting for HTML.
    """

    JavaScript = ViewerId.JavaScriptSource.value
    """
    Instructs the Session.LogSource methods to use syntax highlighting for JavaScript.
    """

    VbScript = ViewerId.VbScriptSource.value
    """
    Instructs the Session.LogSource methods to use syntax highlighting for VBScript.
    """

    Perl = ViewerId.PerlSource.value
    """
    Instructs the Session.LogSource methods to use syntax highlighting for Perl.
    """

    Sql = ViewerId.SqlSource.value
    """
    Instructs the Session.LogSource methods to use syntax highlighting for SQL.
    """

    Ini = ViewerId.IniSource.value
    """
    Instructs the Session.LogSource methods to use syntax highlighting for INI file.
    """

    Python = ViewerId.PythonSource.value
    """
    Instructs the Session.LogSource methods to use syntax highlighting for Python.
    """

    Xml = ViewerId.XmlSource.value
    """
    Instructs the Session.LogSource methods to use syntax highlighting for XML.
    """
