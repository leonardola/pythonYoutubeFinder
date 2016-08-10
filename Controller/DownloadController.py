from flask_socketio import emit
from flask import render_template
from Controller import socketio, app, database
from DownloadScheduler import DownloadScheduler

downloadScheduler = DownloadScheduler(socketio)

@app.route('/downloading')
def downloading_page():

    downloading_videos = database.get_not_downloaded_videos()
    downloaded_videos = database.get_last_downloaded_videos()
    last_search_date = database.get_last_search_date()

    return render_template('downloading.html.jinja2',
                           videos = downloading_videos,
                           downloaded_videos = downloaded_videos,
                           last_search_date = last_search_date)

@app.route("/video/delete/<video_id>", methods=["POST"])
def delete_video(video_id):
    database.set_video_downloaded(video_id)
    return "ok"

@app.route('/search')
def search_videos():
    print "started to search videos"
    downloadScheduler.execute_now()
    return 'ok'

@app.route('/shutdown')
def shutdown():
    socketio.stop()
    return 'Server shutting down...'

@socketio.on('my event')
def handle_my_custom_event(json):
    print "connect with socketio"
    emit('my response', json)
