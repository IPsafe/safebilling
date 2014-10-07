import re
import ESL 

# Default
defaultESLport = 8021
defaultESLsecret = 'ClueCon'
conn_timeout = 5


class FSinfo:
    """Class that establishes connection to FreeSWITCH ESL Interface
    to retrieve statistics on operation.

    """

    def __init__(self, host='127.0.0.1', port=defaultESLport, secret="ClueCon", 
                 autoInit=True):
        """Initialize connection to FreeSWITCH ESL Interface.
        
        @param host:     FreeSWITCH Host
        @param port:     FreeSWITCH ESL Port
        @param secret: FreeSWITCH ESL Secret
        @param autoInit: If True connect to FreeSWITCH ESL Interface on 
                         instantiation.
                         
        >>> fs = FSinfo(host='127.0.0.1', port=defaultESLport, secret="ClueCon")
		>>> print fs.getChannelCount()
		0
		>>> print fs.getReloadGateway()

        """
        # Set Connection Parameters
        self._eslconn = None
        self._eslhost = host or '127.0.0.1'
        self._eslport = int(port or defaultESLport)
        self._eslpass = secret or defaultESLsecret
        
        ESL.eslSetLogLevel(0)
        if autoInit:
            self._connect()

    def __del__(self):
        """Cleanup."""
        if self._eslconn is not None:
            del self._eslconn

    def _connect(self):
        """Connect to FreeSWITCH ESL Interface."""
        try:
            self._eslconn = ESL.ESLconnection(self._eslhost, 
                                              str(self._eslport), 
                                              self._eslpass)
        except:
            pass
        if not self._eslconn.connected():
            raise Exception(
                "Connection to FreeSWITCH ESL Interface on host %s and port %d failed."
                % (self._eslhost, self._eslport)
                )
    
    def _execCmd(self, cmd, args):
        """Execute command and return result body as list of lines.
        
            @param cmd:  Command string.
            @param args: Command arguments string. 
            @return:     Result dictionary.
            
        """
        command = cmd + " " + args
        print command
        print command.encode('utf-8')
        output = self._eslconn.sendRecv(command.encode('utf-8'))
        body = output.getBody()
        if body:
            return body.splitlines()
        return None
    
    def _execShowCmd(self, showcmd):
        """Execute 'show' command and return result dictionary.
        
            @param cmd: Command string.
            @return: Result dictionary.
            
        """
        result = None
        lines = self._execCmd("show", showcmd)
        if lines and len(lines) >= 2 and lines[0] != '' and lines[0][0] != '-':
            result = {}
            result['keys'] = lines[0].split(',')
            items = []
            for line in lines[1:]:
                if line == '':
                    break
                items.append(line.split(','))
            result['items'] = items
        return result
    
    def _execShowCountCmd(self, showcmd):
        """Execute 'show' command and return result dictionary.
        
            @param cmd: Command string.
            @return: Result dictionary.
            
        """
        result = None
        lines = self._execCmd("api show", showcmd + " count")
        for line in lines:
            mobj = re.match('\s*(\d+)\s+total', line)
            if mobj:
                return int(mobj.group(1))
        return result

    def getChannelCount(self):
        """Get number of active channels from FreeSWITCH.
        
        @return: Integer or None.
        
        """
        return self._execShowCountCmd("channels")
        
    def getReloadACL(self):
        """Reload ACL"""
        result = None
        return self._execCmd("bgapi", "reloadacl")

        
    def getReloadGateway(self, profile_name):
        """Reload sofia's gateway"""
        result = None
        return self._execCmd("bgapi", "sofia profile " + profile_name + " rescan reloadxml")
        
        
    def getRestartSofia(self, profile_name):
        """Restart sofia profile"""
        result = None
        return self._execCmd("bgapi", "sofia profile " + profile_name + " restart")

    def getRestartSofiaAll(self):
        """Restart sofia profile"""
        result = None
        return self._execCmd("bgapi", "sofia profile restart all")


    def getRestartSofiaAll(self):
        """Restart sofia profile"""
        result = None
        return self._execCmd("bgapi", "sofia profile restart all")        
        
    def getReloadxml(self):
        """Restart sofia profile"""
        result = None
        return self._execCmd("bgapi", "reloadxml")        

# fs = FSinfo(host='127.0.0.1', port=defaultESLport, secret="ClueCon")
# print fs.getChannelCount()
# print fs.getReloadGateway("external")
