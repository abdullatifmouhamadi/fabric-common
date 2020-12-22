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
    python3.6 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt


    echo "==> Running patchs ..."
	chmod +x ./script/patchs/archlinux_install.sh
	./script/patchs/archlinux_install.sh

    pip install -r odoo_src/requirements.txt
fi

