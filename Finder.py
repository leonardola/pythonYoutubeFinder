#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.


class Finder:

    DEVELOPER_KEY = ""
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    def __init__(self,dev_key):
        self.DEVELOPER_KEY = dev_key
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        self.youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                        developerKey=self.DEVELOPER_KEY)

    def youtube_search(self,options):


        # Call the search.list method to retrieve results matching the specified
        # query term.
        if hasattr(options,"q"):

            search_response = self.youtube.search().list(
                q=options.q,
                part="id,snippet",
                channelId=options.channelId,
                order=options.order,
                publishedAfter=options.publishedAfter
            ).execute()
        else:
            search_response = self.youtube.search().list(
                part="id,snippet",
                channelId=options.channelId,
                order=options.order,
                publishedAfter=options.publishedAfter
            ).execute()


        videos = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append(
                    {
                        "id":search_result["id"]["videoId"],
                        "tittle":search_result["snippet"]["title"],
                        "published_at":search_result["snippet"]["publishedAt"]
                    }
                )

        return videos

    """search for given channel without the unwanted words"""
    def search(self,channelName,unwanted_words,starting_date):

        #adds a - to every unwanted word its a not logical operator for google
        if unwanted_words:
            unwanted_words = [" -" + s for s in unwanted_words]
            unwanted_words = ''.join(unwanted_words)

            argparser.add_argument("--q", help="Search term", default = "a|e|i|u " + unwanted_words)

        argparser.add_argument("--channelId", help="Channel id", default = channelName)
        #argparser.add_argument("--type", help="Video only", default = "video")
        argparser.add_argument("--part", help="Query columns", default="snippet")
        argparser.add_argument("--order", help="Order of download", default="date")
        argparser.add_argument("--publishedAfter", help="Day to start looking for", default=starting_date)
        args = argparser.parse_args()

        try:
            return self.youtube_search(args)
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


    def get_channel_id(self,channel_name):

        channel_name.replace(" ","%20")

        search_response = self.youtube.search().list(
            q=channel_name,
            part="snippet",
            type="channel"
        ).execute()

        channels = search_response.get("items", [])

        if len(channels) > 1:

            print("multiple channels were found choose one from: \n")

            for id,channel in enumerate(channels):
                print `id` + "> " + channel['snippet']['title'] + ": " + channel['snippet']['description'] + " \n"

            choosen_channel = raw_input("Type the number of the choosen one: ")

            return channels[int(choosen_channel)]['snippet']['channelId']

        if len(channels) == 1:

            return channels[0]['id']['channelId']

        print("No channel was found\n")

        return False