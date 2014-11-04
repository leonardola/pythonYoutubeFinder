__author__ = 'leonardoalbuquerque'

import Database

database = Database.Database()

channelName = input("Type the name of a channel: ")


database.saveChannel(channelName, "2010-01-05")