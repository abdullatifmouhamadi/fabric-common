# required

sudo pacman -S unzip postgresql python-lxml python-gevent
sudo pacman -S cups dbus ipp-usb python-gobject gobject-introspection bluez bluez-utils


systemctl start cups
systemctl start bluetooth
bluetoothctl power on

# controle du bluetooth

https://wiki.archlinux.org/index.php/Bluetooth

