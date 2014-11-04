__author__ = 'leonardoalbuquerque'

import sqlite3


class Database:

    def __init__(self):

        self.connection = sqlite3.connect('database')

        self.cursor = self.connection.cursor()

    def executeQuery(self,query):

        self.cursor.execute(query);

        retorno = self.cursor.fetchmany()

        return retorno

    def saveChannel(self, name, date):

        query = "INSERT INTO channel (name, last_download) values('%s','%s')"%(name,date)

        self.cursor.execute(query)
        self.connection.commit()


