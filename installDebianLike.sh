#!/usr/bin/env bash

read -p "Are you sure running as Root and inside the pythonYoutubeFinder folder? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then

    echo"updateing apt"
    apt-get update

    echo "installing crontab"
    apt-get -y install crontab

    echo "installing python"
    apt-get -y install python

    echo "installing python dev"
    apt-get -y install python-pip python-dev build-essential

    echo "updating pip"
    sudo pip install --upgrade pip

    echo "updating virtualenv"
    pip install --upgrade virtualenv

    echo "changing permissions"
    chmod -R 777 ./

    echo"installing pip packages"
    pip install requests
    pip install --upgrade google-api-python-client
    pip install youtube-dl
    pip install flask
    pip install apscheduler==2.1.2
    pip install flask-socketio
    pip install blitzdb
    pip install eventlet
    pip install gevent-websocket

    SCRIPTPATH=$(pwd -P)
    PYTHONPATH=$(which python)

    echo "add this line to crontab:"
    #echo new cron into cron file
    sudo echo "@reboot" $PYTHONPATH $SCRIPTPATH"/webMain.py"

fi
