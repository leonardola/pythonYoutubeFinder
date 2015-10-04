from __future__ import unicode_literals
import youtube_dl
from Database import Database

database = Database()

class Youtube_dl_interface:

    def __init__(self, socketio):
        self.socketio = socketio
        self.video_id = False

    def progress_hook(self, data):

        database.set_video_download_data(self.video_id, data)
        self.socketio.emit('download status changed', {'videoId':self.video_id, 'downloadData': data})

        return

    def download(self, video_id, download_path):

        if not download_path:
            print("Download path was not given")

        self.video_id = video_id

        ydl_opts = {
            'outtmpl': download_path+'%(title)s-%(id)s.%(ext)s',
             'progress_hooks': [self.progress_hook]
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['http://www.youtube.com/watch?v=' + video_id])

        return