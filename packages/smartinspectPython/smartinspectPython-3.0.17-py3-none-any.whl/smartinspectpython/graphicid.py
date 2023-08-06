"""
Module: graphicid.py

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
class GraphicId(EnumComparable):
    """
    Used by the GraphicViewerContext class to specify the desired
    picture type.
    """

    Bitmap = ViewerId.Bitmap.value
    """
    Instructs the GraphicViewerContext class to treat the data as bitmap image.
    """

    Jpeg = ViewerId.Jpeg.value
    """
    Instructs the GraphicViewerContext class to treat the data as JPEG image.
    """

    Icon = ViewerId.Icon.value
    """
    Instructs the GraphicViewerContext class to treat the data as Window icon.
    """

    Metafile = ViewerId.Metafile.value
    """
    Instructs the GraphicViewerContext class to treat the data as Window Metafile image.
    """

    Png = ViewerId.Png.value
    """
    Instructs the GraphicViewerContext class to treat the data as PNG image.
    """

