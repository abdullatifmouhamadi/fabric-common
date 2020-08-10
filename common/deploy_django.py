from settings import APPS, PROJECT_NAME
from common.deploy import Deployable

class DeployDjango(Deployable):

    def __init__(self, app_name, app_stage, params):
        Deployable.__init__(self, stage = app_stage, app_name = app_name, params = params)

        self.db_conf_file        = self.appDir + '/src/project/common/config/database/dbconfig.py'
        self.django_setting_file = self.appDir + '/src/project/project/settings.py'
        self.celery_conf_file    = self.appDir + '/src/project/project/taskconf/main.py'
        self.biachara_conf_file  = self.appDir + '/src/project/common/config/biachara.py'


    def setup_python_env(self):
        print("\n\n==> setup_python_env\n\n")
        self.rc.chmod(permissions = '+x',
                      pattern     = self.appDir + '/script/setup.sh')
        self.cnx.run('cd {} && \
                     ./script/setup.sh \
                     '.format(self.appDir))

    # @deprecated
    def setup_django_env(self):
        self.cnx.run('cd {} && \
                       source venv/bin/activate && \
                       cd src/project && \
                       python manage.py makemigrations && \
                       python manage.py migrate && \
                       python manage.py collectstatic --noinput \
                      '.format(self.appDir))

    def setup_django_settings(self):
        #self.rc.sed(self.django_setting_file, "DEBUG = True", "DEBUG = False")
        self.rc.sed(self.django_setting_file, r"ALLOWED_HOSTS = \[\]", 'ALLOWED_HOSTS = ["{}","{}"]'.format(self.stage['host'], 'www.' + self.stage['host']))



    def config_database_conf_file(self):
        print("\n\n==> config_database\n\n")
        mybiachara_dbname        = self.db_name
        mybiachara_username      = self.db_username
        mybiachara_password      = self.db_password
        
        mybiachara_dbname_test   = self.db_name_test
        mybiachara_username_test = self.db_username_test
        mybiachara_password_test = self.db_password_test

        # :-) very important to begin with test
        self.rc.sed(self.db_conf_file, 'mybiachara_dbname_test', mybiachara_dbname_test)
        self.rc.sed(self.db_conf_file, 'mybiachara_username_test', mybiachara_username_test)
        self.rc.sed(self.db_conf_file, 'mybiachara_password_test', mybiachara_password_test)

        self.rc.sed(self.db_conf_file, 'mybiachara_dbname', mybiachara_dbname)
        self.rc.sed(self.db_conf_file, 'mybiachara_username', mybiachara_username)
        self.rc.sed(self.db_conf_file, 'mybiachara_password', mybiachara_password)


    def setup_database(self):
        self.setup_database_and_access(dbname    = self.db_name, 
                                       username  = self.db_username, 
                                       password  = self.db_password)
        self.setup_database_and_access(dbname    = self.db_name_test, 
                                       username  = self.db_username_test, 
                                       password  = self.db_password_test)

                                       
    def setup_celery(self):
        print("\n\n=> setting up celery\n\n")
        DATAMANAGER_USER     = self.rabbitmq_username
        DATAMANAGER_PASSWORD = self.rabbitmq_password
        DATAMANAGER_VHOST    = self.rabbitmq_vhost

        self.rc.sed(self.celery_conf_file, 'DATAMANAGER_USER', DATAMANAGER_USER)
        self.rc.sed(self.celery_conf_file, 'DATAMANAGER_PASSWORD', DATAMANAGER_PASSWORD)
        self.rc.sed(self.celery_conf_file, 'DATAMANAGER_VHOST', DATAMANAGER_VHOST)

        try:
            self.setup_rabbitmq_appuser()
        except:
            print("Already exists Maybe")

