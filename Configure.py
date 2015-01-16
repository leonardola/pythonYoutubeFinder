__author__ = 'leonardoalbuquerque'

import Database

database = Database.Database()

stop = False

while not stop:

    channelName = raw_input("Type the name of a channel: ")

    dateToStartDownloading = raw_input("What is the first date to download from yyyy-mm-dd:")

    database.saveChannel(channelName, dateToStartDownloading)

    if(raw_input("Add another channel? y|n ") != "y"):

        stop = True

    channelsList = database.getChannelsList();

print("Listing all channels ")

for index in channelsList:

    print(index)


print("Good Bie and enjoy")