__author__ = 'leonardoalbuquerque'

import requests
import json

class Channel:

    def __init__(self, channelName):

        self.channelName = channelName
        self.videoList = False

    def getChannelVideoList(self):

        if not self.videoList :

            response = requests.get("https://gdata.youtube.com/feeds/api/videos?author="+self.channelName+"&v=2&orderby=updated&alt=jsonc&max-results=5")

            content = json.loads(response.content)

            self.videoList = content['data']['items']

        return self.videoList