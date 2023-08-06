"""
Module: siauto.py

Provides automatically created objects for using the SmartInspect and Session classes.
Please refer to the SiAuto class for more information and examples.

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description      |
| ---------- | ----------- | -----------------|
| 2023/05/30 | 3.0.0.0     | Initial Version. | 

</details>
"""

# all classes to import when "import *" is specified.
__all__ = [
    'SiAuto',
    'Session',
    'Level',
    'ConfigurationTimer',
]

import os

# our package imports.
from .smartinspect import SmartInspect
from .session import Session
from .level import Level
from .configurationtimer import ConfigurationTimer
from .utils import static_init

@static_init    # indicate we have a static init method.
class SiAuto:
    """
    Provides automatically created objects for using the SmartInspect and Session classes.

    This class provides a static property called Si of type SmartInspect.
    Furthermore a Session instance named Main with Si as parent is ready to use. The siauto module 
    is especially useful if you do not want to create SmartInspect and Session instances by yourself.

    The SmartInspect.Connections property of Si is set to "tcp(host=localhost)", the
    SmartInspect.AppName property to "Auto" and the Session.Name property to "Main".

    Threadsafety:
        The public static members of this class are thread-safe.

    **Example:**
    ```python
    # Use the following for 1-time initialization code:

    from .smartinspectpython.siauto import *
    SiAuto.Si.Connections = 'tcp(host=yourdns.com)'
    SiAuto.Si.Enabled = True            # connect
    SiAuto.Main.Level = Level.Debug     # set logging level to Debug (ALL msgs)
    #SiAuto.Main.Level = Level.Verbose   # set logging level to Verbose
    #SiAuto.Main.Level = Level.Message   # set logging level to Message
    #SiAuto.Main.Level = Level.Warning   # set logging level to Warning
    #SiAuto.Main.Level = Level.Error     # set logging level to Error

    #Use the following in main (or classes) in your project:

    # get logger reference.
    logsi:Session = SiAuto.Main
    
    # log some messages and data.
    logsi.LogSystem(Level.Debug)
    logsi.LogDebug("This is a Debug message.")
    logsi.LogMessage("This is a Message.")
    logsi.LogWarning("You have been warned!")
    logsi.LogError("Danger Will Robinson!")
    ```
    """

    """
    ## Static Properties
    """

    # static properties.
    Si:SmartInspect = None   
    """ 
    SmartInspect logging instance (automatically created). 
    """

    Main:Session = None
    """ 
    SmartInspect logging Session instance ('Main', automatically created). 

    The Session.Name is set to "Main" and the Session.Parent to SiAuto.Si.

    **Example:**
    ```python
    Use the following in main (or classes) in your project:

    # get logger reference.
    logsi:Session = SiAuto.Main
    
    # log some messages and data.
    logsi.LogSystem(Level.Debug)
    logsi.LogDebug("This is a Debug message.")
    logsi.LogMessage("This is a Message.")
    logsi.LogWarning("You have been warned!")
    logsi.LogError("Danger Will Robinson!")
    ```
    """

    """
    ## Methods
    """

    @classmethod
    def static_init(cls) -> None:
        """ 
        Initializes a new static instance of the class.
        """
        # Note - at this point, you cannot call any of the static methods in this class,
        # as we are still in the initilization phase!

        # create a new smartinspect instance, using the
        # entry point name as the appname.
        cls.Si = SmartInspect(os.path.basename(os.sys.argv[0]))

        # set default connections string, logging levels, and disable by default.
        cls.Si.Connections = 'tcp(host=localhost)'
        cls.Si.Enabled = False
        cls.Si.Level = Level.Debug
        cls.Si.DefaultLevel = Level.Debug

        # create new default session, named "Main".
        cls.Main = cls.Si.AddSession('Main', True)
        cls.Main.Level = Level.Debug
