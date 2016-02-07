#! /bin/bash
if [ ! -n "$1" ]; then
    echo "Syntax: simpleapp_deploy branch_name"
    echo "Use \"master\" for default"
    exit 1
fi

service simpleapp_panel stop
sleep 1

if [ -f "/opt/orange/env/bin/pip" ]; then
    /opt/orange/env/bin/pip uninstall simpleapp -y
fi


mkdir -p /opt/orange/
chmod 777 -R /usr/local/orange/simpleapp/log/

rm -rf /opt/orange/simpleapp
git clone https://pprolancer@bitbucket.org/pprolancer/simpleapp.git -b $1 /opt/orange/simpleapp

virtualenv /opt/orange/env
cd /opt/orange/simpleapp
../env/bin/python setup.py install

echo "+++ Running web server..."
service nginx restart
service simpleapp_panel start

echo
echo "Finished!"
