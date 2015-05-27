__author__ = 'leonardoalbuquerque'

from Finder import Finder
from Youtube_dl_interface import Youtube_dl_interface
from Database import Database

#donwload a video then set it as downloaded
def download_video(videoId):

    if not database.video_was_downloaded(videoId):

        youtube_dl.download(videoId,database.get_download_path())

    print("downloaded")
    database.set_video_downloaded(videoId)

#downloads all the videso that failed to download last time
def download_failed_videos():

    videos = database.get_not_downloaded_videos()

    if videos.count() > 0:
        print "downloading videos that failed download"

    for video in videos:
        print video['tittle'] + "\n"
        download_video(video['id'])

#start the finder
finder = Finder("AIzaSyA_UtBFJDfg9EsdczPFyE9wt7oIm3m1O8E")

#start the youtube-dl api
youtube_dl = Youtube_dl_interface()

#start the database conection
database = Database()

#it is good to download failed videos first
download_failed_videos()

#finds new videos
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
        download_video(video['id'])

    #sets the starting download date as the last video of the channel
    if videos:
        last_video = videos[-1]

        database.change_channel_date(channel["name"],last_video["published_at"])


videos = database.get_not_downloaded_videos()
print "Not downloaded yet\n"

for video in videos:
    print "%s\n" % (video['tittle'])