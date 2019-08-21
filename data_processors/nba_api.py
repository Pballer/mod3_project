"""Module that will load all NBA api requests."""

import requests
import pandas as pd
from enum import Enum
from time import sleep


class NBARequestTypes(Enum):
    PLAYERS = 'players'
    TEAMS = 'teams'
    STATS = 'stats'
    GAMES = 'games'


class NBARequests(object):

    def __init__(self, api_key):

        self.base_url = "https://free-nba.p.rapidapi.com/{}"


        self.headers = {
            'x-rapidapi-host': "free-nba.p.rapidapi.com",
            'x-rapidapi-key': api_key
        }

    def get_all_data(self, data_type, start_page=0, params={}) -> pd.DataFrame:
        """Load all data from NBA api for given data type."""
        data_url = self.base_url.format(data_type)
        next_page = start_page

        data = []
        while next_page is not None:
            if next_page != 0 and next_page % 50 == 0:
                print('Sleep for 30 seconds...')
                sleep(30)

            querystring = {"page": next_page, "per_page": "100"}
            querystring.update(params)
            print(querystring)
            response = requests.request("GET",
                                        data_url,
                                        headers=self.headers,
                                        params=querystring)
            json = response.json()

            data.extend(json['data'])
            next_page = json['meta']['next_page']

        data_df = pd.DataFrame.from_dict(data)

        return data_df
