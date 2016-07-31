__author__ = 'leonardoalbuquerque'

from Finder import Finder
from Youtube_dl_interface import Youtube_dl_interface
from Controller import database

database = database


class Main:
    def __init__(self, socketio):

        self.socketio = socketio

        # start the finder
        self.finder = Finder("AIzaSyA_UtBFJDfg9EsdczPFyE9wt7oIm3m1O8E")

        # start the youtube-dl api
        self.youtube_dl = Youtube_dl_interface(self.socketio)

        # start the database conection
        # database = Database()

        # finds new videos
        self.channels = database.get_channels_list()

        self.download_path = database.get_download_path()

    def start(self):

        print("started searching videos")

        # it is good to download failed videos first
        self.download_failed_videos()

        for channel in database.get_channels_list():  # self.channels:

            # search videos
            videos = self.finder.search(channel["id"], channel["unwanted_words"], channel['date'])

            if not videos:
                continue

            database.set_last_search_date()

            # this allow to save all videos before downloading so if
            # anything happens while downloading it can recover
            for video in videos:
                database.save_video(channel['pk'], video)

            # download each video
            for video in videos:
                self.download_video(video['id'])

            # sets the starting download date as the last video of the channel
            if videos:
                last_video = videos[0]

                database.change_channel_date(channel["name"], last_video["published_at"])

        videos = database.get_not_downloaded_videos()

        if len(videos) > 0:
            print "Videos that failed\n"

            for video in videos:
                print "%s\n" % (video['tittle'].encode('utf-8'))

        database.set_last_search_date()

        print("done")

    # donwload a video then set it as downloaded
    def download_video(self, video_id):

        if not database.video_was_downloaded(video_id):

            self.youtube_dl.download(video_id, database.get_download_path())
            print("Downloaded")
        else:
            print("Video " + video_id + " Already downloaded ")

        database.set_video_downloaded(video_id)

    # downloads all the videso that failed to download last time
    def download_failed_videos(self):

        videos = database.get_not_downloaded_videos()

        if len(videos) > 0:
            print "downloading videos that failed download"

        for video in videos:
            self.download_video(video['id'])