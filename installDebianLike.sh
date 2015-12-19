#!/usr/bin/env bash

read -p "Are you sure running as Root and inside the pythonYoutubeFinder folder? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
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
fi
