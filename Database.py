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

        return self.channels.find();

    def delete_channel(self,channelName):

        self.channels.remove({'name':channelName})

    def add_channel_unwanted_word(self,channelName,unwanted_words):

        channel = self.channels.update({"name": channelName},{"$push":{"unwanted_words":{"$each":unwanted_words}}})

        #channel.unwanted_list.insert(unwanted_words)

    def get_channel_unwantedWords(self,channelName):

        return self.channels.findOne({"name":channelName}).unwanted_words

    def remove_channel_unwanted_word(self,channelName,unwanted_word):

        self.channels.findOne({"name":channelName}).findOne({"unwanted_words":unwanted_word}).remove