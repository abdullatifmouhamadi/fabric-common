



class RemoteCommand:
    def __init__(self, conn):
        self.cnx = conn


    def pwd(self):
        self.cnx.run('pwd')

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