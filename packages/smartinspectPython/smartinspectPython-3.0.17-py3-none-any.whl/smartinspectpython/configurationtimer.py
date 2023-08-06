"""
Module: configurationtimer.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  
| 2023/06/09 | 3.0.8.0     | Added call to RaiseInfoEvent for when a configuration settings file is changed and reloaded.

</details>
"""

import os
import _threading_local
import threading
from ctypes import ArgumentError
from datetime import datetime, timedelta

# our package imports.
from .dotnetcsharp import ArgumentNullException
from .smartinspect import SmartInspect

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class ConfigurationTimer:
    """
    Monitors a SmartInspect configuration settings file for changes
    and reloads the configuration when it does.

    Use this class to monitor and automatically reload SmartInspect
    configuration files.  This class periodically checks if the
    related configuration file has changed (by comparing the last
    modified datetime) and automatically tries to reload the configuration
    properties. You can pass the SmartInspect object to configure,
    the path of the configuration file to monitor, and the interval
    in which the path should check for changes.

    For information about SmartInspect configuration files, please
    refer to the documentation of the SmartInspect.LoadConfiguration
    method.

    Threadsafety:
        This class is fully thread-safe.

    <details>
        <summary>View Sample Code</summary>
    ```python
    .. include:: ../docs/include/samplecode_configurationtimer.md
    ```

    The following is the configuration settings file contents:
    ```python
    .. include:: ../docs/include/samplecode_smartinspect_config.md
    ```
    </details>
    """

    def __init__(self, smartInspect:SmartInspect, fileName:str, interval:int=60) -> None:
        """
        Initializes a new instance of the class.

        Args:
            smartInspect (SmartInspect):
                The SmartInspect object to configure.
            fileName (str):
                The path of the configuration file to monitor.
            interval (int):
                The interval (in seconds) in which this timer should check for changes
                to the configuration file.
                Default value is 60 (seconds).

        Raises:
            ArgumentNullException:
                The smartInspect or fileName parameter is null.
            ArgumentError:
                The interval parameter is less than 1 or greater than 300 (seconds).

        The monitoring of the file begins immediately.
        """
        # validations:
        if (smartInspect == None):
            raise ArgumentNullException("smartInspect")
        if (fileName == None):
            raise ArgumentNullException("fileName")
        if ((interval < 1) or (interval > 300)):
            raise ArgumentError("Interval argument must be in the range of 1 to 300 (seconds).")

        # initialize instance.
        self.__fLock:object = _threading_local.RLock()
        self.__fSmartInspect = smartInspect
        self.__fFileName:str = fileName
        self.__fInterval:int = interval
        self.__fIntervalNextCheck:datetime = datetime.utcnow()
        self.__fFileDateModified:datetime = datetime.min
        self.__fMonitorCondition:threading.Condition = threading.Condition(self.__fLock)
        self.__fStarted = False
        self.__fStopped = False

        # start monitoring the file for changes.
        self.Start()


    @staticmethod
    def _GetFileAge(fileName:str) -> bool:
        """
        Gets the last modified date time of the specified file path.

        Args:
            fileName (str):
                The path of the configuration file to monitor.

        Returns:
            (bool):
                True if the function was successful; otherwise, false.
            (datetime):
                datetime of file last modified date if the function was successful;
                otherswise, datetime.min if not.

        No exception will be thrown by this method.
        """
        result:bool = False
        age:datetime = None

        try:
            
            # get last modified date time of file.
            ts = os.path.getmtime(fileName)     # returns timestamp
            age = datetime.fromtimestamp(ts)    # converts timestamp to datetime
            result = True
        
        except Exception as ex:
        
            # if file info could not be obtained, then return False to indicate failure.
            age = datetime.min
            result = False

        return result, age


    def Start(self) -> None:
        """
        Starts monitoring the configuration file for changes.

        This method is called automatically when a new instance of the class 
        is created.  It can also be called after issuing a "Stop" method
        call, to restart monitoring of the configuration file.

        It will start a new thread named "SiConfigFileMonitorTask" that will
        monitor a specified configuration file for changes at a selected
        interval, and reload the configuration automatically.
        """
        with (self.__fLock):

            # if threadtask is already running then don't bother.
            if (self.__fStarted):
                return

            # get last modified date time of specified configuration file path.
            result, self.__fFileDateModified = ConfigurationTimer._GetFileAge(self.__fFileName)

            # reset stop requested status.
            self.__fStopped = False

            # start the thread task to monitor the file.
            self.__fThread = threading.Thread(target=self.__MonitorFileTask, args=(self,))
            self.__fThread.name = "SiConfigFileMonitorTask"
            self.__fThread.start()

            # indicate we are monitoring.
            self.__fStarted = True


    def Stop(self) -> None:
        """
        Stops monitoring the configuration file for changes.
        """
        with (self.__fLock):

            # if threadtask has not started yet then we are done.
            if (not self.__fStarted):
                return

            # inform the thread task we want it to stop.
            self.__fStopped = True
            self.__fMonitorCondition.notify_all()

        # wait for the monitoring threadtask to finish up.
        if (self.__fThread != None):
            self.__fThread.join()

        # reset threadtask object.
        self.__fThread = None


    def __MonitorFileTask(self, instance) -> None:
        """
        Periodically checks the last modified datetime of a configuration
        file to see if it has changed, and reloads the configuration if so.
        """
        try:

            # process until we are asked to stop by main thread.
            while (True):

                with (self.__fLock):
        
                    # were we asked to stop?  if so, then we are done.
                    if (self.__fStopped):
                        break

                    # is main thread still alive?  if not, then we are done.
                    if (not threading.main_thread().is_alive()):
                        break

                    # has interval been reached since last check?
                    if (datetime.utcnow() >= self.__fIntervalNextCheck):

                        # calculate next interval check datetime.
                        self.__fIntervalNextCheck = datetime.utcnow() + timedelta(seconds=self.__fInterval)

                        # get last modified date time of specified configuration file path.
                        lastUpdate:datetime = None
                        result, lastUpdate = ConfigurationTimer._GetFileAge(self.__fFileName)

                        # did we get the last modified datetime?
                        if (result):

                            # yes - has file changed since the last time we checked?
                            # if so, then save the last modified date and reload configuration.
                            if (lastUpdate > self.__fFileDateModified):
                                self.__fFileDateModified = lastUpdate
                                self.__fSmartInspect.RaiseInfoEvent("SI Configuration File change detected - reloading configuration from file \"{0}\"".format(self.__fFileName))
                                self.__fSmartInspect.LoadConfiguration(self.__fFileName)

                        # wait until we receive a pulse from the main thread
                        # that it asked us to stop, or a timeout of 1 second occurs.
                        # this keeps the thread responsive and prevents shutdown hanging.
                        self.__fMonitorCondition.wait(1)

        except Exception as ex:
        
            # ignore exceptions.
            pass
