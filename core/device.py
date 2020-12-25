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
        #self.bash.chown(owner   = '{}:wheel'.format(self.ssh.ssh_user), pattern = self.installDir)


    #https://disconnected.systems/blog/raspberry-pi-archlinuxarm-setup/
    def create_image_file(self, name, size, path):

        if self.bash.file_exists(pattern="{}/{}".format(path, name)):
            print("imageALREADY EXISTS")
            return False

        # Create an image file
        self.bash.remove("{}/{}".format(path, name))

        self.bash.sudo('fallocate -l {} {}/{}'.format(size, path, name))


        """
        result           = self.bash.sudo('losetup --find --show {}/{}'.format(path, name))
        self.loopbackdev = result.stdout.strip()
        """
        self.bind_filesystem(path = path, name = name)


        # Format and mount the device
        p1 = self.loopbackdev+'p1'
        p2 = self.loopbackdev+'p2'
        

        self.bash.sudo('parted --script {} mklabel msdos'.format(self.loopbackdev))
        self.bash.sudo('parted --script {} mkpart primary fat32 0% 100M'.format(self.loopbackdev))
        self.bash.sudo('parted --script {} mkpart primary ext4 100M 100%'.format(self.loopbackdev))
        

        self.bash.sudo("mkfs.vfat -F32 %s" % p1)
        self.bash.sudo("mkfs.ext4 -F %s" % p2)

        """
        self.bash.sudo("mkdir -p %s/mnt" % path)

        self.bash.sudo("mount {} {}/mnt".format(p2, path))
        self.bash.sudo("mkdir %s/mnt/boot" % path)
        self.bash.sudo("mount {} {}/mnt/boot".format(p1, path))
        """
        self.mount_image(device = self.loopbackdev, path = path)

        # Install the base system

        self.bash.sudo('bsdtar -xpf {}/ArchLinuxARM-rpi-2-latest.tar.gz -C {}/mnt'.format(path, path) )



        # umount and clean
        self.bash.sudo("umount -l {}/mnt/boot || /bin/true".format(path))
        self.bash.sudo("umount -l {}/mnt || /bin/true".format(path))
        
        self.bash.sudo('losetup --detach "{}"'.format(self.loopbackdev))



    def bind_filesystem(self, path, name):
        if self.loopbackdev == None:
            result           = self.bash.sudo('losetup --find --show {}/{}'.format(path, name))
            self.loopbackdev = result.stdout.strip()

        return self.loopbackdev


    def mount_filesystem(self, path, name):
        if self.loopbackdev == None:
            result           = self.bash.sudo('losetup --find --show -P {}/{}'.format(path, name))
            self.loopbackdev = result.stdout.strip()

        return self.loopbackdev      



    def mount_image(self, device, path):
        p1 = device + 'p1'
        p2 = device + 'p2'

        self.bash.sudo("mkdir -p %s/mnt" % path)

        self.bash.sudo("mount {} {}/mnt".format(p2, path))
        self.bash.sudo("mkdir -p %s/mnt/boot" % path)
        self.bash.sudo("mount {} {}/mnt/boot".format(p1, path))


    def pre_chroot(self, path, name):

        if self.mounted(path=path):
            print("imageALREADY MOUNTED")
            return False


        device = self.mount_filesystem(path=path, name=name)
        self.mount_image(device=device, path=path)
        #print("imageALREADY MOUNTED")
        #return False
        

        self.bash.sudo("mount -t proc none {}/mnt/proc || /bin/true".format(path))
        self.bash.sudo("mount -t sysfs none {}/mnt/sys || /bin/true".format(path))
        self.bash.sudo("mount -o bind /dev {}/mnt/dev || /bin/true".format(path))

        self.bash.sudo("mv {}/mnt/etc/resolv.conf {}/mnt/etc/resolv.conf.bak || /bin/true".format(path, path))
        self.bash.sudo("cp /etc/resolv.conf {}/mnt/etc/resolv.conf || /bin/true".format(path))
        self.bash.sudo("cp /usr/bin/qemu-arm-static {}/mnt/usr/bin/ || /bin/true".format(path))


    def chroot(self, path, cmd):
        if not self.mounted(path=path):
            print("imageNOT MOUNTED")
            return False

        self.bash.sudo("chroot {}/mnt {}".format(path, cmd))




    def mounted(self, path):
        result = self.bash.sudo('mountpoint -q %s/mnt && echo "mounted" || echo "not mounted"' % path)
        if result.stdout.strip() == "mounted":
            return True
        else:
            return False
        #print(result.stdout.strip())



    def umount(self, path):

        self.bash.sudo("rm {}/mnt/etc/resolv.conf || /bin/true".format(path))
        self.bash.sudo("mv {}/mnt/etc/resolv.conf.bak {}/mnt/etc/resolv.conf || /bin/true".format(path, path))
        self.bash.sudo("rm {}/mnt/usr/bin/qemu-arm-static || /bin/true".format(path))


        self.bash.sudo("umount -l {}/mnt/dev || /bin/true".format(path))
        self.bash.sudo("umount -l {}/mnt/proc || /bin/true".format(path))
        self.bash.sudo("umount -l {}/mnt/sys || /bin/true".format(path))


        self.bash.sudo("umount -l {}/mnt/boot || /bin/true".format(path))
        self.bash.sudo("umount -l {}/mnt || /bin/true".format(path))


    def get_binded_dev(self, path, name):
        result = self.bash.sudo('losetup --list | awk \'{{if ($6 = "{}/{}") print $1;}}\' '.format(path, name))
        stdout = result.stdout.strip()
        params = stdout.split('\n')
        if len(params) > 1:
            return params[1]
        return None


    def post_build(self, path, name):
        """
            Cleaning Up
        """
        self.umount(path=path)


        device = self.get_binded_dev(path, name)
        self.bash.sudo('losetup --detach "{}"'.format(device))


        """
        if self.loopbackdev:
            self.bash.sudo('losetup --detach "{}"'.format(self.loopbackdev))
        """
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
              owner     = self.ssh.ssh_user,
              nopull    = False)

