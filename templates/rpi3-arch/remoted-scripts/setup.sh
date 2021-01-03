#!/bin/bash

NAME="Installation"

echo "=> Starting $NAME as `whoami`"




#cd /home/deploy/Developer
#rm -rf yay
#git clone https://aur.archlinux.org/yay.git
#cd yay
#makepkg -s



echo "=> Création du compte 'deploy'"
useradd -m -g users -G wheel -s /bin/bash deploy
echo deploy:Houda2016 | chpasswd



echo "=> Configuration du 'localtime'"
ln -sf /usr/share/zoneinfo/Europe/Paris /etc/localtime


echo "=> Générer les traductions"
locale-gen
localectl set-x11-keymap fr

echo "=> Activation des services"

#systemctl enable NetworkManager
#systemctl enable sddm
#systemctl enable sshd
#systemctl enable cups

echo "=> Dangers"

sed --in-place 's/^#\s*\(%wheel\s\+ALL=(ALL)\s\+ALL\)/\1/' /etc/sudoers


