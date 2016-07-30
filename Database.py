__author__ = 'leonardoalbuquerque'

from blitzdb import FileBackend, queryset
from Entity import Channel, Configuration, Video

import time

class Database:

    def __init__(self):
        self.database = FileBackend("db")
        self.database.autocommit = True

        return

    # name, date, id, unwanted_words
    def save_channel(self, data):

        data['date'] += "T19:00:00+00:00"

        addedChannel = self.database.save(Channel.Channel(data))

        return addedChannel

    def get_channels_list(self):
        return self.database.filter(Channel.Channel, {})

    def delete_channel_by_name(self, channel_name):
        channel = self.database.filter(Channel.Channel, {'name': channel_name})
        channel.delete()

    def delete_channel_by_id(self, channel_id):
        channel = self.database.filter(Channel.Channel, {'id': channel_id})
        channel.delete()

    def add_channel_unwanted_word(self, channelName, unwanted_words):

        channel = self.channels.get(Channel.Channel, {"name": channelName})
        channel.unwanted_words.update(unwanted_words)
        channel.save()

    def get_channel_unwanted_words(self, channelName):

        channel = self.database.get(Channel.Channel, {"name": channelName})

        if not channel:
            print("Channel not found")
            return

        return channel.unwanted_words

    def remove_channel_unwanted_word(self, channel_name, unwanted_words):

        channel = self.database.get(Channel.Channel, {"name": channel_name})
        channel.unwanted_words = {k: v for k, v in channel.unwanted_words.iteritems() if v != unwanted_words}
        channel.save()

    def change_channel_date(self, channel_name, new_date):

        channel = self.database.get(Channel.Channel, {'name': channel_name})
        channel.date = new_date
        channel.save()







    # videos
    def save_video(self, channel_id, video):

        video['channel_id'] = channel_id
        video['downloaded'] = False

        try:
            self.database.get(Video.Video, {"id": video['id']})
        except:
            video['add_date'] = self.get_current_date()
            self.database.save(Video.Video(video))

            return False

        return True

    def set_video_downloaded(self, video_id):

        video = self.database.get(Video.Video, {"id": video_id})
        video.download_date = self.get_current_date()
        video.downloaded = 'True'
        video.save()

    def set_video_download_data(self, video_id, download_data):

        video = self.database.get(Video.Video, {"id": video_id})
        video.download_data = download_data
        video.save()

    # gets all not downloaded videos of a channel by its id or name,
    # if no channel is given than finds not downloaded videos from all channels
    def get_not_downloaded_videos(self, **kwargs):

        if len(kwargs) == 0:

            return self.database.filter(Video.Video, {"downloaded": False}).sort('download_date', queryset.QuerySet.ASCENDING)

        elif "channel_name" in kwargs:

            channel = self.database.filter(Video.Video, {"name": kwargs['channel_name']}).sort('download_date', queryset.QuerySet.ASCENDING)

            if not channel:
                return False

            channel_id = channel['pk']
        else:
            channel_id = kwargs['channel_id']

        return self.database.filter(Video.Video, {"channel_id": channel_id, "downloaded": False}).sort('download_date', queryset.QuerySet.ASCENDING)

    def video_was_downloaded(self, video_id):

        try:
            self.database.get(Video.Video, {"id": video_id, "downloaded": True})
            return True
        except:
            return False








    # general config

    def set_download_path(self, path):

        try:
            download_path = self.database.get(Configuration.Configuration, {'name': 'download_path'})
            download_path.download_path = path
            download_path.save()
        except:
            self.database.save(Configuration.Configuration({'name': 'download_path', 'download_path': path}))

    def get_download_path(self):

        try:
            download_path = self.database.get(Configuration.Configuration, {'name': 'download_path'})
        except Configuration.Configuration.DoesNotExist as err:
            return False

        if download_path:
            return download_path['download_path']

        return False

    def get_last_downloaded_videos(self):

        channels = self.get_channels_list()

        videos = []

        for channel in channels:
            videoFromDb = self.database.filter(Video.Video, {'channel_id': channel.pk}).sort('download_date', queryset.QuerySet.DESCENDING)

            if videoFromDb:
                videos.append(videoFromDb.next())

        return videos








    def get_current_date(self):
        return time.strftime("%d/%m/%Y-%H:%M:%S")

    def set_last_search_date(self):

        try:
            configuration = self.database.get(Configuration.Configuration, {"name": "last_search_date"})
        except:
            configuration = self.database.save(Configuration.Configuration({'name': "last_search_date", "last_search_date": self.get_current_date()}))

        configuration.last_search_date = self.get_current_date()
        configuration.save()

    def get_last_search_date(self):

        try:
            last_search_date = self.database.get(Configuration.Configuration, {"name": "last_search_date"})
        except:
            return "Never"

        return last_search_date['last_search_date']
