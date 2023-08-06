"""
Module: scheduler.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

import _threading_local
import threading

# our package imports.
from .schedulerqueue import SchedulerQueue
from .schedulercommand import SchedulerCommand
from .scheduleraction import SchedulerAction
from .packet import Packet
from .protocolcommand import ProtocolCommand

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class Scheduler:
    """
    Responsible for scheduling protocol operations and executing
    them asynchronously in a different thread of control.

    This class is used by the Protocol.IsValidOption to asynchronously execute
    protocol operations. New commands can be scheduled for execution with
    the Schedule method. The scheduler can be started and stopped
    with the Start and Stop methods. The scheduler uses a size
    limited queue to buffer scheduler commands. The maximum size of
    this queue can be set with the Threshold property. To influence
    the behavior of the scheduler if new commands are enqueued and
    the queue is currently considered full, you can specify the
    Throttle mode.

    Threadsafety:
        This class is guaranteed to be thread-safe.
    """

    _BUFFER_SIZE:int = 0x10

    def __init__(self, protocol) -> None:
        """
        Initializes a new instance of the class.

        Args:
            protocol (Protocol):
                The protocol object on which to execute the actual operations like
                connect, disconnect, write or dispatch.
        """
        # initialize instance.
        self.__fMonitor = _threading_local.RLock()
        self.__fMonitorCondition:threading.Condition = threading.Condition(self.__fMonitor)
        self.__fThread:threading.Thread = None
        self.__fQueue:SchedulerQueue = SchedulerQueue()
        self.__fBuffer = [None] * Scheduler._BUFFER_SIZE
        self.__fProtocol = protocol
        self.__fThreshold:int = 0
        self.__fThrottle:bool = False
        self.__fStopped:bool = False
        self.__fStarted:bool = False


    @property
    def Threshold(self) -> int:
        """ 
        Gets the Threshold property value.

        Represents the maximum size of the scheduler command queue.

        To influence the behavior of the scheduler if new commands
        are enqueued and the queue is currently considered full,
        you can specify the Throttle mode.
        """
        return self.__fThreshold

    @Threshold.setter
    def Threshold(self, value:int):
        """ 
        Sets the Threshold property value.
        """
        if (value != None):
            self.__fThreshold = value


    @property
    def Throttle(self) -> bool:
        """ 
        Gets the Throttle property value.

        Specifies if the scheduler should automatically throttle
        threads that enqueue new scheduler commands.

        If this property is true and the queue is considered full
        when enqueuing new commands, the enqueuing thread is
        automatically throttled until there is room in the queue
        for the new command. In non-throttle mode, the thread is
        not blocked but older commands are removed from the queue.
        """
        return self.__fThrottle

    @Throttle.setter
    def Throttle(self, value:bool):
        """ 
        Sets the Throttle property value.
        """
        if (value != None):
            self.__fThrottle = value


    def __Enqueue(self, command:SchedulerCommand) -> bool:
        """
        Queues a new command for asynchronous execution.

        Args:
            command (SchedulerCommand):
                The command to queue.</param>

        Returns:
            True if the command could be queued for asynchronous
            execution and false otherwise.

        This method adds the passed command to the internal queue
        of scheduler commands. The command is eventually executed
        by the internal scheduler thread. This method can block the
        caller if the scheduler operates in Throttle mode and the
        internal queue is currently considered full (see Threshold).
        """
        # has the scheduler threadtask been started yet?  
        # if not, then we are done.
        if (not self.__fStarted):
            return False

        # if scheduler threadtask has stopped then we are done.
        if (self.__fStopped):
            return False

        # any room in the queue for this command?  if not, then we are done.
        commandSize:int = command.Size
        if (commandSize > self.__fThreshold):
            return False

        # lock the queue so only the main thread can access it.
        with (self.__fMonitor):
        
            # is throttling disabled?  or did a protocol function fail?
            if ((not self.__fThrottle) or (self.__fProtocol.Failed)):
            
                # if so, then remove old commands from the queue until we have
                # enough room for the command we are about to add to the queue.
                if ((self.__fQueue.Size + commandSize) > self.__fThreshold):
                    self.__fQueue.Trim(commandSize)
            
            else:
            
                # if throttling is enabled, then wait for the scheduler threadtask
                # to process enough items in the queue until room is made for the
                # command we are about to add to the queue.
                while ((self.__fQueue.Size + commandSize) > self.__fThreshold):

                    self.__fMonitorCondition.wait()

            # add the command to the queue.
            self.__fQueue.Enqueue(command)

            # signal the scheduler threadtask that we added an item to the queue.
            self.__fMonitorCondition.notify_all()

        return True


    def Clear(self) -> None:
        """
        Removes all scheduler commands from this scheduler.

        This method clears the current queue of scheduler commands.
        If the Stop method is called after calling Clear and no new
        commands are stored between these two calls, the internal
        scheduler thread will exit as soon as possible (after the
        current command, if any, has been processed).
        """
        with (self.__fMonitor):
        
            # clear the queue, and let the scheduler threadtask know about it.
            self.__fQueue.Clear()
            self.__fMonitorCondition.notify_all()


    def Schedule(self, command:SchedulerCommand) -> bool:
        """
        Schedules a new command for asynchronous execution.

        Args:
            command (SchedulerCommand):
                The command to schedule.</param>

        Returns:
            True if the command could be scheduled for asynchronous
            execution and false otherwise.

        This method adds the passed command to the internal queue
        of scheduler commands. The command is eventually executed
        by the internal scheduler thread. This method can block the
        caller if the scheduler operates in Throttle mode and the
        internal queue is currently considered full (see Threshold).
        """
        return self.__Enqueue(command)


    def Start(self) -> None:
        """
        Starts this scheduler and the internal scheduler threadtask.

        This method must be called before scheduling new commands
        with the Schedule method. Call Stop to stop the internal
        thread when the scheduler is no longer needed. Note that
        this method starts the internal scheduler thread only once.
        This means that subsequent calls to this method have no
        effect.
        """
        with (self.__fMonitor):
        
            # if scheduler already started then we are done.
            if (self.__fStarted):
                return

            # start the scheduler threadtask on a new thread.
            self.__fThread = threading.Thread(target=self.__SchedulerThreadTask, args=(self,))
            self.__fThread.name = "SiSchedulerThreadTask"
            self.__fThread.start()
            self.__fStarted = True


    def Stop(self) -> None:
        """
        Stops this scheduler and the internal scheduler threadtask.

        This is the matching method for Start. After calling this
        method, new commands will no longer be accepted by Schedule
        and are ignored. This method blocks until the internal
        thread has processed the current content of the queue.
        Call Clear before calling Stop to exit the internal thread
        as soon as possible.
        """
        with (self.__fMonitor):

            # if scheduler has not started yet then we are done.
            if (not self.__fStarted):
                return

            # indicate scheduler has stopped, and pulse the scheduler threadtask
            # to let it know that it can stop.
            self.__fStopped = True
            self.__fMonitorCondition.notify_all()

        # wait for the scheduler threadtask to finish up.
        if (self.__fThread != None):
            self.__fThread.join()


    ##################################################################################################################################
    # The following methods are ran on the Scheduler threadtask!
    ##################################################################################################################################

    def __SchedulerThreadTask(self, instance) -> None:
        """
        Scheduler thread task method.
        """
        while (True):
        
            count:int = self.__Dequeue()

            # is scheduler stopped and no more commands to process?
            if (count == 0):
                break

            if (not self.__RunCommands(count)):
                break   # stopped 

        # reset buffer.
        self.__fBuffer = [None] * Scheduler._BUFFER_SIZE


    def __Dequeue(self) -> int:
        """
        Removes a scheduler command from the queue, and places it into
        an command buffer for subsequent execution by the scheduler thread.

        Returns:
            The number of commands that were removed from the queue.

        This method adds the passed command to the internal queue
        of scheduler commands. The command is eventually executed
        by the internal scheduler thread. This method can block the
        caller if the scheduler operates in Throttle mode and the
        internal queue is currently considered full (see Threshold).

        This method is executed by the __SchedulerThreadTask.
        """
        count:int = 0
        length:int = len(self.__fBuffer)

        # lock the queue so only the scheduler threadtask thread can access it.
        with (self.__fMonitor):
        
            # anything in the queue to process?
            while (self.__fQueue.Count == 0):
            
                # no - were we asked to stop?  if so, then we are done.
                if (self.__fStopped):
                    break

                # is main thread still alive?  if not, then we are done.
                if (not threading.main_thread().is_alive()):
                    break

                # continue waiting until we receive a pulse from the main thread
                # that it added something to the queue (or asked us to stop).
                self.__fMonitorCondition.wait()

            # ensure the queue has not been destroyed (in case of shutdown).
            if (self.__fQueue != None):
            
                # pull as many items off of the queue that will fit in our buffer.
                # we will return how many items we pulled off of the queue.
                while (self.__fQueue.Count > 0):
                
                    self.__fBuffer[count] = self.__fQueue.Dequeue()
                    count = count + 1

                    if (count >= length):
                        break

            # inform the main thread that it can process the buffer
            # of commands that we just dequeued.
            self.__fMonitorCondition.notify_all()

        return count


    def __RunCommand(self, command:SchedulerCommand) -> None:
        """
        Processes a dequeued command.

        Args:
            command (SchedulerCommand):
                The dequeued command to run.

        This method is executed by the __SchedulerThreadTask.
        """
        # Process the dequeued command. The Impl methods cannot
        # throw an exception. Exceptions are reported with the
        # error event of the protocol in asynchronous mode.

        action:SchedulerAction = command.Action

        if (action == SchedulerAction.Connect):
            self.__fProtocol._ImplConnect()
        elif (action == SchedulerAction.WritePacket):
            packet:Packet = command.State
            self.__fProtocol._ImplWritePacket(packet)
        elif (action == SchedulerAction.Disconnect):
            self.__fProtocol._ImplDisconnect()
        elif (action == SchedulerAction.Dispatch):
            cmd:ProtocolCommand = command.State
            self.__fProtocol._ImplDispatch(cmd)


    def __RunCommands(self, count:int) -> bool:
        """
        Runs the specified number of commands in the queue.

        Args:
            count (int):
                The number of commands to run.

        Returns:
            True if all commands were run successfully, otherwise False.

        This method is executed by the __SchedulerThreadTask.
        """
        for i in range(count):
        
            stopped:bool = self.__fStopped

            command:SchedulerCommand = self.__fBuffer[i]
            if (command != None):
                self.__RunCommand(command)
            self.__fBuffer[i] = None

            if (not stopped):
                continue

            # The scheduler has been stopped before the last
            # command has been processed. To shutdown this
            # thread as fast as possible we check if the last
            # command of the protocol has failed (or if the
            # last command has failed to change the previous
            # failure status, respectively). If this is the
            # case, we clear the queue and exit this thread
            # immediately.
            if (self.__fProtocol.Failed):
            
                self.Clear()
                return False

        return True
