import os
import sys
import json
from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

with open('/home/wenbo/Desktop/Tap-News/config/config.json') as config_file:
    config = json.load(config_file)

SLEEP_TIME_IN_SECONDS = config['news_pipeline']['news_fetcher']['SLEEP_TIME_IN_SECONDS']

# TODO: add your own queue url and name
DEDUPE_NEWS_TASK_QUEUE_URL = config['news_pipeline']['news_fetcher']['DEDUPE_NEWS_TASK_QUEUE_URL']
DEDUPE_NEWS_TASK_QUEUE_NAME = config['news_pipeline']['news_fetcher']['DEDUPE_NEWS_TASK_QUEUE_NAME']
SCRAPE_NEWS_TASK_QUEUE_URL = config['news_pipeline']['news_fetcher']['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = config['news_pipeline']['news_fetcher']['SCRAPE_NEWS_TASK_QUEUE_NAME']

scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)



def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return

    task = msg
    text = None

    # Support CNN only
    # if task['source'] == 'cnn';
    #     print 'scraping CNN news'
    #     text = cnn_news_scraper.extract_news(task['url'])
    # else:
    #     'News source is not supported'

    # task['text'] = text
    # dedupe_news_queue_client.sendMessage(task)

    article = Article(task['url'])
    article.download()
    article.parse()
    article.nlp()
    task['keywords'] = article.keywords
    task['text'] = article.text
    dedupe_news_queue_client.sendMessage(task)


while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)