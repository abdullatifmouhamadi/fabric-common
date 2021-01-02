#!/bin/bash

NAME="Odoo PosBoxLess"

echo "Starting $NAME as `whoami`"

#../venv/bin/python3.7 ../odoo_src/odoo-bin -c ./odoo.conf -p MYPORT --addons-path=../custom-addons/,../odoo_src/addons/

../venv/bin/python3.7 ../odoo_src/odoo-bin --load=web,hw_drivers,hw_proxy,hw_posbox_homepage,hw_escpos --addons-path=../odoo_src/addons/

#/home/pi/odoo/odoo.py --load=web,hw_proxy,hw_posbox_homepage,hw_posbox_upgrade,hw_scale,hw_scanner,hw_escpos


