from fabric_common.common.build import Build
from ..core.device import Device
from pprint import pprint



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
        
 
        #self.post_build(path=self.image_path, name=self.image_name)


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
                    cmd ="pacman -Sy --noconfirm --needed \
                          git base-devel go python python-pip \
                          sudo ca-certificates ca-certificates-utils \
                         ")

        self.chroot(path=self.image_path, 
                    cmd ="mkdir -p ~/Developer")



                    



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
