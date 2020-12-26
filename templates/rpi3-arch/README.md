


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


losetup --detach loop0

```