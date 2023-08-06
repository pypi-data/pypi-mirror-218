"""
Module: sessionmanager.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

import _threading_local

# our package imports.
from .dotnetcsharp import ArgumentNullException
from .level import Level
from .configuration import Configuration
from .session import Session
from .sessioninfo import SessionInfo
from .sessiondefaults import SessionDefaults

from .const import (
    DEFAULT_COLOR_VALUE
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SessionManager:
    """ 
    Manages and configures Session instances.
    
    This class manages and configures a list of sessions. Sessions
    can be configured and added to the list with the Add method. To
    lookup a stored session, you can use Get. To remove an existing
    session from the list, call Delete.

    Stored sessions will be reconfigured if LoadConfiguration has
    been called and contains corresponding session entries.

    Threadsafety:
        This class is fully thread-safe.
    """

    # static constants.
    PREFIX:str = "session."
    PREFIX_LEN:int = len(PREFIX)

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        self.__fLock:object = _threading_local.RLock()
        self.__fDefaults:SessionDefaults = SessionDefaults()
        self.__fSessions = {}
        self.__fSessionInfos = {}


    @property
    def Defaults(self) -> SessionDefaults:
        """
        Specifies the default property values for new sessions.

        This property lets you specify the default property values
        for new sessions which will be passed to the Add method.
        Please see the Add method for details. For information about
        the available session properties, please refer to the
        documentation of the Session class.
        """
        return self.__fDefaults


    def Add(self, session:Session, store:bool) -> None:
        """
        Configures a passed Session instance and optionally saves it
        for later access.

        Args:
            session (Session):
                The session to configure and to save for later access, if desired.
            store (bool):
                Indicates if the passed session should be stored for later access.

        This method configures the passed session with the default
        session properties as specified by the Defaults property.
        This default configuration can be overridden on a per-session
        basis by loading the session configuration with the
        LoadConfiguration method.

        If the 'store' parameter is true, the passed session is stored
        for later access and can be retrieved with the Get method. To
        remove a stored session from the internal list, call Delete. 

        If this method is called multiple times with the same session
        name, then the Get method operates on the session which got
        added last. If the session parameter is null, this method does nothing.
        """
        if (session == None):
            return

        with self.__fLock:
        
            self.__fDefaults.Assign(session)

            if (store):
                self.__fSessions[session.Name] = session
                session.IsStored = True

            self.Configure(session, session.Name)


    def Assign(self, session:Session, info:SessionInfo) -> None:
        """
        Assigns property values to a session instance from stored session information.

        Args:
            session (Session):
                Session to assign property values to.
            info (SessionInfo):
                Session information to retrieve property values from.
        """
        if (info.Active):

            if (info.HasColor):
                session.ColorBG = info.ColorBG

            if (info.HasLevel):
                session.Level = info.Level

            if (info.HasActive):
                session.Active = info.Active
            
        else:
            
            if (info.HasActive):
                session.Active = info.Active

            if (info.HasLevel):
                session.Level = info.Level

            if (info.HasColor):
                session.ColorBG = info.ColorBG


    def Clear(self) -> None:
        """
        Clears the configuration of this session manager and removes
        all sessions from the internal lookup table.
        """
        with self.__fLock:
            
            self.__fSessions.clear()
            self.__fSessionInfos.clear()


    def Configure(self, session:Session, sessionName:str) -> None:
        """
        Configures the specified session from stored session information.

        Args:
            session (Session):
                Session to configure.
            sessionName (str):
                Name to retrieve session information properties from.
        """
        info:SessionInfo = None
        key:str = sessionName.lower()   # SessionInfo keys are always lower-case
        if (key in self.__fSessionInfos.keys()):
            info = self.__fSessionInfos[key]

        if (info != None):
            self.Assign(session, info)


    def Delete(self, session:Session) -> None:
        """
        Removes a session from the internal list of sessions.

        Args:
            session (Session):
                The session to remove from the lookup table of sessions. 

        This method removes a session which has previously been added
        with the Add method. After this method returns, the Get method
        returns null when called with the same session name unless a
        different session with the same name has been added.

        This method does nothing if the supplied session argument is null.
        """
        if (session == None):
            return

        with self.__fLock:
        
            name:str = session.Name
            if (self.__fSessions[name] == session):
                self.__fSessions.pop(name)


    def Get(self, sessionName:str) -> Session:
        """
        Returns a previously added session.
        
        Args:
             (str):
                The name of the session to lookup and return. 
        
        Returns:
            The requested session or null if the supplied name of the
            session is unknown.
        
        Raises:
            ArgumentNullException:
                Thrown if the supplied sessionName is null, and a
                "Main" session does not exist.
        
        This method returns a session which has previously been
        added with the Add method and can be identified by the
        supplied name parameter. If the requested session is unknown
        then this method returns null.

        If sessionName is null, then the default "Main" session is
        returned if one exists.

        Note that the behavior of this method can be unexpected in
        terms of the result value if multiple sessions with the same
        name have been added. In this case, this method returns the
        session which got added last and not necessarily the session
        which you expect. 

        Adding multiple sessions with the same name should therefore be avoided.
        </para>
        """
        with (self.__fLock):

            # if session name not supplied, then try to return the 
            # default "Main" session.
            if (sessionName == None):
                if "Main" in self.__fSessions.keys():
                    return self.__fSessions["Main"]
        
            # if session name not supplied then it's a problem.
            if (sessionName != None) and (len(sessionName) == 0):
                raise ArgumentNullException("sessionName")

            # otherwise try to return the listed session name.
            if (sessionName in self.__fSessions.keys()):
                return self.__fSessions[sessionName]
            else:
                return None


    def LoadConfiguration(self, config:Configuration) -> None:
        """
        Loads the configuration properties of this session manager.
        
        Args:
            config (Configuration):
                The Configuration object to load the configuration from.

        This method loads the configuration of this session manager
        from the passed Configuration object. Sessions which have
        already been stored or will be added with Add will
        automatically configured with the new properties if the
        passed Configuration object contains corresponding session
        entries. Moreover, this method also loads the default session
        properties which will be applied to all sessions which are
        passed to Add.

        Please see the SmartInspect.LoadConfiguration method for
        details on how session entries and session defaults look
        like.
        """
        with self.__fLock:
         
            self.__fSessionInfos.clear()
            self.LoadInfos(config)
            self.LoadDefaults(config)


    def LoadDefaults(self, config:Configuration) -> None:
        """
        Loads the configuration session default properties of this session manager.
        
        Args:
            config (Configuration):
                The Configuration object to load the configuration from.

        This method will only process "SessionDefaults.x" lines, and will
        ignore the SmartInspect object configuration and "Session.x.x" lines.
        """
        self.__fDefaults.Active = config.ReadBoolean("sessiondefaults.active", self.__fDefaults.Active)
        self.__fDefaults.Level = config.ReadLevel("sessiondefaults.level", self.__fDefaults.Level)
        self.__fDefaults.ColorBG = config.ReadColor("sessiondefaults.color", self.__fDefaults.ColorBG)


    def LoadInfo(self, name:str, config:Configuration) -> SessionInfo:
        """
        Loads the configuration session instance properties of a defined
        session in this session manager.
        
        Args:
            name (str):
                The session name.
            config (Configuration):
                The Configuration object to load the configuration from.

        Returns:
            A SessionInfo object with session information.
        """
        info:SessionInfo = SessionInfo()

        # use lower-case config name, just in case ".Name" property not defined.
        info.Name = name

        info.HasName = config.Contains(SessionManager.PREFIX + name + ".name")
        if (info.HasName):
            info.Name = config.ReadString(SessionManager.PREFIX + name + ".name", name)

        info.HasActive = config.Contains(SessionManager.PREFIX + name + ".active")
        if (info.HasActive):
            info.Active = config.ReadBoolean(SessionManager.PREFIX + name + ".active", True)

        info.HasLevel = config.Contains(SessionManager.PREFIX + name + ".level")
        if (info.HasLevel):
            info.Level = config.ReadLevel(SessionManager.PREFIX + name + ".level", Level.Debug)

        info.HasColor = config.Contains(SessionManager.PREFIX + name + ".colorbg")
        if (info.HasColor):
            info.ColorBG = config.ReadColor(SessionManager.PREFIX + name + ".colorbg", DEFAULT_COLOR_VALUE)

        return info


    def LoadInfos(self, config:Configuration) -> None:
        """
        Loads the configuration session instance properties of all defined
        sessions in this session manager.
        
        Args:
             (Configuration):
                The Configuration object to load the configuration from.

        This method will only process the "session.x.x" configuration lines, and will
        ignore the SmartInspect object configuration and SessionDefaults lines.
        """

        for i in range(config.Count):

            key:str = config.ReadKey(i)

            # do we have a session here?
            if (key == None):
                continue

            # only process the "session.x.x" configuration lines.
            # session info should contain 3 parts: SESSIONPREFIX.NAME.PROPERTY.
            # for example: "session.MySessionName.Level".

            if (len(key) < SessionManager.PREFIX_LEN):
                continue    # No, too short

            prefix:str = key[0:SessionManager.PREFIX_LEN]

            if (not prefix.lower() == SessionManager.PREFIX):
                continue    # No prefix match

            suffix:str = key[SessionManager.PREFIX_LEN:]
            index:int = suffix.rindex('.')
            if (index == -1):
                continue

            # at this point we know the 3 parts are there - get the session name (middle) part.
            name:str = suffix[0:index]

            # duplicate session configuration entry?  if so, then don't add it.
            # this will occur in case multiple session properties are specified for
            # the same session name, as ALL properties for a session name are processed 
            # by the "LoadInfo()" method call below.  in this case, just ignore the 
            # property because it has already been processed.
            if (name in self.__fSessionInfos.keys()):
                continue

            info:SessionInfo = self.LoadInfo(name, config)
            self.__fSessionInfos[name] = info

            # do we need to update a related session?
            # we have to check the list one at a time because the name value from the
            # configuration file is in lower-case, but the session keys are in mixed-case!
            for sessionkey in self.__fSessions.keys():
                session:Session = self.__fSessions[sessionkey]
                if ((session != None) and (name == session.Name.lower())):
                    self.Assign(session, info)
                    break


    def Update(self, session:Session, toName:str, fromName:str) -> None:
        """
        Updates an entry in the internal lookup table of sessions.

        Args:
            session (Session):
                The session whose name has changed and whose entry should be updated.
            toName (str):
                The new name of the session.
            fromName (str):
                The old name of the session.

        Once the name of a session has changed, this method is called
        to update the internal session lookup table. The 'to' argument
        specifies the new name and 'from' the old name of the session.
        After this method returns, the new name can be passed to the
        Get method to lookup the supplied session.
        """
        if (session == None):
            return

        if (fromName == None) or (toName == None):
            return

        with self.__fLock:
        
            if (self.__fSessions[fromName] == session):
                self.__fSessions.Remove(fromName)

            self.Configure(session, toName)
            self.__fSessions[toName] = session
