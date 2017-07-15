import json
import os
import pickle
import random
import redis
import sys


with open('/home/wenbo/Desktop/Tap-News/config/config.json') as config_file:
	config = json.load(config_file)

print config