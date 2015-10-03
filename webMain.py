__author__ = 'leonardoalbuquerque'

from flask import Flask, jsonify
app = Flask(__name__)
from flask import render_template
from Database import Database

from bson import Binary, Code
from bson.json_util import dumps

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

    return jsonify(data=data)

if __name__ == "__main__":
    app.run(debug=True)
