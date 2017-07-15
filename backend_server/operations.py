import json
import os
import pickle
import random
import redis
import sys

import logging
logger = logging.getLogger('backend-server.operations.')

from bson.json_util import dumps
from datetime import datetime

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

with open('/home/wenbo/Desktop/Tap-News/config/config.json') as config_file:
    config = json.load(config_file)


import mongodb_client
import news_recommendation_service_client

from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = config['backend_server']['operations']['REDIS_HOST']
REDIS_PORT = config['backend_server']['operations']['REDIS_PORT']

NEWS_TABLE_NAME = config['backend_server']['operations']['NEWS_TABLE_NAME']
CLICK_LOGS_TABLE_NAME = config['backend_server']['operations']['CLICK_LOGS_TABLE_NAME']

NEWS_LIMIT = config['backend_server']['operations']['NEWS_LIMIT']  # a user can only have load NEWS_LIMIT news
NEWS_LIST_BATCH_SIZE = config['backend_server']['operations']['NEWS_LIST_BATCH_SIZE']  
USER_NEWS_TIME_OUT_IN_SECONDS = config['backend_server']['operations']['USER_NEWS_TIME_OUT_IN_SECONDS']

LOG_CLICKS_TASK_QUEUE_URL = config['backend_server']['operations']['LOG_CLICKS_TASK_QUEUE_URL']
LOG_CLICKS_TASK_QUEUE_NAME = config['backend_server']['operations']['LOG_CLICKS_TASK_QUEUE_NAME']

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)




def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

   

    # The final list of news to be returned.
    sliced_news = []

    if redis_client.get(user_id) is not None:
        logger.info('user is already in redis')
        news_digests = pickle.loads(redis_client.get(user_id))

        # If begin_index is out of range, this will return empty list;
        # If end_index is out of range (begin_index is within the range), this
        # will return all remaining news ids.
        sliced_news_digests = news_digests[begin_index:end_index]
        logger.info('load sliced news')

        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        logger.info('user is not in redis')
        db = mongodb_client.get_db()
        try:
            total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        finally:
            logger.error('Some error occurs when find news in MongoDB')
            
        total_news_digests = map(lambda x:x['digest'], total_news)

        redis_client.set(user_id, pickle.dumps(total_news_digests))
        logger.info('user $s is set to redis', user_id)
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    # Get preference for the user
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]
        print 'top preference is: topPreference', topPreference


    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        if news['class'] == topPreference:
            news['reason'] = 'Recommend'
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': datetime.utcnow()}

    db = mongodb_client.get_db()
    db[CLICK_LOGS_TABLE_NAME].insert(message)
    logger.info('get a new click')


    # Send log task to machine learning service for prediction
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    cloudAMQP_client.sendMessage(message)



def getSimilarNews(user_id, news_id):
    db = mongodb_client.get_db()
    clickedNews = db[NEWS_TABLE_NAME].find_one({'digest':news_id})
    similarNews = []
    news_digests = pickle.loads(redis_client.get(user_id))
    
    all_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in': news_digests}}))
    for news in all_news:
        
        intersection = set.intersection(set(news['keywords']), set(clickedNews['keywords']))
        if len(intersection) >= 2 and news['digest'] != news_id:
            similarNews.append(news)
    print 'got similar news'
    return json.loads(dumps(similarNews))