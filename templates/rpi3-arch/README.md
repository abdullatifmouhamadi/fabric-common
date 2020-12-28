


# umount

```
rm ./mnt/etc/resolv.conf
mv ./mnt/etc/resolv.conf.bak ./mnt/etc/resolv.conf
rm ./mnt/usr/bin/qemu-arm-static

umount -l ./mnt/dev
umount -l ./mnt/proc
umount -l ./mnt/sys
umount -l ./mnt/boot
umount -l ./mnt


```



# installation
sudo pacman -S --needed xorg
sudo pacman -S --needed lxqt xdg-utils ttf-freefont sddm
sudo pacman -S --needed libpulse libstatgrab libsysstat lm_sensors network-manager-applet oxygen-icons pavucontrol-qt
sudo pacman -S --needed firefox vlc filezilla leafpad xscreensaver archlinux-wallpaper

# deamon
systemctl enable sddm
systemctl enable NetworkManager


# config
nmcli device wifi connect SSID_or_BSSID password password

# configure langue






# image creation

https://disconnected.systems/blog/raspberry-pi-archlinuxarm-setup/

# desktop
https://www.debugpoint.com/2020/12/lxqt-arch-linux-install/
https://www.zybuluo.com/yangxuan/note/344907

# gpu

xf86-video-fbdev




# pour chromium 
yay -S icu67