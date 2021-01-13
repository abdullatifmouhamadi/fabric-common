# required

sudo pacman -S unzip postgresql python-lxml python-gevent libsass
sudo pacman -S cups dbus ipp-usb python-gobject gobject-introspection bluez bluez-utils


systemctl start cups
systemctl start bluetooth
bluetoothctl power on

# controle du bluetooth

https://wiki.archlinux.org/index.php/Bluetooth



# defaults

useradd -m -g users -s /bin/bash pi




groupadd usbusers
usermod -a -G usbusers pi
usermod -a -G lp pi # cups


sudo -u postgres createuser -s deploy

yay -S raspberrypi-userland-aarch64-git xf86-video-fbturbo-git
yay -S xorg-xhost