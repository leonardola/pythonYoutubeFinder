__author__ = 'leonardoalbuquerque'

'''import sqlite3'''


from pymongo import MongoClient

class Database:

    def __init__(self):

        client = MongoClient("127.0.0.1")

        database = client.youtubeDownloader

        self.channels = database.channels
        self.videos = database.videos
        self.configuration = database.configuration


    #channel

    def save_channel(self, name, date, id, unwanted_words):

        addedChannel = self.channels.insert({"name": name, "date": date,"id": id, "unwanted_words":unwanted_words})

        return addedChannel

    def get_channels_list(self):

        return self.channels.find()

    def delete_channel(self,channelName):

        self.channels.remove({'name':channelName})

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

            self.videos.insert(video)

            return False

        return True

    def set_video_downloaded(self,video_id):

        self.videos.update({"id":video_id},{"$set":{"downloaded":True}})

    # gets all not downloaded videos of a channel by its id or name,
    # if no channel is given than finds not downloaded videos from all channels
    def get_not_downloaded_videos(self,**kwargs):

        if len(kwargs) == 0:

            return self.videos.find({"downloaded":None})

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

        self.configuration.update({"name":"download_path"},{"download_path":path,"name":"download_path"},upsert=True)

    def get_download_path(self):

        download_path = self.configuration.find_one({"name":"download_path"})

        if download_path:
            return download_path['download_path']

        return False