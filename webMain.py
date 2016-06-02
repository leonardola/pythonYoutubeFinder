__author__ = 'leonardoalbuquerque'

from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from flask.ext.socketio import emit
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
def home():

    return render_template('home.html.jinja2', download_path = database.get_download_path())

@app.route('/downloading')
def downloading_page():

    downloading_videos = database.get_not_downloaded_videos()

    #database.get_last_downloaded_videos()

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
def get_channel_data_by_name(channel_name):
    data = finder.get_channels_with_name(channel_name)

    return jsonify(data=data)


@app.route("/getChannelData/<channel_id>")
def get_channel_data(channel_id):
    finder.get_channel_data(channel_id)

    return "ok"

@app.route("/channel/add", methods=["GET","POST"])
def add_channel():
    data = request.json
    database.save_channel(data)
    return "ok"

@app.route("/channel/remove/<channel_id>")
def remove_channel(channel_id):
    database.delete_channel_by_id(channel_id)
    return "ok"


@socketio.on('my event')
def handle_my_custom_event(json):
    print "connect with socketio"
    emit('my response', json)


def getRequestData():
    imutableData = request.form
    return {k:v for k,v in imutableData.items()}

@app.route('/shutdown')
def shutdown():
    socketio.stop()
    return 'Server shutting down...'

@app.route('/updateDownloadPath', methods = ["POST"])
def update_download_path():
    data = getRequestData()

    database.set_download_path(data['newDownloadPath'])
    return "ok"

@app.route('/search')
def search_videos():
    downloadScheduler.execute_now()

    return "ok"

if __name__ == '__main__':
    downloadScheduler = DownloadScheduler(socketio)
    #app.debug = True
    socketio.run(app, use_reloader=True, host='0.0.0.0')