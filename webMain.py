__author__ = 'leonardoalbuquerque'

from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from flask.ext.socketio import send, emit


from Database import Database
from DownloadScheduler import DownloadScheduler
import thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
database = Database()

@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/downloading')
def downloading_page():

    downloading_videos = database.get_not_downloaded_videos()

    return render_template('downloading.html', videos = downloading_videos)

@app.route("/video/delete/<video_id>", methods=["POST"])
def delete_video(video_id):
    database.set_video_downloaded(video_id)
    return "ok"

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json)




if __name__ == '__main__':
    DownloadScheduler(socketio)
    app.debug = True
    socketio.run(app, use_reloader=True)