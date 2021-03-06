#!/bin/sh

echo "==> Setting python environment"

if [ -e venv/pyvenv.cfg ]
then
    echo "==> Install from requirements.txt python environment"
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -r odoo_src/requirements.txt
else # init
    echo "==> Init python environment"
    rm -rf venv
    python3.7 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt


    echo "==> Running patchs ..."
	chmod +x ./script/patchs/archlinux_install.sh
	./script/patchs/archlinux_install.sh
    
    pip install -r odoo_src/requirements.txt


    echo "==> Running v4l2.py patchs ..."
    cp ./script/patchs/v4l2.py.iotpatch ./venv/lib/python3.7/site-packages/
    cd ./venv/lib/python3.7/site-packages/
    patch v4l2.py < v4l2.py.iotpatch
    cd -
    #echo "==> Running http.py patchs ..."
    #cp ./script/patchs/http.py.iotpatch ./odoo_src/odoo
    #cd ./odoo_src/odoo
    #patch http.py < http.py.iotpatch
    

fi

