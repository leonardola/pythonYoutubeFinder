__author__ = 'leonardoalbuquerque'

from Finder import Finder
from Youtube_dl_interface import Youtube_dl_interface
from Database import Database

#start the finder
finder = Finder("AIzaSyA_UtBFJDfg9EsdczPFyE9wt7oIm3m1O8E")

#start the youtube-dl api
youtube_dl = Youtube_dl_interface()

#start the database conection
database = Database()

channels = database.get_channels_list()

for channel in channels:


    #search videos
    videos = finder.search(channel["id"],channel["unwanted_words"],channel['date'])

    for video in videos:

        if database.save_video(channel['_id'],video):
            youtube_dl.download(video["id"])
            database.set_video_downloaded(video['id'])

    if videos:
        last_video = videos[-1]

        database.change_channel_date(channel["name"],last_video["published_at"])