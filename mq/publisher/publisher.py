import os
from amqplib import client_0_8 as amqp
from dotenv import load_dotenv

load_dotenv()


class Publisher(object):
    def __init__(self, connection, exchange, routing_key, delivery_mode=2):
        self.connection = connection
        self.channel = self.connection.connection.channel()
        self.exchange = exchange
        self.routing_key = routing_key
        self.delivery_mode = delivery_mode

    def publish(self, message_data):
        message = amqp.Message(message_data)
        message.properties['delivery_mode'] = self.delivery_mode
        self.channel.basic_publish(message, exchange=self.exchange, routing_key=self.routing_key)
        return message

    def close(self):
        if getattr(self, 'channel'):
            self.channel.close()
        if getattr(self, 'connection.py'):
            self.connection.connection.close()
