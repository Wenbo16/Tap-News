import requests
import os
import sys
import json
from json import loads

with open('/home/wenbo/Desktop/Tap-News/config/config.json') as config_file:
    config = json.load(config_file)

NEWS_API_KEY = config['common']['news_api_client']['NEWS_API_KEY']
NEWS_API_ENDPOINT = config['common']['news_api_client']['NEWS_API_ENDPOINT']
ARTICALS_API = config['common']['news_api_client']['ARTICALS_API']

BCC = 'bbc'
CNN = 'cnn'
DEFAULT_SOURCES = [CNN]

SORT_BY_TOP = config['common']['news_api_client']['SORT_BY_TOP']

# flexibility
def buildUrl(end_point=NEWS_API_ENDPOINT, api_name=ARTICALS_API):
    return end_point + api_name


def getNewsFromSource(sources=[DEFAULT_SOURCES], sortBy=SORT_BY_TOP):
    articles = []
    for source in sources:
        payload = {'apiKey': NEWS_API_KEY,
                   'source': source,
                   'sortBy': sortBy}

        # https://newsapi.org/v1/articles?source=cnn&apiKey=6e402bf74e5e4376b4d991ce169d1ed3
        response = requests.get(buildUrl(), params=payload)
        res_json = loads(response.content)  # transfer string to json

        # Extract news from response
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # Populate news source in each article

            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])

    return articles