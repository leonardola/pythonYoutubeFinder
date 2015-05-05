from __future__ import unicode_literals
import youtube_dl


class Youtube_dl_interface:

    def download(self,video_id,download_path):

        if not download_path:
            print("Download path was not given")

        ydl_opts = {
            'outtmpl': download_path+'%(title)s-%(id)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['http://www.youtube.com/watch?v=' + video_id])

        return
