__author__ = 'leonardoalbuquerque'

'''import sqlite3'''

import pymongo

from pymongo import MongoClient

class Database:

    def __init__(self):

        client = MongoClient()

        database = client.youtubeDownloader

        self.channels = database.channels


    def saveChannel(self, name, date):

        addedChannel = self.channels.insert({"name": name, "date": date})

        return addedChannel

    def getChannelsList(self):

        return self.channels.find();

    def deleteChannel(self,channelName):

        self.channels.remove({'name':channelName})