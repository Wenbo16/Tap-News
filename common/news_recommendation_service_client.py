import pyjsonrpc
import os
import sys
import json

with open('/home/wenbo/Desktop/Tap-News/config/config.json') as config_file:
	config = json.load(config_file)

URL = config['common']['news_recommendation_service_client']['URL']

client = pyjsonrpc.HttpClient(url=URL)

def getPreferenceForUser(userId):
    preference = client.call('getPreferenceForUser', userId)
    print "Preference list: %s" % str(preference)
    return preference