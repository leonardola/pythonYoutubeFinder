__author__ = 'leonardoalbuquerque'

from blitzdb import FileBackend
from Entity import Channel, Configuration

import time

#new db
from CodernityDB.database import Database

class Database:

    def __init__(self):

        self.database = FileBackend("db")

        # self.channels = database.filter(Channel)
        # self.videos = database.filter()
        # self.configuration = database.configuration


    #name, date, id, unwanted_words
    def save_channel(self, data):

        data['date'] += "T19:00:00+00:00"

        addedChannel = self.database.save(Channel, Channel(data))

        return addedChannel

    def get_channels_list(self):
        return self.channels.find()

    def delete_channel_by_name(self, channel_name):
        self.channels.remove({'name':channel_name})

    def delete_channel_by_id(self, channel_id):
        self.channels.remove({'id':channel_id})


    def add_channel_unwanted_word(self,channelName,unwanted_words):

        channel = self.channels.update({"name": channelName},{"$push":{"unwanted_words":{"$each":unwanted_words}}})

    def get_channel_unwanted_words(self,channelName):

        channel = self.channels.find_one({"name":channelName})

        if not channel:
            print("Channel not found")
            return

        return channel['unwanted_words']


    def remove_channel_unwanted_word(self,channel_name,unwanted_words):

        self.channels.update({"name":channel_name},{"$pull":{"unwanted_words":{"$in":unwanted_words}}})

    def change_channel_date(self,channel_name,new_date):

        self.channels.update(
            {"name":channel_name},#finds the channel
            {"$set":{"date":new_date}}#update the date
        )



    #videos
    def save_video(self,channel_id, video):

        video['channel_id'] = channel_id

        if not self.videos.find_one({"id":video['id']}):
            video['add_date'] = self.get_current_date()
            self.videos.insert(video)

            return False

        return True

    def set_video_downloaded(self, video_id):

        self.videos.update(
            {"id":video_id},
            {"$set":{"downloaded":True, "download_date": self.get_current_date()}}
        )

    def set_video_download_data(self, video_id, download_data):
        self.videos.update(
            {"id": video_id},
            {"$set":{"download_data": download_data}}
        )

    # gets all not downloaded videos of a channel by its id or name,
    # if no channel is given than finds not downloaded videos from all channels
    def get_not_downloaded_videos(self,**kwargs):

        if len(kwargs) == 0:

            return self.videos.find({"downloaded":None}).sort([
                ("add_date", -1)
            ])

        elif "channel_name" in kwargs:

            channel = self.channels.find_one({"name":kwargs['channel_name']})

            if not channel:
                return False

            channel_id = channel['_id']
        else:
            channel_id = kwargs['channel_id']

        return self.videos.find({"channel_id":channel_id,"downloaded":None})

    def video_was_downloaded(self,video_id):

        if self.videos.find_one({"id":video_id,"downloaded":True}):
            return True

        return False

    # general config

    def set_download_path(self,path):

        downlod_path = self.get_download_path()

        if not downlod_path:
            self.database.save(Configuration.Configuration({'name': 'download_path', 'download_path':path}))
        else:
            downlod_path.download_path = path

        self.database.commit()

    def get_download_path(self):

        download_path = self.database.get(Configuration.Configuration, {'name': 'download_path'})

        if download_path:
            return download_path.download_path

        return False

    def get_last_downloaded_videos(self):

        channels = self.get_channels_list()

        videos = []

        for channel in channels:
            video = self.videos.find_one({"channel_id": channel['_id'], "downloaded": True}, sort=[("download_date", pymongo.DESCENDING)])

            if video:
                videos.append(video)

        return videos

    def get_current_date(self):
        return time.strftime("%d/%m/%Y-%H:%M:%S")

    def set_last_search_date(self):
        self.configuration.update({"name":"last_search_date"},{"last_search_date":self.get_current_date(),"name":"last_search_date"},upsert=True)

    def get_last_search_date(self):

        last_search_date = self.configuration.find_one({"name":"last_search_date"})

        return last_search_date['last_search_date']