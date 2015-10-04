__author__ = 'leonardoalbuquerque'

from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from flask.ext.socketio import send, emit

from flask import jsonify

from Database import Database
from Main import Main
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

@app.route('/videos/')
def getVideos():
    #there is also a loads function
    videos = database.get_not_downloaded_videos()

    data = []

    for video in videos:
        data.append({
            'id':video['id'],
            'tittle': video['tittle'],
            'downloadData': video['download_data'] if 'download_data' in video else  False
        })
    print("asdf")
    socketio.emit('my event', {'data': 42})

    return jsonify(data=data)


@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json)

if __name__ == '__main__':
    main = Main(socketio)
    thread.start_new_thread(main.start, ())

    app.debug = True
    socketio.run(app, use_reloader=True)