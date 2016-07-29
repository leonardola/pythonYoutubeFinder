from flask import Flask, request
from flask.ext.socketio import SocketIO


app = Flask(__name__)

from Database import Database
from Finder import Finder


finder = Finder("AIzaSyA_UtBFJDfg9EsdczPFyE9wt7oIm3m1O8E")


app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

database = Database()

def getRequestData():
    imutableData = request.form
    return {k:v for k,v in imutableData.items()}

from Controller import ChannelsController
from Controller import DefaultController
from Controller import DownloadController