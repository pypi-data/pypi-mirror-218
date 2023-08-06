"""
Module: protocolfactory.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

# our package imports.
from .smartinspectexception import SmartInspectException
from .dotnetcsharp import ArgumentNullException
from .protocol import Protocol
from .tcpprotocol import TcpProtocol
from .fileprotocol import FileProtocol
from .textprotocol import TextProtocol
from .memoryprotocol import MemoryProtocol
from .utils import static_init

# conditional import of the "pipeprotocol" module.  this module utilizes
# the pywin32 module (for Win32 API calls), which is not defined on other systems!
# we only want to include this module if running on Windows.
import platform
if (platform.system().lower() == "windows"):
    from .pipeprotocol import PipeProtocol

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@static_init    # indicate we have a static init method.
@export
class ProtocolFactory:
    """ 
    Creates Protocol instances and registers custom protocols.

    This class is responsible for creating instances of Protocol
    subclasses and registering custom protocol implementations. To
    add a custom protocol, please have a look at the documentation
    and example of the RegisterProtocol method.

    Threadsafety:
        This class is fully thread-safe.
    """

    # static properties.
    __fProtocolClasses = {}
    __fProtocolClassNames = {}

    _PROTOCOL_NOT_FOUND:str = "The requested protocol is unknown: \"{0}\""


    @classmethod
    def static_init(cls) -> None:
        """ 
        Initializes a new instance of the class.
        """
        # Note - at this point, you cannot call any of the static methods in this class,
        # as we are still in the initilization phase!

        # register all Protocol types that we support out of the box.

        protocolName:str = "tcp"
        cls.__fProtocolClasses[protocolName] = TcpProtocol
        cls.__fProtocolClassNames[protocolName] = TcpProtocol.__name__

        protocolName = "file"
        cls.__fProtocolClasses[protocolName] = FileProtocol
        cls.__fProtocolClassNames[protocolName] = FileProtocol.__name__

        protocolName = "text"
        cls.__fProtocolClasses[protocolName] = TextProtocol
        cls.__fProtocolClassNames[protocolName] = TextProtocol.__name__

        protocolName = "mem"
        cls.__fProtocolClasses[protocolName] = MemoryProtocol
        cls.__fProtocolClassNames[protocolName] = MemoryProtocol.__name__

        osname:str = platform.system()
        if (osname != None) and (osname.lower() == "windows"):
            protocolName = "pipe"
            cls.__fProtocolClasses[protocolName] = PipeProtocol
            cls.__fProtocolClassNames[protocolName] = PipeProtocol.__name__


    @staticmethod
    def _CreateInstance(protocolName:str) -> Protocol:
        """
        Creates a new class instance of the selected protocol name.

        Args:
            protocolName (str):
                The protocol name to search for.

        For example, the protocol name of "tcp" will create a new instance
        of the TcpProtocol class.

        The instance created will also have its "__init__" method called
        when it is created.
        """
        try:

            oInstanceClass = ProtocolFactory.__fProtocolClasses[protocolName]
            oInstanceClassName = ProtocolFactory.__fProtocolClassNames[protocolName]
            oInstanceType = type(oInstanceClassName, (oInstanceClass, object), {})
            oInstance = oInstanceType.__call__()

            return oInstance
         
        except Exception as ex:

            raise SmartInspectException(str(ex))


    @staticmethod
    def GetProtocol(name:str, options:str) -> Protocol:
        """
        Creates an instance of a Protocol subclass. 

        Args:
            name (str):
                The protocol name to search for.
            options (str):
                The options to apply to the new Protocol instance. Can be null.

        Returns:
            A new instance of a Protocol subclass.

        Raises:
            SmartInspectException:
                Unknown protocol or invalid options syntax.
        
        This method tries to create an instance of a Protocol subclass
        using the name parameter. If you, for example, specify "file"
        as name parameter, this method returns an instance of the
        FileProtocol class. If the creation of such an instance has
        been successful, the supplied options will be applied to
        the protocol.

        For a list of available protocols, please refer to the Protocol
        class. Additionally, to add your own custom protocol, please
        have a look at the RegisterProtocol method.

        Please note that if the name argument is null, then the
        return value of this method is null as well.
        """
        if (name == None):
            return None

        # ensure name is proper format for comparison.
        name = name.strip().lower()

        # find the protocol object type based on known registered names.
        protocolClass:object = None
        if (ProtocolFactory.__fProtocolClasses != None):
            if (name in ProtocolFactory.__fProtocolClasses.keys()):
                protocolClass = ProtocolFactory.__fProtocolClasses[name]

        # if we could not find it then it's an error.
        if (protocolClass == None):
            raise SmartInspectException(ProtocolFactory._PROTOCOL_NOT_FOUND.format(name))

        # create a new instance of the protocol and return it.
        protocol:Protocol = ProtocolFactory._CreateInstance(name)

        if (protocol != None):
            protocol.Initialize(options)

        return protocol


    @staticmethod
    def RegisterProtocol(name:str, protocolClass) -> None:
        """
        Registers a custom protocol implementation to the SmartInspect
        library.

        Args:
            name (str):
                The name of the custom protocol to register.
            protocolClass (type):
                The class of your custom protocol. It needs to be a class
                derived from the Protocol class.

        This method enables you to register your own custom protocols.
        This can be used to extend the built-in capabilities of the
        SmartInspect Python library. To add your own protocol, derive
        your custom protocol class from .protocol, choose a name and
        pass this name and the type to this method. After registering
        your protocol, you are able to use it in the
        SmartInspect.Connections" property just like
        any other (standard) protocol.

        If one of the supplied arguments is null or the supplied type
        is not derived from the Protocol class then no custom protocol
        is added.
        """
        if (name == None):
            raise ArgumentNullException("name")
        if (protocolClass == None):
            raise ArgumentNullException("protocolClass")

        # ensure name is properly formatted for comparison later.
        name = name.strip().lower()

        # is specified type a subclass of Protocol?  If so, then add it.
        if (issubclass(protocolClass, Protocol)):
            ProtocolFactory.__fProtocolClasses[name] = protocolClass
            ProtocolFactory.__fProtocolClassNames[name] = protocolClass.__name__
