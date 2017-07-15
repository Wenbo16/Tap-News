import datetime
import hashlib
import os
import redis
import sys
import json

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
with open('/home/wenbo/Desktop/Tap-News/config/config.json') as config_file:
    config = json.load(config_file)

import news_api_client

from cloudAMQP_client import CloudAMQPClient

NEWS_SOURCES = config['news_pipeline']['news_monitor']['NEWS_SOURCES']

REDIS_HOST = config['news_pipeline']['news_monitor']['REDIS_HOST']
REDIS_PORT = config['news_pipeline']['news_monitor']['REDIS_PORT']

NEWS_TIME_OUT_IN_SECONDS = config['news_pipeline']['news_monitor']['NEWS_TIME_OUT_IN_SECONDS']
SLEEP_TIME_IN_SECONDS = config['news_pipeline']['news_monitor']['SLEEP_TIME_IN_SECONDS']

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

SCRAPE_NEWS_TASK_QUEUE_URL = config['news_pipeline']['news_monitor']['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = config['news_pipeline']['news_monitor']['SCRAPE_NEWS_TASK_QUEUE_NAME']

cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)
    num_of_new_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            # If 'publishedAt' is None, set it to current UTC time.
            if news['publishedAt'] is None:
                # Make the time in format YYYY-MM_DDTHH:MM:SS in UTC
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)

    print "Fetched %d news." % num_of_new_news

    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)