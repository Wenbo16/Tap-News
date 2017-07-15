import operations
import pyjsonrpc
import os
import sys
import json
import logging
from logstash_formatter import LogstashFormatterV1

with open('/home/wenbo/Desktop/Tap-News/config/config.json') as config_file:
    config = json.load(config_file)

SERVER_HOST = config['backend_server']['service']['SERVER_HOST']
SERVER_PORT = config['backend_server']['service']['SERVER_PORT']

# Initialize logger
logger = logging.getLogger('backend-server')
logger.setLevel(logging.INFO)
logFile = logging.FileHandler('main.log')
formatter = LogstashFormatterV1()
logFile.setFormatter(formatter)
logger.addHandler(logFile)


class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ Test Method """
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "add is called with %d and %d" % (a, b)
        return a + b

    """ Get news summaries for a user """
    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        logger.info('get news summaries for user')
        return operations.getNewsSummariesForUser(user_id, page_num)

    """ Log user news clicks """
    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id):
        logger.info('log news clicks for user')
        return operations.logNewsClickForUser(user_id, news_id)

    """ get similar news based on clicks """
    @pyjsonrpc.rpcmethod
    def getSimilarNews(self, user_id, news_id):
        logger.info('get similar news for user')
        return operations.getSimilarNews(user_id, news_id)

# Threading HTTP Server
http_server = pyjsonrpc.ThreadingHttpServer(
  server_address = (SERVER_HOST, SERVER_PORT),
  RequestHandlerClass = RequestHandler
)

logger.info("Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT))
print "Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()