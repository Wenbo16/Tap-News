from pymongo import MongoClient
import logging
import os
import sys
import json

with open('/home/wenbo/Desktop/Tap-News/config/config.json') as config_file:
	config = json.load(config_file)

MONGO_DB_HOST = config['common']['mongodb']['MONGO_DB_HOST']
MONGO_DB_PORT = config['common']['mongodb']['MONGO_DB_PORT']
DB_NAME = config['common']['mongodb']['DB_NAME']

try:
	client = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))
except err:
	logging.error('connect to %s:%s' % (MONGO_DB_HOST, MONGO_DB_PORT), exc_info=True)

def get_db(db=DB_NAME):
    db = client[db]
    return db
