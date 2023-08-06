"""
Module: protocol.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  
| 2023/06/09 | 3.0.8.0     | Added InfoEvent event and RaiseInfoEvent method to convey SI informational events to interested parties.

</details>
"""

import _threading_local
from datetime import datetime, timedelta 

# our package imports.
from .smartinspectexception import SmartInspectException
from .protocolexception import ProtocolException
from .packetqueue import PacketQueue
from .packet import Packet
from .logheader import LogHeader
from .level import Level
from .optionsparser import OptionsParser
from .optionfoundeventargs import OptionFoundEventArgs
from .connectionsbuilder import ConnectionsBuilder
from .filerotate import FileRotate
from .scheduleraction import SchedulerAction
from .schedulercommand import SchedulerCommand
from .protocolcommand import ProtocolCommand
from .erroreventargs import ErrorEventArgs
from .infoeventargs import InfoEventArgs
from .lookuptable import LookupTable
from .scheduler import Scheduler
from .utils import Event

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class Protocol:
    """
    Is the abstract base class for a protocol. 
    A protocol is responsible for transporting packets.

    A protocol is responsible for the transport of packets. This
    base class offers all necessary methods to handle the protocol
    options and it declares several abstract protocol specific
    methods for handling protocol destinations like connecting or
    writing packets.

    The following table lists the available protocols together with
    their identifier in the SmartInspect.Connections and a short description.

    Protocol (Identifier)  | Description
    ---------------------  | ----------------------------------------------------------------
    FileProtocol ("file")  | Used for writing log files in the standard SmartInspect binary log file format which can be loaded into the Console.
    MemoryProtocol ("mem") | Used for writing log data to memory and saving it to a stream on request.
    PipeProtocol ("pipe")  | Used for sending log data over a named pipe directly to a local Console.
    TcpProtocol ("tcp")    | Used for sending packets over a TCP connection directly to the Console.
    TextProtocol ("text")  | Used for writing log files in a customizable text format.  Best suited for end-user notification purposes.

    There are several options which are IsValidOption
    and beyond that each protocol has its
    own set of additional options. For those protocol specific
    options, please refer to the documentation of the corresponding
    protocol class. Protocol options can be set with Initialize and
    derived classes can query option values using the Get methods.

    Threadsafety:
        The public members of this class are thread-safe.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        # initialize instance - options.
        self.__fCaption:str = ''
        self.__fLevel:Level = Level.Debug
        self.__fReconnect:bool = False
        self.__fReconnectInterval:int = 0
        self.__fBacklogEnabled:bool = False
        self.__fBacklogQueue:int = 0;
        self.__fBacklogFlushOn:Level = Level.Debug
        self.__fBacklogKeepOpen:bool = False
        self.__fAsyncEnabled:bool = False
        self.__fAsyncThrottle:bool = False
        self.__fAsyncClearOnDisconnect:bool = False
        self.__fAsyncQueue:int = 0

        # initialize instance - Internal data.
        self.__fHostName:str = ''
        self.__fAppName:str = ''
        self.__fReconnectDateTime:datetime = None
        self.__fKeepOpen:bool = False
        self.__fFailed:bool = False
        self.__fConnected:bool = False
        self.__fInitialized:bool = False
        self.__fLock:object = _threading_local.RLock()
        self.__fOptions:LookupTable = LookupTable()
        self.__fQueue:PacketQueue = PacketQueue()
        self.__fScheduler:Scheduler = None

        # define all events raised by this class.
        self.ErrorEvent:Event = Event()
        """
        Event raised when a protocol raises an exception.
        """
        self.InfoEvent:Event = Event()
        """
        Event raised when a protocol has an informational message to convey.
        """

        # wire up event handlers.
        self.ErrorEvent += self.OnErrorEvent
        self.InfoEvent += self.OnInfoEvent


    @property
    def AppName(self) -> str:
        """ 
        Gets the AppName property value.
        
        The application name of a protocol is usually set to the
        name of the application this protocol is created in. The
        application name can be used to write LogHeader packets
        after a successful protocol connect.
        """
        return self.__fAppName
    
    @AppName.setter
    def AppName(self, value:str):
        """ 
        Sets the AppName property value.
        """
        if value != None:
            self.__fAppName = value


    @property
    def Asynchronous(self) -> bool:
        """
        Gets the Asynchronous property value.

        Indicates if this protocol is operating in asynchronous protocol mode.

        If this property returns true, this protocol is operating
        in asynchronous protocol mode. Otherwise, it returns false.
        Asynchronous protocol mode can be enabled with the
        Initialize method. Also see IsValidOption for information
        on asynchronous logging and how to enable it.
        """
        return self.__fAsyncEnabled


    @property
    def Caption(self) -> str:
        """
        Gets the Caption property value.

        Returns the caption of this protocol.

        The caption is used in the SmartInspect.Dispatch method to
        lookup a requested connection. The caption can be set with
        the Options property. If you use only one connection at once
        or does not use the SmartInspect.Dispatch method, the caption
        option can safely be ignored.

        For more information, please refer to the documentation of
        the Dispatch and SmartInspect.Dispatch methods.
        """
        return self.__fCaption


    @property
    def Failed(self) -> bool:
        """
        Gets the Failed property value.

        Returns if the last executed connection-related operation of
        this protocol has failed. Indicates if the next operation is
        likely to block.
        """
        return self.__fFailed


    @property
    def HostName(self) -> str:
        """ 
        Gets the HostName property value.
        
        The host name of a protocol is usually set to the name of
        the machine this protocol is created in. The host name can
        be used to write LogHeader packets after a successful
        protocol connect.
        """
        return self.__fHostName
    
    @HostName.setter
    def HostName(self, value:str):
        """ 
        Sets the HostName property value.
        """
        if value != None:
            self.__fHostName = value


    @property
    def Name(self) -> str:
        """
        Gets the Name property value.

        Specifies the name of a real protocol implementation.

        Raises:
            NotImplementedError:
                Thrown if the property method is not overridden in an inheriting class.
            
        Real implementations should return a meaningful name which
        represents the protocol. For example, the FileProtocol
        returns "file", the TcpProtocol "tcp" and the TextProtocol
        "text".
        """
        raise NotImplementedError()


    def __AddOption(self, sender:object, e:OptionFoundEventArgs) -> None:
        """
        Handles the OptionsParser OptionFoundEvent.

        Args:
            sender (object):
                The object which fired the event.
            e (OptionFoundEventArgs):
                Arguments that contain detailed information related to the event.
        """
        if (self.__MapOption(e.Key, e.Value)):
            return

        # is the option supported by the protocol?  if not, then it's an error!
        if (not self.IsValidOption(e.Key)):
            raise SmartInspectException(str.format("Option \"{0}\" is not available for protocol \"{1}\"", e.Key, e.Protocol))

        self.__fOptions.Put(e.Key, e.Value)


    def __CreateOptions(self, options:str) -> None:
        """
        Parses options for this protocol, and adds them to a key-based lookup table.

        Args:
            options (str):
                Protocol options string.
        """
        parser:OptionsParser = None

        try:

            # wire up events, and parse the protocol options.
            parser = OptionsParser()
            parser.OptionFoundEvent += self.__AddOption
            parser.Parse(self.Name, options)

        except Exception as ex:

            self.__RemoveOptions()
            raise  # pass exception on thru.

        finally:

            if (parser != None):
                parser.OptionFoundEvent.unhandle_all()


    def __FlushQueue(self) -> None:
        """
        """
        packet:Packet = self.__fQueue.Pop()

        while (packet != None):
            self.__ForwardPacket(packet, False)
            packet = self.__fQueue.Pop()


    def __ForwardPacket(self, packet:Packet, disconnect:bool) -> None:
        """
        """
        if (not self.__fConnected):

            if (not self.__fKeepOpen):
                self.InternalConnect()
                self.__fConnected = True
                self.__fFailed = False # Success
            else:
                self.__Reconnect()

        if (self.__fConnected):

            packet.Lock()

            try:

                self.InternalWritePacket(packet)

            finally:

                packet.Unlock()

            if (disconnect):
                self.__fConnected = False
                self.InternalDisconnect()


    def __GetOptions(self) -> str:
        """
        Returns a string of options used by this protocol.
        """
        builder:ConnectionsBuilder = ConnectionsBuilder()
        self.BuildOptions(builder)
        return builder.Connections


    def _ImplConnect(self) -> None:
        """
        Internal function that will connect to the protocol destination.
        """
        if (not self.__fConnected and self.__fKeepOpen):

            try:

                try:

                    self.InternalConnect()
                    self.__fConnected = True
                    self.__fFailed = False

                except Exception as ex:

                    self.Reset()
                    raise  # pass exception on thru.

            except Exception as ex:

                self.HandleException(str(ex))


    def _ImplDisconnect(self) -> None:
        """
        Internal function that will disconnect from the protocol destination
        and reset itself to a consistent state.
        """
        if (self.__fConnected):

            try:

                self.Reset()

            except Exception as ex:

                self.HandleException(str(ex))

        else:
            self.__fQueue.Clear()


    def _ImplDispatch(self, command:ProtocolCommand) -> None:
        """
        Executes a protocol specific custom action.

        Args:
            command
                The protocol command which provides protocol specific
                information about the custom action. Can be null.
        """
        if (self.__fConnected):

            try:

                self.InternalDispatch(command)

            except Exception as ex:

                self.HandleException(str(ex))


    def _ImplWritePacket(self, packet:Packet) -> None:
        """
        Writes a packet to the protocol specific destination.

        Args:
            packet
                Packet to write.
        """
        if ((not self.__fConnected) and (not self.__fReconnect) and (self.__fKeepOpen)):
            return

        if (packet == None):
            return

        try:

            try:

                skip:bool = False

                if (self.__fBacklogEnabled):

                    if (packet.Level >= self.__fBacklogFlushOn) and (packet.Level != Level.Control):
                        self.__FlushQueue()
                    else:
                        self.__fQueue.Push(packet)
                        skip = True

                if (not skip):
                    self.__ForwardPacket(packet, not self.__fKeepOpen)
            
            except Exception as ex:

                self.Reset()
                raise  # pass exception on thru.

        except Exception as ex:

            self.HandleException(str(ex))


    def __MapOption(self, key:str, value:str) -> bool:
        """
        This method is for backwards compatibility. In older
        SmartInspect versions the backlog options didn't have
        'backlog.' prefix. This has been changed in version
        3.0. This method does the mapping between the old and
        the new backlog options.

        Args:
            key (str):
                The option key string value.
            value (str):
                The option value string.
        """
        if (key == "backlog"):
            self.__fOptions.Put(key, value)
            backlog:int = self.__fOptions.GetSizeValue("backlog", 0)

            if (backlog > 0):
                self.__fOptions.Add("backlog.enabled", "true")
                self.__fOptions.Add("backlog.queue", value)
            else:
                self.__fOptions.Add("backlog.enabled", "false")
                self.__fOptions.Add("backlog.queue", "0")

            return True

        if (key == "flushon"):
            self.__fOptions.Put(key, value)
            self.__fOptions.Add("backlog.flushon", value)
            return True

        if (key == "keepopen"):
            self.__fOptions.Put(key, value)
            self.__fOptions.Add("backlog.keepopen", value)
            return True

        return False


    def __RaiseErrorEvent(self, ex:Exception) -> None:
        """
        Raises the ErrorEvent event with found exception data.

        Args:
            ex
                The exception that caused the event.

        This method is used to inform other objects that an exception was caught for 
        a protocol function.
        """
        try:

            args:ErrorEventArgs = ErrorEventArgs(ex)
            self.ErrorEvent(self, args)

        except Exception as ex:

            # ignore exceptions.
            pass


    def __Reconnect(self) -> None:

        if (self.__fReconnectInterval > 0):

            # get elapsed time between the last disconnect and now.
            elapsed:timedelta = (datetime.utcnow() - self.__fReconnectDateTime)
            
            # convert to milliseconds to compare to reconnect interval (milliseconds value).
            elapsedms:int = round(elapsed.total_seconds() * 1000)

            # if elapsed time (in milliseconds) is less than our reconnect 
            # interval (in milliseconds), then the interval has not been
            # reached and we will not try to reconnect just yet.
            if (elapsedms < self.__fReconnectInterval):
                return   # the interval has not been reached!

        try:

            if (self.InternalReconnect()):
                self.__fConnected = True

        except:

            # Reconnect exceptions are not reported, but we
            # need to record that the last connection attempt
            # has failed (see below).
            pass

        self.__fFailed = not self.__fConnected

        if (self.__fFailed):

            try:

                self.Reset()

            except:

                pass # Ignored


    def __RemoveOptions(self) -> None:
        self.__fOptions.Clear()


    def __ScheduleConnect(self) -> None:
        """
        """
        command:SchedulerCommand = SchedulerCommand()
        command.Action = SchedulerAction.Connect

        if (self.__fScheduler != None):
            self.__fScheduler.Schedule(command)


    def __ScheduleDisconnect(self) -> None:
        """
        """
        command:SchedulerCommand = SchedulerCommand()
        command.Action = SchedulerAction.Disconnect
        if (self.__fScheduler != None):
            self.__fScheduler.Schedule(command)


    def __ScheduleDispatch(self, cmd:ProtocolCommand) -> None:
        """
        """
        command:SchedulerCommand = SchedulerCommand()
        command.Action = SchedulerAction.Dispatch
        command.State = cmd

        if (self.__fScheduler != None):
            self.__fScheduler.Schedule(command)


    def __ScheduleWritePacket(self, packet:Packet) -> None:
        """
        """
        command:SchedulerCommand = SchedulerCommand()
        command.Action = SchedulerAction.WritePacket
        command.State = packet
        if (self.__fScheduler != None):
            self.__fScheduler.Schedule(command)


    def __StartScheduler(self) -> None:
        """
        Starts the scheduler and the internal scheduler thread
        that will process packets (if asynchronous mode is enabled).
        """
        self.__fScheduler = Scheduler(self)
        self.__fScheduler.Threshold = self.__fAsyncQueue
        self.__fScheduler.Throttle = self.__fAsyncThrottle

        try:

            self.__fScheduler.Start()

        except Exception as ex:

            self.__fScheduler = None
            raise  # pass exception on thru.


    def __StopScheduler(self) -> None:
        """
        Stops the scheduler and the internal scheduler thread
        that will process packets (if asynchronous mode is enabled).
        """
        if (self.__fScheduler != None):
            self.__fScheduler.Stop()
            self.__fScheduler = None


    def _WriteLogHeaderPacket(self):
        """
        Writes a Log header packet that identifies us to the SmartInspect Console.
        """
        logHeader:LogHeader = LogHeader()
        logHeader.AppName = self.__fAppName
        logHeader.HostName = self.__fHostName
        self.InternalWritePacket(logHeader)


    def BuildOptions(self, builder:ConnectionsBuilder) -> None:
        """
        Fills a ConnectionsBuilder instance with the options currently
        used by this protocol.

        Args:
            builder:
                The ConnectionsBuilder object to fill with the current options
                of this protocol.
        
        The filled options string consists of key, value option pairs
        separated by commas.
        
        This function takes care of the options (see IsValidOption).
        To include protocol specific options, override this function.
        """
        # Asynchronous options.
        builder.AddOptionBool("async.enabled", self.__fAsyncEnabled)
        builder.AddOptionBool("async.clearondisconnect", self.__fAsyncClearOnDisconnect)
        builder.AddOptionInteger("async.queue", self.__fAsyncQueue / 1024)
        builder.AddOptionBool("async.throttle", self.__fAsyncThrottle)

        # Backlog options.
        builder.AddOptionBool("backlog.enabled", self.__fBacklogEnabled)
        builder.AddOptionLevel("backlog.flushon", self.__fBacklogFlushOn)
        builder.AddOptionBool("backlog.keepopen", self.__fBacklogKeepOpen)
        builder.AddOptionInteger("backlog.queue", self.__fBacklogQueue / 1024)

        # General options.
        builder.AddOptionLevel("level", self.__fLevel)
        builder.AddOptionString("caption", self.__fCaption)
        builder.AddOptionBool("reconnect", self.__fReconnect)
        builder.AddOptionInteger("reconnect.interval", self.__fReconnectInterval)


    def Connect(self) -> None:
        """
        Connects to the protocol specific destination.
        
        Raises:
            ProtocolException:
                Connecting to the destination failed.  Can only occur when operating in
                normal blocking mode. In asynchronous mode, the Error event is used for
                reporting exceptions instead.
        
        In normal blocking mode (see IsValidOption), this method
        does nothing more than to verify that the protocol is not
        already connected and does not use the IsValidOption
        and then calls the abstract protocol specific InternalConnect method in a thread-safe
        and exception-safe context.

        When operating in asynchronous mode instead, this method
        schedules a connect operation for asynchronous execution
        and returns immediately. Please note that possible
        exceptions which occur during the eventually executed
        connect are not thrown directly but reported with the
        Error event.
        """
        with self.__fLock:

            if (self.__fAsyncEnabled):

                # is the scheduler already running?  if so, then nothing to do!
                if (self.__fScheduler != None):
                    return

                try:

                    self.__StartScheduler()
                    self.__ScheduleConnect()

                except Exception as ex:

                    self.HandleException(str(ex))

            else:

                self._ImplConnect()


    def Disconnect(self) -> None:
        """
        Disconnects from the protocol destination.

        Raises:
            ProtocolException:
                Disconnecting from the destination failed. Can only occur when operating
                in normal blocking mode. In asynchronous mode, the Error event is used for
                reporting exceptions instead.

        In normal blocking mode (see IsValidOption), this method
        checks if this protocol has a working connection and then
        calls the protocol specific InternalDisconnect method in a
        thread-safe and exception-safe context.

        When operating in asynchronous mode instead, this method
        schedules a disconnect operation for asynchronous execution
        and then blocks until the internal protocol thread is done.
        Please note that possible exceptions which occur during
        the eventually executed disconnect are not thrown directly
        but reported with the Error event.
        """
        with self.__fLock:

            if (self.__fAsyncEnabled):

                # if scheduler is not running then there is nothing else to do.
                if (self.__fScheduler == None):
                    return

                if (self.__fAsyncClearOnDisconnect):
                    self.__fScheduler.Clear()

                self.__ScheduleDisconnect()
                self.__StopScheduler()

            else:

                self._ImplDisconnect()


    def Dispatch(self, command:ProtocolCommand) -> None:
        """
        Dispatches a custom action to a concrete implementation of
        a protocol.

        Args:
            command:
                The protocol command object which provides protocol specific
                information about the custom action. Can be null.
        Raises:
            ProtocolException:
                An exception occurred in the custom action. Can only occur when operating
                in normal blocking mode. In asynchronous mode, the Error event is
                used for reporting exceptions instead.

        In normal blocking mode (see IsValidOption), this method
        does nothing more than to call the protocol specific
        InternalDispatch method with the supplied command argument
        in a thread-safe and exception-safe way. Please note that
        this method dispatches the custom action only if the protocol
        is currently connected.

        When operating in asynchronous mode instead, this method
        schedules a dispatch operation for asynchronous execution
        and returns immediately. Please note that possible
        exceptions which occur during the eventually executed
        dispatch are not thrown directly but reported with the
        Error event.
        """
        with self.__fLock:

            if (self.__fAsyncEnabled):

                if (self.__fScheduler == None):
                    return  # Not running

                self.__ScheduleDispatch(command)

            else:

                self._ImplDispatch(command)


    def Dispose(self) -> None:
        """
        Disconnects from the protocol destination.

        Raises:
            ProtocolException:
                Disconnecting from the destination failed. Can only occur when operating
                in normal blocking mode. In asynchronous mode, the Error event is used for
                reporting exceptions instead.

        In normal blocking mode (see IsValidOption), this method
        checks if this protocol has a working connection and then
        calls the protocol specific InternalDisconnect method in a
        thread-safe and exception-safe context.

        When operating in asynchronous mode instead, this method
        schedules a disconnect operation for asynchronous execution
        and then blocks until the internal protocol thread is done.
        Please note that possible exceptions which occur during
        the eventually executed disconnect are not thrown directly
        but reported with the Error event.
        """
        try:

            self.Disconnect()

        finally:

            # unwire all event handlers.
            if (self.ErrorEvent != None):
                self.ErrorEvent.unhandle_all()
            if (self.InfoEvent != None):
                self.InfoEvent.unhandle_all()


    def GetBooleanOption(self, key:str, defaultValue:bool) -> bool:
        """
        Gets the boolean value of a key.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (bool):
                The value to return if the key does not exist.
        
        Returns:
            Either the value if the key exists or defaultValue
            otherwise. Note that this method can throw an exception
            of type ArgumentNullException if you pass a null
            reference as key.

        Raises:
            ArgumentNullException:
                The key argument is null.

        A bool value will be treated as true if the value of the
        key matches either "true", "yes" or "1" and as false
        otherwise. Note that this method can throw an exception
        of type ArgumentNullException if you pass a null reference
        as key.
        """
        return self.__fOptions.GetBooleanValue(key, defaultValue)


    def GetBytesOption(self, key:str, size:int, defaultValue:bytearray) -> bytearray:
        """
        Gets the byte array value of a key.

        Args:
            key (str):
                The key whose value to return.
            size (int):
                The desired size in bytes of the returned byte array. If
                the element value does not have the expected size, it is
                shortened or padded automatically.
            defaultValue (bytearray):
                The value to return if the given key is unknown or if the
                found value has an invalid format.
        
        Returns:
            Either the value converted to a byte array for the given key
            if an element with the given key exists and the found value
            has a valid format or defaultValue otherwise.

        Raises:
            ArgumentNullException:
                The key argument is null.

        The returned byte array always has the desired length as
        specified by the size argument. If the element value does
        not have the required size after conversion, it is shortened
        or padded (with zeros) automatically. This method returns
        the defaultValue argument if either the supplied key is
        unknown or the found value does not have a valid format
        (e.g. invalid characters when using hexadecimal strings).

        Note that this method can throw an exception of type
        ArgumentNullException if you pass a null reference as key.
        """
        return self.__fOptions.GetBytesValue(key, size, defaultValue)


    def GetIntegerOption(self, key:str, defaultValue:int) -> int:
        """
        Gets the integer value of a key.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (int):
                The value to return if the key does not exist.
        
        Returns:
            Either the value if the key exists or defaultValue
            otherwise. Note that this method can throw an exception
            of type ArgumentNullException if you pass a null
            reference as key.

        Raises:
            ArgumentNullException:
                The key argument is null.

        Please note that if a value could be found but is not a
        valid integer, the supplied default value will be returned.
        Only non-negative integers will be recognized as valid
        values. Also note that this method can throw an exception
        of type ArgumentNullException if you pass a null reference
        as key.
        """
        return self.__fOptions.GetIntegerValue(key, defaultValue)


    def GetLevelOption(self, key:str, defaultValue:Level) -> Level:
        """
        Gets the Level value of a key.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (Level):
                The value to return if the key does not exist.
        
        Returns:
            Either the value converted to the corresponding Level value
            for the given key if an element with the given key exists
            and the found value is a valid Level value or defaultValue
            otherwise.

        Raises:
            ArgumentNullException:
                The key argument is null.

        This method returns the defaultValue argument if either the
        supplied key is unknown or the found value is not a valid
        Level value. Please see the Level enum for more information
        on the available values. Note that this method can throw an
        exception of type ArgumentNullException if you pass a null
        reference as key.
        """
        return self.__fOptions.GetLevelValue(key, defaultValue)


    def GetRotateOption(self, key:str, defaultValue:FileRotate) -> FileRotate:
        """
        Gets the FileRotate value of a key.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (FileRotate):
                The value to return if the key does not exist.
        
        Returns:
            Either the value converted to a FileRotate value for the
            given key if an element with the given key exists and the
            found value is a valid FileRotate or defaultValue otherwise.
            Note that this method can throw an exception of type
            ArgumentNullException if you pass a null reference as key.

        Raises:
            ArgumentNullException:
                The key argument is null.

        This method returns the defaultValue argument if either the
        supplied key is unknown or the found value is not a valid
        Level value. Please see the Level enum for more information
        on the available values. Note that this method can throw an
        exception of type ArgumentNullException if you pass a null
        reference as key.
        """
        return self.__fOptions.GetRotateValue(key, defaultValue)


    def GetSizeOption(self, key:str, defaultValue:int) -> int:
        """
        Gets an integer value of a key. The integer value is interpreted 
        as a byte size and it is supported to specify byte units.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (int):
                The value to return if the key does not exist.
        
        Returns:
            Either the value converted to an integer for the given key if
            an element with the given key exists and the found value is a
            valid integer or defaultValue otherwise.

        Raises:
            ArgumentNullException:
                The key argument is null.

        This method returns the defaultValue argument if either the
        supplied key is unknown or the found value is not a valid
        integer or ends with an unknown byte unit. Only non-negative
        integer values are recognized as valid.
        
        It is possible to specify a size unit at the end of the value.
        If a known unit is found, this function multiplies the
        resulting value with the corresponding factor. For example, if
        the value of the element is "1KB", the return value of this
        function would be 1024.
        
        The following table lists the available units together with a
        short description and the corresponding factor.

        Unit Name / Factor | Description
        ------------------ | -----------
        KB / 1024          | KiloByte
        MB / 1024^2        | MegaByte
        GB / 1024^3        | GigaByte
        
        If no unit is specified, this function defaults to the KB
        unit. Note that this method can throw an exception of type
        ArgumentNullException if you pass a null reference as key.
        """
        return self.__fOptions.GetSizeValue(key, defaultValue)


    def GetStringOption(self, key:str, defaultValue:str) -> str:
        """
        Gets the string value of a key.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (str):
                The value to return if the key does not exist.
        
        Returns:
            Either the value if the key exists or defaultValue
            otherwise. Note that this method can throw an exception
            of type ArgumentNullException if you pass a null
            reference as key.

        Raises:
            ArgumentNullException:
                The key argument is null.
        """
        value:str = self.__fOptions.GetStringValue(key, defaultValue)
        if (value == None):
            return ""
        return value


    def GetTimespanOption(self, key:str, defaultValue:float) -> float:
        """
        Gets an integer value of a key. The integer value is
        interpreted as a time span and it is supported to specify time
        span units.

        Args:
            key (str):
                The key whose value to return.
            defaultValue (float):
                The value to return if the key does not exist.
        
        Returns:
            Either the value converted to an integer for the given key if
            an element with the given key exists and the found value is a
            valid integer or defaultValue otherwise. The value is returned
            in milliseconds.

        Raises:
            ArgumentNullException:
                The key argument is null.

        This method returns the defaultValue argument if either the
        supplied key is unknown or the found value is not a valid
        integer or ends with an unknown time span unit.
        
        It is possible to specify a time span unit at the end of the
        value. If a known unit is found, this function multiplies the
        resulting value with the corresponding factor. For example, if
        the value of the element is "1s", the return value of this
        function would be 1000.
        
        The following table lists the available units together with a
        short description and the corresponding factor.
        
        Unit Name / Factor | Description
        ------------------ | -----------
        s (Seconds)        | 1000
        m (Minutes)        | 60*s
        h (Hours)          | 60*m
        d (Days)           | 24*h
        
        If no unit is specified, this function defaults to the Seconds
        unit. Please note that the value is always returned in
        milliseconds.
        """
        return self.__fOptions.GetTimespanValue(key, defaultValue)


    def HandleException(self, message:str) -> None:
        """
        Handles a protocol exception.

        Args:
            message (str):
                The exception message.
        
        Raises:
            ProtocolException:
                Always in normal blocking mode; never in asynchronous mode.
        
        This method handles an occurred protocol exception. It
        first sets the Failed flag and creates a ProtocolException
        object with the name and options of this protocol. In
        normal blocking mode (see IsValidOption), it then throws
        this exception. When operating in asynchronous mode,
        it invokes the Error event handlers instead and does not
        throw an exception.
        """
        # indicate that the last operation has failed.
        self.__fFailed = True

        # create exception object.
        ex:ProtocolException = ProtocolException(message, self.Name, self.__GetOptions())

        if (self.__fAsyncEnabled):

            # notify event handlers.
            self.__RaiseErrorEvent(ex)

        else:

            raise ex


    def Initialize(self, options:str) -> None:
        """
        Sets and initializes the options of this protocol.
        
        Args:
            options (str):
                Protocol options, in string delimited format.

        Raises:
            SmartInspectException:
                Invalid options syntax or an unknown option key.
        
        This property expects an options string which consists
        of key, value pairs separated by commas like this:
        "filename=log.sil, append=true". To use a comma in a value,
        you can use quotation marks like in the following example:
        "filename=\\"log.sil\\", append=true".
        
        Please note that a SmartInspectException exception is thrown
        if an incorrect options string is assigned. An incorrect
        options string could use an invalid syntax or contain one or
        more unknown option keys. This method can be called only once.
        Further calls have no effect. Pass null or an empty string to
        use the default options of a particular protocol.
        """
        with (self.__fLock):

            if (not self.__fInitialized):

                if (options != None):
                    self.__CreateOptions(options)

                self.LoadOptions()
                self.__fInitialized = True


    def InternalConnect(self) -> None:
        """
        Connects to the protocol destination
        Abstract method - inheriting classes must override.

        Raises:
            Exception:
                Connecting to the destination failed.
        
        This method initiates a protocol specific connection attempt.
        The behavior of real implementations of this method can often
        be changed by setting protocol options with the Initialize
        method. This method is always called in a thread-safe and
        exception-safe context.
        """
        raise NotImplementedError()


    def InternalDisconnect(self) -> None:
        """
        Disconnects from the protocol destination.
        Abstract method - inheriting classes must override.

        Raises:
            Exception:
                Disconnecting from the destination failed.

        This method is intended for real protocol implementations
        to disconnect from the protocol specific source. This
        could be closing a file or disconnecting a TCP socket, for
        example. This method is always called in a thread-safe and
        exception-safe context.
        """
        raise NotImplementedError()


    def InternalDispatch(self, command:ProtocolCommand) -> None:
        """
        Executes a protocol specific custom action.
        
        Args:
            command (ProtocolCommand):
                The protocol command which provides protocol specific
                information about the custom action. Can be null.

        Raises:
            Exception:
                Executing the custom action failed.

        The default implementation does nothing. Derived protocol
        implementations can override this method to add custom
        actions. Please see the MemoryProtocol.InternalDispatch
        method for an example. This method is always called in a
        thread-safe and exception-safe way.
        """
        pass    # empty by default


    def InternalReconnect(self) -> bool:
        """
        Reconnects to the protocol specific destination.

        Returns:
            True if the reconnect attempt has been successful and false otherwise.
        
        Raises:
            Exception:
                Reconnecting to the destination failed.

        This method initiates a protocol specific reconnect attempt.
        The behavior of real method implementations can often be
        changed by setting protocol options with Initialize. This
        method is always called in a thread-safe and exception-safe
        context.

        The default implementation simply calls the protocol specific
        InternalConnect method. Derived classes can change this
        behavior by overriding this method. 
        """
        self.InternalConnect()
        return True


    def InternalWritePacket(self, packet:Packet) -> None:
        """
        Writes a packet to the protocol destination.

        Args:
            packet (Packet):
                The packet to write.

        Raises:
            Exception:
                Writing the packet to the destination failed.

        This method is intended for real protocol implementations
        to write the supplied packet to the protocol specific
        destination. This method is always called in a thread-safe
        and exception-safe context.
        """
        pass


    def IsValidOption(self, name:str) -> bool:
        """
        Overriddeable. Validates if a option is supported by this protocol.

        True if the option is supported and false otherwise.


        Args:
            name (str):
                The option name to validate.

        Returns:
            True if the option is supported and false otherwise.

        The following table lists all valid options, their default
        values and descriptions common to all protocols. See below
        for explanations.

        Option Name (Default Value)     | Description
        ---------------------------     | ----------------------------------------------------
        level (debug)                   | Specifies the log level of this protocol.
        reconnect (false)               | Specifies if a reconnect should be initiated when a connection gets dropped.
        reconnect.interval (0)          | If reconnecting is enabled, specifies the minimum time in seconds between two successive reconnect attempts. If 0 is specified, a reconnect attempt is initiated for each packet if needed. It is possible to specify time span units like this: "1s". Supported units are "s" (seconds), "m" (minutes), "h" (hours) and "d" (days).
        caption ([name])                | Specifies the caption of this protocol as used by SmartInspect.Dispatch. By default, it is set to the protocol identifier (e.g., "file" or "mem").
        async.enabled (false)           | Specifies if this protocol should operate in asynchronous instead of the default blocking mode.
        async.queue (2048)              | Specifies the maximum size of the asynchronous queue in kilobytes. It is possible to specify size units like this: "1 MB". Supported units are "KB", "MB" and "GB".
        async.throttle (true)           | Specifies if the application should be automatically throttled in asynchronous mode when more data is logged than the queue can handle.
        async.clearondisconnect (false) | Specifies if the current content of the asynchronous queue should be discarded before disconnecting. Useful if an application must not wait for the logging to complete before exiting.
        backlog.enabled (false)         | Enables the backlog feature (see below).
        backlog.queue (2048)            | Specifies the maximum size of the backlog queue in kilobytes. It is possible to specify size units like this: "1 MB". Supported units are "KB", "MB" and "GB".
        backlog.flushon (error)         | Specifies the flush level for the backlog functionality.
        backlog.keepopen (false)        | Specifies if the connection should be kept open between two successive writes when the backlog feature is used.
        
        With the log level of a protocol you can limit the amount of
        data being logged by excluding packets which don't have a
        certain minimum log level. For example, if you set the level
        to "message", all packets with a log level of "debug" or
        "verbose" are ignored. For a complete list of available log
        level values, please see the documentation of the Level enum.

        The caption option specifies the caption for this protocol
        as used by the SmartInspect.Dispatch method. This method
        can send and initiate custom protocol actions and the caption
        is used to lookup the requested connection. By default, the
        caption is set to the identifier of a protocol (e.g., "file"
        or "mem"). For more information about the dispatching of
        custom protocol actions, please refer to the documentation of
        the Dispatch and SmartInspect.Dispatch methods.

        If the backlog option is enabled, all packets whose log level
        is less than the flushon level and equal to or higher than the
        general log level of a protocol, will be written to a queue
        rather than directly to the protocol specific destination. When
        a packet arrives with a log level of at least the same value
        as the flushon option, the current content of the queue is
        written. The total amount of memory occupied by this queue
        can be set with the queue option. If the packet queue has
        been filled up with packets and a new packet is about to be
        stored, old packets are discarded.

        As an example, if the backlog queue is set to "2 MB" and the
        flushon level to "error", all packets with a log level less
        than error are written to a queue first. By specifying a queue
        option of "2 MB", the backlog queue is set to a maximum memory
        size of 2 megabyte. Now, when a packet with a log level of
        error arrives, the current content of the queue and then the
        error itself are written.

        With the keepopen option of the backlog feature you can specify
        if a connection should be kept open between two successive
        writes. When keepopen is set to false, a connection is only
        available during the actual write / flush. A connection is
        thus only created when absolutely necessary.

        A protocol can either operate in normal blocking (the default)
        or in asynchronous mode. In blocking mode, the operations of
        this protocol (Connect, Disconnect, Dispatch and WritePacket)
        are executed synchronously and block the caller until they are
        done. In asynchronous mode, these operations are not executed
        directly but scheduled for execution in a different thread 
        and return immediately. Asynchronous logging can increase the
        logging performance and reduce the blocking of applications.

        When operating in asynchronous mode, this protocol uses a
        queue to buffer the logging data. The total amount of memory
        occupied by this queue can be set with the queue option. The
        throttle option specifies if an application should be
        automatically throttled in asynchronous mode when more data
        is logged / generated than the queue can handle. If this
        option is disabled and the queue is currently full, old
        packets are discarded when new data is logged. The throttle
        option ensures that no logging data is lost but can be
        disabled if logging performance is critical.

        With the clearondisconnect option, you can specify if the
        current content of the asynchronous queue should be discarded
        before disconnecting. This can be useful if an application
        must not wait for the logging to complete before exiting.

        The reconnect option allows a protocol to reconnect
        automatically before a packet is being written. A reconnect
        might be necessary if a working connection has been unexpectedly
        disconnected or could not be established in the first place.
        Possible errors during a reconnect attempt will silently be
        ignored and not reported.

        Please note that the reconnect functionality causes a protocol
        by default to initiate a connection attempt for every packet
        until a connection has been successfully (re-) established.
        This can be a very time consuming process, especially when
        using a protocol which requires a complex connection process
        like TcpProtocol, for example. This can slow down
        the logging performance. When using the reconnect option, it
        is thus recommended to also enable asynchronous logging to not
        block the application or to specify a reconnect interval to
        minimize the reconnect attempts.
        """
        return \
            (name == "caption") or \
            (name == "level") or \
            (name == "reconnect") or \
            (name == "reconnect.interval") or \
            (name == "backlog.enabled") or \
            (name == "backlog.flushon") or \
            (name == "backlog.keepopen") or \
            (name == "backlog.queue") or \
            (name == "async.enabled") or \
            (name == "async.queue") or \
            (name == "async.throttle") or \
            (name == "async.clearondisconnect")


    def LoadOptions(self) -> None:
        """
        Overriddeable. Loads and inspects protocol-specific options.

        This method is intended to give real protocol implementations
        the opportunity to load and inspect options. This method will
        be called automatically when the options have been changed.
        The default implementation of this method takes care of the
        options IsValidOption and  should thus always be called by 
        derived classes which override this method.
        """

        strvalue:str = None

        # General protocol options.
        self.__fLevel = self.GetLevelOption("level", Level.Debug)
        self.__fReconnect = self.GetBooleanOption("reconnect", False)
        self.__fReconnectInterval = self.GetTimespanOption("reconnect.interval", 0)
        strvalue = self.GetStringOption("caption", self.Name)
        if (strvalue != None):
            self.__fCaption = strvalue

        # Backlog protocol options.
        self.__fBacklogEnabled = self.GetBooleanOption("backlog.enabled", False)
        self.__fBacklogQueue = self.GetSizeOption("backlog.queue", 2048)
        self.__fBacklogFlushOn = self.GetLevelOption("backlog.flushon", Level.Error)
        self.__fBacklogKeepOpen = self.GetBooleanOption("backlog.keepopen", False)
        self.__fQueue.Backlog = self.__fBacklogQueue
        self.__fKeepOpen = (not self.__fBacklogEnabled) or (self.__fBacklogKeepOpen)

        # Asynchronous protocol options.
        self.__fAsyncEnabled = self.GetBooleanOption("async.enabled", False)
        self.__fAsyncThrottle = self.GetBooleanOption("async.throttle", True)
        self.__fAsyncQueue = self.GetSizeOption("async.queue", 2048)
        self.__fAsyncClearOnDisconnect = self.GetBooleanOption("async.clearondisconnect", False)


    def OnErrorEvent(self, sender:object, e:ErrorEventArgs) -> None:
        """
        Method that will handle the Protocol.ErrorEvent event.
        Inheriting classes can override this method to handle the event.

        Args:
            sender (object):
                The object which fired the event.
            e (ErrorEventArgs):
                Arguments that contain detailed information related to the event.

        Derived classes can override this method to intercept the
        Protocol.Error event. Note that the Error event is only
        used in combination with asynchronous logging (please see
        IsValidOption for more information). In normal blocking
        mode, exceptions are reported by throwing.
        
        IMPORTANT: Keep in mind that adding SmartInspect log statements to the event 
        handlers can cause a presumably undesired recursive behavior!
        """
        pass


    def OnInfoEvent(self, sender:object, e:InfoEventArgs) -> None:
        """
        Method that will handle the Protocol.InfoEvent event.
        Inheriting classes can override this method to handle the event.

        Args:
            sender (object):
                The object which fired the event.
            e (InfoEventArgs):
                Arguments that contain detailed information related to the event.

        Derived classes can override this method to intercept the
        Protocol.Info event. 
        
        IMPORTANT: Keep in mind that adding SmartInspect log statements to the event 
        handlers can cause a presumably undesired recursive behavior!
        """
        pass


    def RaiseInfoEvent(self, message:str) -> None:
        """
        Raises the InfoEvent event with an informational message.

        Args:
            message (str)
                The message that caused the event.

        This method is used to inform other objects that an informational message was
        issued by a protocol function.
        """
        try:

            args:InfoEventArgs = InfoEventArgs(message)
            self.InfoEvent(self, args)

        except Exception as ex:

            # ignore exceptions.
            pass


    def Reset(self) -> None:
        """
        Resets the protocol and brings it into a consistent state.

        This method resets the current protocol state by clearing
        the internal backlog queue of packets, setting the connected
        status to false and calling the abstract InternalDisconnect
        method of a real protocol implementation to cleanup any
        protocol specific resources.
        """
        self.__fConnected = False
        self.__fQueue.Clear()
        
        try:

            self.InternalDisconnect()

        finally:

            # store current date for comparison later when trying to reconnect.
            self.__fReconnectDateTime = datetime.utcnow()


    def WritePacket(self, packet:Packet) -> None:
        """
        Writes a packet to the protocol specific destination.

        Args:
            packet (Packet):
                The packet to write.

        Raises:
            ProtocolException:
                Writing the packet to the destination failed. Can only occur when operating
                in normal blocking mode. In asynchronous mode, the Error event is
                used for reporting exceptions instead.
        
        This method first checks if the log level of the supplied
        packet is sufficient to be logged. If this is not the
        case, this method returns immediately.

        Otherwise, in normal blocking mode (see IsValidOption),
        this method verifies that this protocol is successfully
        connected and then writes the supplied packet to the
        IsValidOption or passes it directly to the protocol specific 
        destination by calling the InternalWritePacket method. 
        Calling InternalWritePacket is always done in a thread-safe 
        and exception-safe way.

        When operating in asynchronous mode instead, this method
        schedules a write operation for asynchronous execution and
        returns immediately. Please note that possible exceptions
        which occur during the eventually executed write are not
        thrown directly but reported with the Error event.
        """
        with self.__fLock:

            if (packet.Level < self.__fLevel):
                return

            if (self.__fAsyncEnabled):

                if (self.__fScheduler == None):
                    return  # Not running

                self.__ScheduleWritePacket(packet)

            else:

                self._ImplWritePacket(packet)
