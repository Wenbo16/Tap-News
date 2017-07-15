# -*- coding: utf-8 -*
import json
import pika
import logging

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3

        # Create a connection object. Here, the username, password, connection URL, port, etc., will be specified.
        # A TCP connection will be set up between the application and RabbitMQ.
        self.connection = pika.BlockingConnection(self.params)

        # The connection interface can be used to open a channel and 
        # when the channel is opened it can be used to send and receive messages.
        self.channel = self.connection.channel() 

        # Declaring a queue will cause it to be created if it does not already exist. 
        # All queues need to be declared before they can be used.
        self.channel.queue_declare(queue=queue_name) 


    # send a message
    def sendMessage(self, message):

        # The default exchange means that messages are routed to the queue with the name
        # specified by routing_key if it exists.
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=json.dumps(message))
        print "[x] Sent message to %s: %s" % (self.queue_name, message)
        logging.info("[x] Sent message to %s: %s" % (self.queue_name, message))


    # get a message if the server returns a message
    def getMessage(self):
        # 是consumer。不用basic consume（）是因为我们的queue操作是封装在CloudAMQP_client里的，不方便使用callback的方式调用，我不想把callback传进去。（实际上这么设计也可以）
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name) # basic_get是 blocking的
        if method_frame:
            print "[x] Received message from %s: %s" % (self.queue_name, body)
            logging.info("[x] Received message from %s: %s" % (self.queue_name, body))

            # inform the message is recieved by offering using delivery_tag and delete the message 
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            print 'No message returned'
            logging.info('No message returned')
            return None

    # BlockingConnection.sleep is a safer way to sleep than time.sleep(). This
    # will repond to server's heartbeat.
    def sleep(self, seconds):
        self.connection.sleep(seconds)


    def close(self, connection):
        self.connection.close()