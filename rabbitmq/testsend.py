# -*- coding: UTF-8 -*-
import pika

if __name__ == '__main__':

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.exchange_declare(exchange="tang",type="fanout")
    message = "You are awsome!"
    for i in range(0, 100):  # 循环100次发送消息
        channel.basic_publish(exchange="tang", routing_key='', body=message + " " + str(i),)
    print "sending ", message