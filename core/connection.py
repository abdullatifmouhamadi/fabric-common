
import getpass
from invoke import Responder
from fabric import Connection, Config
import psycopg2

FAKE_NOT_USED_LOCAL_PORT = 5433

class ConnectionManager:
    def __init__(self, host, user, password):
        self.ssh_host = host
        self.ssh_user = user
        self.ssh_pass = password

        # Autentication
        self.config = Config(overrides={'sudo': {'password': self.ssh_pass}})
        self.cnx = None

    def connect(self):
        if (self.cnx == None):
            self.cnx = Connection( host=self.ssh_host, 
                                   user=self.ssh_user,
                                   connect_kwargs = { "password":self.ssh_pass },
                                   config = self.config, )
        return self.cnx



    
    def executepg(self, statement):
        with self.connect().forward_local(local_port  = FAKE_NOT_USED_LOCAL_PORT,
                                          remote_port = 5432):
            db = psycopg2.connect(
                host='localhost', 
                port=FAKE_NOT_USED_LOCAL_PORT, 
                user='postgres', 
                database='postgres'
            )
            db.autocommit = True
            cur = db.cursor()
            r = cur.execute( statement )
            return r
            #print(cur)




