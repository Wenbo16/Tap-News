import datetime
import os
import sys
import json

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

with open('/home/wenbo/Desktop/Tap-News/config/config.json') as config_file:
    config = json.load(config_file)

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = config['news_pipeline']['news_deduper']['DEDUPE_NEWS_TASK_QUEUE_URL']
DEDUPE_NEWS_TASK_QUEUE_NAME = config['news_pipeline']['news_deduper']['DEDUPE_NEWS_TASK_QUEUE_NAME']

SLEEP_TIME_IN_SECONDS = config['news_pipeline']['news_deduper']['SLEEP_TIME_IN_SECONDS']

SAME_NEWS_SIMILARITY_THRESHOLD = config['news_pipeline']['news_deduper']['SAME_NEWS_SIMILARITY_THRESHOLD']

NEWS_TABLE_NAME = config['news_pipeline']['news_deduper']['NEWS_TABLE_NAME']

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict) :
        return
    task = msg
    text = str(task['text'])
    if text is None:
        return

    # Get all recent news based on publishedAt
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year,
                                               published_at.month,
                                               published_at.day,
                                               0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()

    # mongoDB returns iterable
    same_day_news_list = list(db[NEWS_TABLE_NAME].find(
        {'publishedAt': {'$gte': published_at_day_begin,
                         '$lt': published_at_day_end}}))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [str(news['text']) for news in same_day_news_list]
        documents.insert(0, text)

        # Calculate similarity matrix
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        print pairwise_sim

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print "Duplicated news. Ignore"
                return

    task['publishedAt'] = parser.parse(task['publishedAt'])
    
    # if the news is the same
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass

        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)