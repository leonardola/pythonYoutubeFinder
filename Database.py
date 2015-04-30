__author__ = 'leonardoalbuquerque'

'''import sqlite3'''


from pymongo import MongoClient

class Database:

    def __init__(self):

        client = MongoClient()

        database = client.youtubeDownloader

        self.channels = database.channels
        self.videos = database.videos


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

    #pass the channel_name or channel_id
    def get_channel_not_downloaded_videos(self,**kwargs):

        if len(kwargs) == 0:

            self.videos.find({"downloaded":None})

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