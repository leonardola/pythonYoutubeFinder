#!/usr/bin/env bash

read -p "Are you sure running as Root and inside the pythonYoutubeFinder folder? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then

    echo"updateing apt"
    apt-get update

    echo "installing crontab"
    apt-get install crontab

    echo "installing python"
    apt-get install python

    echo "installing python dev"
    apt-get install python-pip python-dev build-essential

    echo "updating pip"
    sudo pip install --upgrade pip

    echo "updating virtualenv"
    pip install --upgrade virtualenv

    echo "installing mongodb"
    apt-get install mongodb

    echo "changing permissions"
    chmod -R 777 ./

    SCRIPTPATH=$(pwd -P)
    PYTHONPATH=$(which python)

    echo "adding crontab entry"
    #write out current crontab
    crontab -l > mycron
    #echo new cron into cron file
    echo "@reboot" $PYTHONPATH $SCRIPTPATH"/webMain.py" > mycron
    #install new cron file
    crontab mycron
    rm mycron

fi
