__author__ = 'leonardoalbuquerque'

from blitzdb import FileBackend, queryset
from Entity import Channel, Configuration, Video

import time

# new db
from CodernityDB.database import Database


class Database:
    def __init__(self):

        self.database = FileBackend("db")

        # self.channels = database.filter(Channel)
        # self.videos = database.filter()
        # self.configuration = database.configuration

    # name, date, id, unwanted_words
    def save_channel(self, data):

        data['date'] += "T19:00:00+00:00"

        addedChannel = self.database.save(Channel.Channel(data))
        self.database.commit()

        return addedChannel

    def get_channels_list(self):
        return self.database.filter(Channel.Channel, {})

    def delete_channel_by_name(self, channel_name):
        channel = self.database.filter(Channel.Channel, {'name': channel_name})
        channel.delete()
        self.database.commit()

    def delete_channel_by_id(self, channel_id):
        channel = self.database.filter(Channel.Channel, {'id': channel_id})
        channel.delete()
        self.database.commit()

    def add_channel_unwanted_word(self, channelName, unwanted_words):

        channel = self.channels.get(Channel.Channel, {"name": channelName})
        channel.unwanted_words.update(unwanted_words)
        self.database.commit()

    def get_channel_unwanted_words(self, channelName):

        channel = self.database.get(Channel.Channel, {"name": channelName})

        if not channel:
            print("Channel not found")
            return

        return channel.unwanted_words

    def remove_channel_unwanted_word(self, channel_name, unwanted_words):

        channel = self.database.get(Channel.Channel, {"name": channel_name})
        channel.unwanted_words = {k: v for k, v in channel.unwanted_words.iteritems() if v != unwanted_words}

        self.database.commit()

    def change_channel_date(self, channel_name, new_date):

        channel = self.database.get(Channel.Channel, {'name': channel_name})
        channel.date = new_date

    # videos
    def save_video(self, channel_id, video):

        video['channel_id'] = channel_id

        try:
            self.database.get(Video.Video, {"id": video['id']})
        except:
            video['add_date'] = self.get_current_date()
            self.database.save(Video.Video(video))

            self.database.commit()
            return False

        return True

    def set_video_downloaded(self, video_id):

        video = self.database.get(Video.Video, {"id": video_id})
        video.download_date = self.get_current_date()

        self.database.commit()
        # {"$set": {"downloaded": True, "download_date": self.get_current_date()}}

    def set_video_download_data(self, video_id, download_data):

        video = self.database.get(Video.Video, {"id": video_id})
        video.download_data = download_data

        self.database.commit()

        # {"$set": {"download_data": download_data}}

    # gets all not downloaded videos of a channel by its id or name,
    # if no channel is given than finds not downloaded videos from all channels
    def get_not_downloaded_videos(self, **kwargs):

        if len(kwargs) == 0:

            return self.database.filter(Video.Video, {"downloaded": None})

        elif "channel_name" in kwargs:

            channel = self.database.filter(Video.Video, {"name": kwargs['channel_name']})

            if not channel:
                return False

            channel_id = channel['pk']
        else:
            channel_id = kwargs['channel_id']

        return self.database.filter(Video.Video, {"channel_id": channel_id, "downloaded": None})

    def video_was_downloaded(self, video_id):

        try:
            self.database.get(Video.Video, {"id": video_id, "downloaded": True})
            return True
        except:
            return False

    # general config

    def set_download_path(self, path):

        downlod_path = self.get_download_path()

        if not downlod_path:
            self.database.save(Configuration.Configuration({'name': 'download_path', 'download_path': path}))
        else:
            downlod_path.download_path = path

        self.database.commit()

    def get_download_path(self):

        try:
            download_path = self.database.get(Configuration.Configuration, {'name': 'download_path'})
        except:
            return False

        if download_path:
            return download_path.download_path

        return False

    def get_last_downloaded_videos(self):

        channels = self.get_channels_list()

        videos = []

        for channel in channels:
            video = self.database.filter(Video.Video, {'channel_id': channel.pk}).sort('download_date', queryset.QuerySet.DESCENDING)

            if video:
                videos.append(video)

        return videos

    def get_current_date(self):
        return time.strftime("%d/%m/%Y-%H:%M:%S")

    def set_last_search_date(self):
        configuration = self.database.get(Configuration.Configuration, {"name": "last_search_date"})
        configuration.last_search_date = self.get_current_date()

        self.database.commit()
        #self.configuration.update({"name": "last_search_date"},
         #                         {"last_search_date": self.get_current_date(), "name": "last_search_date"},
          #                        upsert=True)

    def get_last_search_date(self):

        try:
            last_search_date = self.database.get(Configuration.Configuration, {"name": "last_search_date"})
        except:
            return "Never"

        return last_search_date['last_search_date']
