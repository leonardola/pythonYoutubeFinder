__author__ = 'leonardoalbuquerque'

'''import sqlite3'''


from pymongo import MongoClient

class Database:

    def __init__(self):

        client = MongoClient()

        database = client.youtubeDownloader

        self.channels = database.channels


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