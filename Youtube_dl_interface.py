from __future__ import unicode_literals
import youtube_dl


class Youtube_dl_interface:

    def download(self,video_id):

        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['http://www.youtube.com/watch?v=' + video_id])

        return
