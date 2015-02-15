__author__ = 'leonardoalbuquerque'

import Database

database = Database.Database()


def delete_channel():
    channel_name = raw_input("Type the name of channel to delete")

    database.deleteChannel(channel_name)


def add_channel():

    stop = False

    '''while not stop:

        channelName = raw_input("Type the name of a channel: ")

        dateToStartDownloading = raw_input("What is the first date to download from yyyy-mm-dd:")

        database.saveChannel(channelName, dateToStartDownloading)

        if(raw_input("Add another channel? y|n ") != "y"):

            stop = True

        '''
    list_channels()


def configure_path():

    return


def list_channels():

    print("Listing all channels ")

    for channel in database.getChannelsList():

        print(channel[u'name'])


actions = {
    'list_channels': list_channels,
    'configure_path': configure_path,
    'add_channel': add_channel,
    'delete_channel': delete_channel,
    'exit': quit
}


whatToDo = raw_input("What do you want to configure?\n" +
                    " add_channel: Adds new channels to the channels list \n" +
                    " modify_channel: Modifies a channel \n" +
                    " list_channels: List all channels \n" +
                    " delete_channel: Deletes a  channel \n" +
                    " configure_path: Configures the path where things are downloaded \n" +
                    " exit: Exit the configuration \n" +
                    "> "
                    )


while True:
    if whatToDo in actions:
        actions[whatToDo]()
    else:
        print "Not recognized"

    whatToDo = raw_input("> ")




