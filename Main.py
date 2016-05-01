__author__ = 'leonardoalbuquerque'

from Finder import Finder
from Youtube_dl_interface import Youtube_dl_interface
from Database import Database

class Main:

    def __init__(self, socketio):

        self.socketio = socketio
        socketio.emit('my event', {'data': 42})

        #start the finder
        self.finder = Finder("AIzaSyA_UtBFJDfg9EsdczPFyE9wt7oIm3m1O8E")

        #start the youtube-dl api
        self.youtube_dl = Youtube_dl_interface(self.socketio)

        #start the database conection
        self.database = Database()

        #finds new videos
        self.channels = self.database.get_channels_list()

        self.download_path = self.database.get_download_path()

    def start(self):

        #it is good to download failed videos first
        self.download_failed_videos()

        for channel in self.channels:

            #search videos
            videos = self.finder.search(channel["id"],channel["unwanted_words"],channel['date'])

            #this allow to save all videos before downloading so if
            #anything happens while downloading it can recover
            for video in videos:
                self.database.save_video(channel['_id'],video)

            #download each video
            for video in videos:
                self.download_video(video['id'])

            #sets the starting download date as the last video of the channel
            if videos:
                last_video = videos[-1]

                self.database.change_channel_date(channel["name"],last_video["published_at"])


        videos = self.database.get_not_downloaded_videos()

        if videos.count() > 0:
            print "Videos that failed\n"

            for video in videos:
                print "%s\n" % (video['tittle'])

    #donwload a video then set it as downloaded
    def download_video(self,video_id):

        if not self.database.video_was_downloaded(video_id):

            self.youtube_dl.download(video_id,self.database.get_download_path())
            print("Downloaded")
        else:
            print("Already downloaded")

        self.database.set_video_downloaded(video_id)

    #downloads all the videso that failed to download last time
    def download_failed_videos(self):

        videos = self.database.get_not_downloaded_videos()

        if videos.count() > 0:
            print "downloading videos that failed download"

        for video in videos:
            #print video['tittle'] + "\n"
            self.download_video(video['id'])

