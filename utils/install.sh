#! /bin/bash

BRANCH=master

if [ -n "$1" ]; then
    BRANCH=$1
fi

# install required softwares
apt-get install nginx -y
apt-get install python-dev -y
apt-get install libevent-dev python-all-dev -y
apt-get install libffi-dev -y
apt-get install python-pip -y
apt-get install git -y
pip install virtualenv

# setup codes
pip uninstall simpleapp -y

mkdir -p /opt/orange/
mkdir -p /usr/local/orange/simpleapp/log/
chmod 777 -R /usr/local/orange/simpleapp/log/

rm -rf /opt/orange/simpleapp
git clone https://pprolancer@bitbucket.org/pprolancer/simpleapp.git -b $BRANCH /opt/orange/simpleapp

cp -a /opt/orange/simpleapp/utils/deploy.sh /usr/local/bin/simpleapp_deploy
cp /opt/orange/simpleapp/utils/simpleapp_nginx.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/simpleapp_nginx.conf /etc/nginx/sites-enabled/simpleapp_nginx.conf
cp /opt/orange/simpleapp/utils/uwsgi/simpleapp_panel.conf /etc/init/

virtualenv /opt/orange/env
cd /opt/orange/simpleapp
../env/bin/python setup.py install

# restart services
echo "Restarting Server..."
service nginx restart
service simpleapp_panel restart

echo
echo "Finished!"
