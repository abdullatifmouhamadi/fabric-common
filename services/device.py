from fabric_common.common.build import Build

class Device:
    def __init__(self, ssh, app):
        """
        Build construct
        """
        ##
        self.ssh        = ssh
        self.bash       = ssh.bash
        self.app        = app
        self.installDir = app['install_dir']

        self.pre_build()


        self.loopbackdev = None



    def pre_build(self):
        self.bash.mkdir(self.installDir)
        self.bash.chown(owner   = '{}:wheel'.format(self.ssh.ssh_user), pattern = self.installDir)


    #https://disconnected.systems/blog/raspberry-pi-archlinuxarm-setup/
    def create_image_file(self, name, size, path):

        # Create an image file
        self.bash.remove("{}/{}".format(path, name))
        self.bash.run('cd {} && fallocate -l {} "{}"'.format(path, size, name))

        result           = self.bash.sudo('losetup --find --show {}/{}'.format(path, name))
        self.loopbackdev = result.stdout.strip()

        # Format and mount the device
        p1 = self.loopbackdev+'p1'
        p2 = self.loopbackdev+'p2'
        

        self.bash.sudo('parted --script {} mklabel msdos'.format(self.loopbackdev))
        self.bash.sudo('parted --script {} mkpart primary fat32 0% 100M'.format(self.loopbackdev))
        self.bash.sudo('parted --script {} mkpart primary ext4 100M 100%'.format(self.loopbackdev))
        

        self.bash.sudo("mkfs.vfat -F32 %s" % p1)
        self.bash.sudo("mkfs.ext4 -F %s" % p2)


        self.bash.sudo("mkdir -p %s/mnt" % self.installDir)

        self.bash.sudo("mount {} {}/mnt".format(p2, self.installDir))
        self.bash.sudo("mkdir %s/mnt/boot" % self.installDir)
        self.bash.sudo("mount {} {}/mnt/boot".format(p1, self.installDir))


        # Install the base system









    def post_build(self):
        """
        deteach
        """
        self.bash.sudo('losetup --detach "{}"'.format(self.loopbackdev))
        
        #print("result '%s'" % self.loopbackdev)




    def setup(self):
        """
        Préeliminaires
        """
        Build(bash      = self.bash, 
              src_dir   = self.app['src_dir'], 
              build_dir = self.app['build_dir'], 
              repo      = self.app['repo'], 
              branch    = self.app['branch'],
              owner     = self.ssh.ssh_user)

