from __future__ import unicode_literals
import youtube_dl
from Database import Database

database = Database()

class Youtube_dl_interface:

    def __init__(self, socketio):
        self.socketio = socketio
        self.video_id = False
        self.ydl = False
        self.already_stoped = False

    def progress_hook(self, data):

        self.socketio.emit('download status changed', {'videoId':self.video_id, 'downloadData': data})

        if not self.already_stoped:
            self.already_stoped = True
            del self.ydl

        return

    def download(self, video_id, download_path):

        if not download_path:
            print("Download path was not given")

        self.video_id = video_id

        ydl_opts = {
            'outtmpl': download_path+'%(title)s-%(id)s.%(ext)s',
             'progress_hooks': [self.progress_hook]
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as self.ydl:
                self.ydl.download(['http://www.youtube.com/watch?v=' + video_id])
        except:
            return

        return