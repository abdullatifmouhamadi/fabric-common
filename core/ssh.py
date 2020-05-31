from .command import RemoteCommand
from .connection import ConnectionManager
from fabric import Remote
from patchwork.files import directory, exists



class SSH:
    def __init__(self, credentials):
        """
            init
        """
        self.ssh_host = credentials['host']
        self.ssh_user = credentials['user']
        self.ssh_pass = credentials['password']


        self.manager = ConnectionManager(self.ssh_host, self.ssh_user, self.ssh_pass)
        self.cnx = self.manager.connect()
        self.bash = RemoteCommand(conn = self.cnx)






