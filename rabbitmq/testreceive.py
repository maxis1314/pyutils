# -*- coding: UTF-8 -*-
import pika

__author__ = 'Yue'


def callback(ch, method, properties, body):
    print body


if __name__ == '__main__':
    connection=pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel=connection.channel()
    channel.exchange_declare(exchange="logs",type="fanout")
    #随机生成Queue
    result=channel.queue_declare(exclusive=True)
    #获取queue的name
    queue_name=result.method.queue
    print "queue_name",queue_name
    channel.queue_bind(exchange="logs",queue=queue_name)
    channel.basic_consume(callback,queue=queue_name,no_ack=True)
    channel.start_consuming()