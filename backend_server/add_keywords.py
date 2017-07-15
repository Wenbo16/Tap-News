from newspaper import Article
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

NEWS_TABLE_NAME = "news"
db = mongodb_client.get_db()

# mongoDB returns iterable
all_news = list(db[NEWS_TABLE_NAME].find())
list1 =  all_news[1]['keywords']
list2 =  all_news[2]['keywords']
list3 =  all_news[3]['keywords']
list4 =  all_news[4]['keywords']

b3 = [val for val in list1 if val in list2]
print set.intersection(set(list1), set(list2))


# for news in all_news:
#     article = Article(news['url'])
#     article.download()
#     article.parse()
#     article.nlp()
#     news['keywords'] = article.keywords
#     db[NEWS_TABLE_NAME].replace_one({'digest': news['digest']}, news)


