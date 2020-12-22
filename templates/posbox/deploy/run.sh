#!/bin/bash

NAME="Odoo PosBoxLess"

echo "Starting $NAME as `whoami`"

#../venv/bin/python3.6 ../odoo_src/odoo-bin -c ./odoo.conf -p MYPORT --addons-path=../custom-addons/,../odoo_src/addons/

../venv/bin/python3.6 ../odoo_src/odoo-bin --load=web,hw_proxy,hw_posbox_homepage,hw_scale,hw_scanner,hw_escpos

#/home/pi/odoo/odoo.py --load=web,hw_proxy,hw_posbox_homepage,hw_posbox_upgrade,hw_scale,hw_scanner,hw_escpos


