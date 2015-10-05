__author__ = 'leonardoalbuquerque'

from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from flask.ext.socketio import send, emit
from flask import jsonify
from flask import request

from Database import Database
from DownloadScheduler import DownloadScheduler
from Finder import Finder
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
database = Database()
finder = Finder("AIzaSyA_UtBFJDfg9EsdczPFyE9wt7oIm3m1O8E")

@app.route('/')
def hello():
    return render_template('home.html.jinja2')


@app.route('/downloading')
def downloading_page():

    downloading_videos = database.get_not_downloaded_videos()

    return render_template('downloading.html.jinja2', videos = downloading_videos)

@app.route("/video/delete/<video_id>", methods=["POST"])
def delete_video(video_id):
    database.set_video_downloaded(video_id)
    return "ok"

@app.route("/channels")
def channels_page():
    channels = database.get_channels_list()
    return render_template("channels.html.jinja2", channels=channels)


@app.route("/channels/getDataByName/<channel_name>")
def getChannelDataByName(channel_name):
    data = finder.get_channels_with_name(channel_name)

    return jsonify(data=data)


@app.route("/getChannelData/<channel_id>")
def getChannelData(channel_id):
    finder.get_channel_data(channel_id)

    return "ok"

@app.route("/channel/add", methods=["GET","POST"])
def addChannel():
    requerst_type = request.headers.get('content-type')
    data = request.json#getRequestData()
    database.save_channel(data)
    return "ok"



@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json)


def getRequestData():
    imutableData = request.form
    return {k:v for k,v in imutableData.items()}

if __name__ == '__main__':
    #DownloadScheduler(socketio)
    app.debug = True
    socketio.run(app, use_reloader=True)