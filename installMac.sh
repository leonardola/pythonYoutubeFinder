#!/usr/bin/env bash
brew install python

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