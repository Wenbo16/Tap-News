from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://jbxtueac:LOc-nR8gE1mB416_2Lv8-nqm8MZ4uwIh@fish.rmq.cloudamqp.com/jbxtueac'
QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

    sentMsg = {'test_key':'test_value'}
    client.sendMessage(sentMsg)
    client.sleep(5)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test_basic passed.'

if __name__ == "__main__":
    test_basic()
