__author__ = 'leonardoalbuquerque'

import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect('database',detect_types=sqlite3.PARSE_DECLTYPES)

        self.cursor = self.connection.cursor()

    def executeQuery(self,query):

        self.cursor.execute(query);

        return self.cursor.fetchall()


    def saveChannel(self, name, date):

        self.cursor.execute("INSERT INTO channel (name, last_download) values('%s','%s')"%(name,date))

        self.connection.commit()


    def getChannelsList(self):

        return self.executeQuery("Select * from channel")
