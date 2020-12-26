from fabric_common.common.build import Build
from ..core.device import Device
from pprint import pprint

from sh import ls, rsync, sshpass
from sh_common.common.utils import log, logi



class Flash(Device):
    def __init__(self, ssh, app, target, params):
        Device.__init__(self, ssh, app)
        """
        Build construct
        """
        self.target = target
        self.setup()


        self.download_rootfilesystem()


        self.image_name = "custom-rpi3.img"
        self.image_path = self.installDir


        self.create_image_file(name=self.image_name, size="8G", path=self.image_path)
        self.pre_chroot(path=self.image_path, name=self.image_name)
        self.base_config()
        self.common_config()
        
 
        #self.post_build(path=self.image_path, name=self.image_name)

    def common_config(self):

        self.chroot(path=self.image_path, 
                    cmd ="mkdir -p ~/Developer")

        r = sshpass("-p", self.ssh_pass, "rsync","-avz", "./fabric_common/templates/rpi3-arch", 'deploy@{}:~/Developer'.format(self.ssh_host)  )
        logi(title="envoie template",msg=r)

        self.bash.sudo("cp -r ~/Developer/rpi3-arch {}/mnt/home/deploy/Developer || /bin/true".format(self.image_path))

        self.chroot(path=self.image_path, 
                    cmd ="chmod +x ~/Developer/rpi3-arch/setup.sh")

        self.chroot(path=self.image_path, 
                    cmd ="~/Developer/rpi3-arch/setup.sh")



        #self.bash.sudo("cp /etc/resolv.conf {}/mnt/etc/resolv.conf || /bin/true".format(self.image_path))




    def base_config(self):
        self.chroot(path=self.image_path, 
                    cmd ="pacman-key --init")

        self.chroot(path=self.image_path, 
                    cmd ="pacman-key --populate archlinuxarm")

        self.chroot(path=self.image_path, 
                    cmd ="cat /etc/resolv.conf") # google ip

        self.chroot(path=self.image_path, 
                    cmd ="ping -c 5 -W 2 google.fr") # google ip

        self.chroot(path=self.image_path, 
                    cmd ="pacman -Suy --noconfirm --needed \
                          git base-devel go python python-pip \
                          sudo ca-certificates ca-certificates-utils \
                         ")




    def download_rootfilesystem(self):
        """
        a
        """
        self.bash.download(pattern = self.installDir,
                           dlink   = self.target['dlink'])


    def create_image(self, name, size):
        """
        a
        """
