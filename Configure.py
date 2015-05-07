__author__ = 'leonardoalbuquerque'

import Database
from Finder import Finder

database = Database.Database()
#should get this from db
finder = Finder("AIzaSyA_UtBFJDfg9EsdczPFyE9wt7oIm3m1O8E")

def delete_channel():
    channel_name = raw_input("Type the name of channel to delete: ")

    database.delete_channel(channel_name)

    print ("Channel deleted")


def add_channel():

    stop = False

    while not stop:

        #that aparently is a pythonic way of doing a do-while :(
        while True:

            channel_name = unicode(raw_input("Type the name of a channel: "), "utf-8")

            channel_id = finder.get_channel_id(channel_name)
            if channel_id:
                break

        #channel_id = raw_input("Type the id of the channel: ")

        #date must be rfc 3339 compliant
        dateToStartDownloading = raw_input("What is the first date to download from yyyy-mm-dd: ") + "T00:00:00Z"

        unwanted_words = []

        #unwanted words
        if(raw_input("Do you want to add some unwanted words? y|n ") == "y"):

            print("You can stop anytime by tiping stop")
            stop_unwanted = False

            while not stop_unwanted:
                input = raw_input("Type the unwanted word: ")
                if(input == "stop"):
                    stop_unwanted = True
                else:
                    unwanted_words.append(input)


        database.save_channel(channel_name, dateToStartDownloading, channel_id,unwanted_words)

        if(raw_input("Add another channel? y|n ") != "y"):

            stop = True


    list_channels()


def configure_path():

    print("To implement")

    return


def list_channels():

    print("Listing all channels ")

    for channel in database.get_channels_list():

        print(channel['name']+": " + channel["id"])

def list_channel_unwanted(channel_name = False):

    if channel_name:
        unwanted_words = database.get_channel_unwanted_words(channel_name)
    else:
        unwanted_words = database.get_channel_unwanted_words(raw_input("Type the channel name: "))

    for unwanted_word in unwanted_words:
        print(unwanted_word+"\n")

def show_menu():
    return raw_input("What do you want to configure?\n" +
              " add_channel: Adds new channels to the channels list \n" +
              " change_channel_date: Modifies a channel start downloading date\n" +
              " list_channels: List all channels \n" +
              " list_channel_unwanted: List all unwanted words of a channel\n"+
              " add_channel_unwanted: Add unwanted words to a channel\n"
              " remove_channel_unwanted: Remove unwanted words to a channel\n"
              " delete_channel: Deletes a  channel \n" +
              " set_download_path: Configures the path where things are downloaded \n" +
              " show_download_path: Shows the donwload path \n"+
              " exit: Exit the configuration \n" +
              " menu: Show this menu\n"+
              "> "
              )

def add_channel_unwanted():
    stop = False

    channel_name = raw_input("Type the channel name: ")

    print("To stop type stop at any time\n")

    unwanted_words = []

    while not stop:

        unwanted_word = raw_input("Type the unwanted word: ")

        if(unwanted_word != "stop"):
            unwanted_words.append(unwanted_word)
        else:
            database.add_channel_unwanted_word(channel_name,unwanted_words)
            stop = True

    print("All unwanted words were saved")

def remove_channel_unwanted():
    channel_name = raw_input("Type the channel name: ")

    if(raw_input("Do you want to list all unwanted words of this channel? y|n ") == "y" ):
        list_channel_unwanted(channel_name)

    print("To stop type stop at any time\n ")

    stop = False

    unwanted_words = []

    while not stop:
        unwanted_word = raw_input("Type the unwanted word: ")
        if(unwanted_word != "stop"):

            unwanted_words.append(unwanted_word)

        else:
            database.remove_channel_unwanted_word(channel_name,unwanted_words)
            stop = True

    print("Removed")


def set_download_path():

    download_path = raw_input("Type the absolute path to download the files: ")

    if not download_path.endswith("/"):
        download_path += "/"

    database.set_download_path(download_path)

def get_download_path():
    print(database.get_download_path())


def change_channel_date():
    channel_name = raw_input("Type the channel name: ")
    new_date = raw_input("Type the new date to start downloading yyyy-mm-dd: ") + "T00:00:00Z"

    database.change_channel_date(channel_name,new_date)


actions = {
    'list_channels': list_channels,
    'change_channel_date': change_channel_date,
    'list_channel_unwanted': list_channel_unwanted,
    'add_channel_unwanted': add_channel_unwanted,
    'remove_channel_unwanted':remove_channel_unwanted,
    'set_download_path': set_download_path,
    'show_download_path':get_download_path,
    'add_channel': add_channel,
    'delete_channel': delete_channel,
    'menu':show_menu,
    'exit': quit
}

test = database.get_download_path()

if not test:

    set_download_path()


whatToDo = show_menu()



while True:
    if whatToDo in actions:
        actions[whatToDo]()
    else:
        print "Action not recognized"

    whatToDo = raw_input("> ")