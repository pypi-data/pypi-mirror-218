"""
Module: processflow.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

from datetime import datetime

# our package imports.
from .packet import Packet
from .packettype import PacketType
from .processflowtype import ProcessFlowType as SIProcessFlowType

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class ProcessFlow(Packet):
    """
    Represents the Process Flow packet type which is used in the
    EnterMethod and LeaveMethod methods in the Session class.

    A Process Flow entry is responsible for illustrated process and
    thread information. 
    
    It has several properties which describe its creation context
    (like a thread ID, time-stamp or hostname) and other properties
    which specify the way the Console interprets this packet (like the
    process flow ID). Furthermore a Process Flow entry contains the
    actual data, namely the title, which will be displayed in the
    Console.

    Threadsafety:
        This class is not guaranteed to be thread-safe. However, instances
        of this class will normally only be used in the context of a
        single thread.
    """

    # static variables.
    HEADER_SIZE:int = 28
    
    def __init__(self, processFlowType:SIProcessFlowType) -> None:
        """ 
        Initializes a new ProcessFlow instance with
        a custom process flow type.

        Args:
            processFlowType (ProcessFlowType):
                The type of the new Process Flow entry describes the way the
                Console interprets this packet. Please see the ProcessFlowType
                enum for more information.
        """

        # initialize the base class.
        super().__init__()

        self.__fProcessFlowType:SIProcessFlowType = processFlowType
        self.__fHostName:str = ''
        self.__fTitle:str = ''
        self.__fTimestamp:datetime
        self.__fProcessId:int = Packet.GetProcessId()
        self.__fThreadId:int = Packet.GetThreadId()


    @property
    def HostName(self) -> str:
        """ 
        Gets the HostName property value.

        Represents the hostname of this Process Flow entry.

        The hostname of this Process Flow entry is usually set to the
        name of the machine this Process Flow entry is sent from. It
        will be empty in the SmartInspect Console when this property
        is set to null.
        """
        return self.__fHostName
    
    @HostName.setter
    def HostName(self, value:str) -> None:
        """ 
        Sets the HostName property value.
        """
        if value != None:
            self.__fHostName = value


    @property
    def PacketType(self) -> PacketType:
        """ 
        Overridden.  Returns PacketType.ProcessFlow
        """
        return PacketType.ProcessFlow


    @property
    def ProcessFlowType(self) -> SIProcessFlowType:
        """ 
        Gets the ProcessFlowType property value.

        Represents the type of this Process Flow entry.
        
        The type of the Process Flow entry describes the way the
        Console interprets this packet. Please see the ProcessFlowType
        enum for more information.
        """
        return self.__fProcessFlowType
    
    @ProcessFlowType.setter
    def ProcessFlowType(self, value:SIProcessFlowType) -> None:
        """ 
        Sets the ProcessFlowType property value.
        """ 
        if value != None:
            self.__fProcessFlowType = value


    @property
    def ProcessId(self) -> int:
        """ 
        Gets the ProcessId property value.

        Represents the ID of the process this object was created in.
        """
        return self.__fProcessId
    
    @ProcessId.setter
    def ProcessId(self, value:int) -> None:
        """ 
        Sets the ProcessId property value.
        """ 
        if value != None:
            self.__fProcessId = value


    @property
    def Size(self) -> int:
        """
        Overridden.  Returns the total occupied memory size of this Process Flow packet.

        The total occupied memory size of this Process Flow is the size
        of memory occupied by all strings, the optional Data stream
        and any internal data structures of this Process Flow.
        """
        result = (self.HEADER_SIZE +
                Packet.GetStringSize(self.__fTitle) +
                Packet.GetStringSize(self.__fHostName))
        return result


    @property
    def ThreadId(self) -> int:
        """ 
        Gets the ThreadId property value.

        Represents the ID of the thread this object was created in.
        """
        return self.__fThreadId
    
    @ThreadId.setter
    def ThreadId(self, value:int) -> None:
        """ 
        Sets the ThreadId property value.
        """ 
        if value != None:
            self.__fThreadId = value


    @property
    def Timestamp(self) -> datetime:
        """ 
        Gets the Timestamp property value.

        Represents the time-stamp of this Log Entry object.

        This property returns the creation time of this Log Entry object.
        """
        return self.__fTimestamp
    
    @Timestamp.setter
    def Timestamp(self, value:datetime) -> None:
        """ 
        Sets the Timestamp property value.
        """
        if value != None:
            self.__fTimestamp = value


    @property
    def Title(self) -> str:
        """ 
        Gets the Title property value.

        Represents the title of this Process Flow entry.

        The title of this Process Flow entry will be empty in the
        SmartInspect Console when this property is set to null.
        """
        return self.__fTitle
    
    @Title.setter
    def Title(self, value:str) -> None:
        """ 
        Sets the Title property value.
        """
        if value != None:
            self.__fTitle = value
