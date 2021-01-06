from fabric_common.utils import ConnectionManager
from settings import APPS, PROJECT_CREDENTIALS
from clusters import CLUSTERS
from fabric import Remote

from patchwork.files import directory, exists




class Deployable:
    def __init__(self, stage, app_name, params):
        self.stage        = stage
        self.app          = APPS[app_name]
        self.params       = params
        self.project_key  = self.app['projectkey']
        self.credentials  = PROJECT_CREDENTIALS[self.project_key]
        self.cluster      = CLUSTERS[params.get('cluster')]


        self.manager = ConnectionManager(cluster = self.cluster)

        self.cnx = self.manager.connect()
        self.rc = RemoteCommand(conn = self.cnx)

        # pg
        self.db = RemotePgsql(manager = self.manager)

        # render
        self.appDir = self.stage['code_dir'] + '/' + self.app['dir_name']
        
        # biachara.dashboard-dev
        # biachara.dashboard-dev.service
        self.nginx_filename  = self.project_key + '.' + self.app['name'] + '-' + self.stage['name']
        self.daemon_filename = self.project_key + '.' + self.app['name'] + '-' + self.stage['name'] + '.service'
        self.port = self.app['port_prefix'] + self.stage['port_suffix']


        # nginx files

        self._NGINX_AVAILABLE_BASE = '/etc/nginx/sites-available'
        self._NGINX_ENABLED_BASE   = '/etc/nginx/sites-enabled'

        self.nginx_available   = '{}/{}'.format(self._NGINX_AVAILABLE_BASE, self.nginx_filename)
        self.nginx_enabled     = '{}/{}'.format(self._NGINX_ENABLED_BASE, self.nginx_filename)

        # daemon files
        self.daemon_location     = '/etc/systemd/system/{}'.format(self.daemon_filename)


        # certbot
        self.certbot_fullchain = '/etc/letsencrypt/live/'+self.stage['host']+'/fullchain.pem'

        # database
        self.db_name          = self.project_key+'_'+self.stage['name']
        self.db_username      = self.credentials['db_username'] # deprecated
        self.db_password      = self.credentials['db_password'] # deprecated

        self.db_name_test     = self.db_name+'_'+'test'
        self.db_username_test = self.credentials['db_username']
        self.db_password_test = self.credentials['db_password']

        # new database
        self.pgdb_name          = 'db_' + self.project_key + '_' + self.app['name'] + '_' + self.stage['name']
        self.pgdb_username      = self.project_key + '_' + self.app['name'] + '_' + self.stage['name']
        self.pgdb_username      = self.pgdb_username.replace('-','_')
        self.pgdb_password      = self.credentials['db_password']


        # rabbitMQ
        self.rabbitmq_username = self.project_key + '_' + self.app['name'] + '_' + self.stage['name']
        self.rabbitmq_password = "change_me_please"
        self.rabbitmq_vhost    = self.project_key + '_' + self.app['name'] + '_' + self.stage['name'] + '_vhost'


    def setup_rabbitmq_appuser(self):
        print("\n\n=> setting up rabbitmq\n\n")
        self.cnx.sudo('rabbitmqctl add_user {} {}'.format(self.rabbitmq_username, self.rabbitmq_password))
        self.cnx.sudo('rabbitmqctl set_user_tags {} administrator'.format(self.rabbitmq_username))
        self.cnx.sudo('rabbitmqctl add_vhost {}'.format(self.rabbitmq_vhost))
        #self.cnx.sudo('rabbitmqctl set_permissions -p / {} ".*" ".*" ".*"'.format(self.rabbitmq_username))
        self.cnx.sudo('rabbitmqctl set_permissions -p {} {} ".*" ".*" ".*"'.format(self.rabbitmq_vhost, self.rabbitmq_username))



    def pre_deploy(self):
        self.rc.mkdir(self.appDir)
        self.rc.chown(owner   = '{}:wheel'.format(self.stage['user']), 
                      pattern = self.stage['code_dir'])


    def setup_database_and_access(self, dbname, username, password):
        self.db.create_db(dbname     = dbname)
        self.db.create_role(role     = username, 
                            password = password)
        self.db.grant_all(dbname     = dbname,
                          role       = username)



    def setup_git_env(self):
        print("\n\n==> setup_git_env\n\n")
        if not exists(self.cnx, self.appDir + '/.git'):
            self.rc.clone(branch  = self.stage['branch'], 
                          repo    = self.app['repo'], 
                          pattern = self.appDir)
                        
        result = self.rc.reset(branch  = self.stage['branch'], 
                               pattern = self.appDir)




    # not working -> exists doesn'- work (i suspect it works only if the 'deploy' user own the file)
    def setup_certbot_ssl(self):
        if (self.params['certbot'] == False):
            return False
        
        print("\n\n==> setup_certbot_ssl\n\n")
        if not self.rc.file_exists(pattern = self.certbot_fullchain): # create them
            self.rc.certbot(param = self.stage['host'] +',www.' + self.stage['host'])
            return False
        else:
            return True
            



    def post_deploy(self):
        self.rc.chown('http:http', self.stage['code_dir'])


