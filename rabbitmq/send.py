#!/usr/bin/env python
import pika
import sys
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',virtual_host='/'))
channel = connection.channel()


#channel.queue_declare(queue='hello')

channel.basic_publish(exchange=sys.argv[1],
                      routing_key=sys.argv[2],
                      body=sys.argv[3])
print(" [x] Sent 'Hello World!'")
connection.close()
