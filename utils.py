
import getpass
from invoke import Responder
from fabric import Connection, Config
import psycopg2

FAKE_NOT_USED_LOCAL_PORT = 5433

class ConnectionManager:
    def __init__(self, stage):
        self.stage = stage

        # Autentication
        self.sudo_pass = 'Houda2016'#getpass.getpass("What's your sudo password?")
        self.config = Config(overrides={'sudo': {'password': self.sudo_pass}})

        self.cnx = None

    def connect(self):
        if (self.cnx == None):
            self.cnx = Connection( host=self.stage['host'], 
                                   user=self.stage['user'],
                                   connect_kwargs = {
                                        "password":self.sudo_pass
                                   },
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




