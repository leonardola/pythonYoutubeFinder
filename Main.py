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

download_path = database.get_download_path()

for channel in channels:

    #search videos
    videos = finder.search(channel["id"],channel["unwanted_words"],channel['date'])

    #this allow to save all videos before downloading so if
    #anything happens while downloading it can recover
    for video in videos:
        database.save_video(channel['_id'],video)

    #download each video
    for video in videos:

        if not database.video_was_downloaded(video['id']):

            youtube_dl.download(video["id"],database.get_download_path())
            print("downloaded")
            database.set_video_downloaded(video['id'])

    #sets the starting download date as the last video of the channel
    if videos:
        last_video = videos[-1]

        database.change_channel_date(channel["name"],last_video["published_at"])

    videos = database.get_channel_not_downloaded_videos(channel_name = channel['name'])

    print "Not downloaded yet\n"

    for video in videos:
        print "%s\n" % (video['tittle'])