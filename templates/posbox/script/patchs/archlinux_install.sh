

################################################################################### compiler version
sed -i 's/psycopg2==2.7.7;/psycopg2==2.8.3;/g' odoo_src/requirements.txt
sed -i 's/gevent/#gevent/g' odoo_src/requirements.txt
sed -i 's/libsass/#libsass/g' odoo_src/requirements.txt
sed -i 's/lxml/#lxml/g' odoo_src/requirements.txt