class RemotePgsql:
    def __init__(self, manager):
        self.m = manager
    
    def create_db(self, dbname):
        try:
            self.m.executepg(statement = 'CREATE DATABASE {};'.format(dbname))
            return True
        except:
            return False

    def create_role(self, role, password = ''):
        try:
            if password != '':
                self.m.executepg(statement = "CREATE USER {} WITH ENCRYPTED PASSWORD '{}' CREATEDB;".format(role, password))
            else:
                self.m.executepg(statement = "CREATE USER {} CREATEDB;".format(role))

            return True
        except:
            return False

    def grant_all(self, dbname, role):
        try:
            self.m.executepg(statement = "GRANT ALL PRIVILEGES ON DATABASE {} TO {};".format(dbname, role))
            return True
        except:
            return False

    def assign_owner(self, dbname, owner):
        try:
            self.m.executepg(statement = "ALTER DATABASE {} OWNER TO {};".format(dbname, owner))
            return True
        except:
            return False


class RemoteCommand:
    def __init__(self, conn):
        self.cnx = conn
    
    def mkdir(self, path):
        self.cnx.sudo('mkdir -p {}'.format(path))

    def chown(self, owner, pattern):
        self.cnx.sudo('chown -hR {} {}'.format(owner, pattern))
    
    def clone(self, branch, repo, pattern):
        try:
            self.cnx.run('git clone -b {} {} {}'.format(branch, repo, pattern))
        except:
            return False
        return True

    def pull(self, branch, pattern):
        try:
            r = self.cnx.run('cd {} && git pull origin {} && git submodule update --init --recursive && git config --global submodule.recurse true'.format(pattern, branch))
            return r
        except:
            return False
        return True

    def reset(self, branch, pattern):
        try:
            r = self.cnx.run('cd {} && git fetch origin&& git reset --hard origin/{} && git submodule update --init --recursive && git config --global submodule.recurse true'.format(pattern, branch))
            return r
        except:
            return False
        return True


    
    def chmod(self, permissions, pattern):
        self.cnx.sudo('chmod {} {}'.format(permissions, pattern))

    def sed(self, pattern, old, new):
        self.cnx.sudo("sed -i 's/{}/{}/g' {}".format(old, new, pattern))

    def copy(self, src, target):
        self.cnx.sudo('cp -rf {} {}'.format(src, target))

    def remove(self, target):
        self.cnx.sudo('rm -rf {}'.format(target))

    def linksoft(self, src, target):
        self.cnx.sudo('ln -sf {} {}'.format(src, target))

    def reloadnginx(self):
        self.cnx.sudo('sudo systemctl reload nginx')


    def certbot(self, param):
        self.cnx.sudo('sudo certbot certonly --email bourou01@gmail.com --webroot -w /var/lib/letsencrypt/ -d {}'.format(param))
        print('sudo certbot certonly --email bourou01@gmail.com --webroot -w /var/lib/letsencrypt/ -d {}'.format(param))


    def directory_exists(self, pattern):
        try:
            result = self.cnx.sudo('[ -d {} ] && echo "True"'.format(pattern))
            if ("True" in result.stdout.strip()):
                return True
        except:
            return False
        return False

    def file_exists(self, pattern):
        try:
            result = self.cnx.sudo('[ -f {} ] && echo "True"'.format(pattern))
            if ("True" in result.stdout.strip()):
                return True
        except:
            return False
        return False


    def daemonreload(self):
        self.cnx.sudo('systemctl daemon-reload')



    def stopdaemon(self, service):
        try:
            self.cnx.sudo('systemctl stop {}'.format(service))
            return True
        except:
            return False
        return False

    def startdaemon(self, service):
        try:
            self.cnx.sudo('systemctl restart {}'.format(service))
            return True
        except:
            return False
        return False

    def run(self, command):
        self.cnx.run(command)


    def sudo(self, command):
        self.cnx.sudo(command)
    
    
    def db_exists(self, dbname):
        result = self.cnx.run('psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname={}"'.format("'"+dbname+"'"))
        if ("1" in result.stdout.strip()):
            return True
        return False