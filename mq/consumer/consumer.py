import socket
from mq.connecton import connection


class Consumer(object):
    def __init__(self, conn: connection.Connection):
        self.queue = None
        self.exchange = None
        self.routing_key = None
        self.consumer_tag = None
        self.connection = conn
        self.channel = self.connection.connection.channel()

    def close(self):
        if getattr(self, 'channel'):
            self.channel.close()
        if getattr(self, 'connection'):
            self.connection.close()

    def declare(self, queue: str, exchange: str, routing_key: str, durable=True, exclusive=False, auto_delete=False):
        self.queue = queue
        self.exchange = exchange
        self.routing_key = routing_key

        self.channel.queue_declare(queue=self.queue, durable=durable, exclusive=exclusive, auto_delete=auto_delete)
        self.channel.exchange_declare(exchange=self.exchange, type='direct', durable=durable, auto_delete=auto_delete)
        self.channel.queue_bind(queue=self.queue, exchange=self.exchange, routing_key=self.routing_key)

        return self

    def wait(self):
        while True:
            self.channel.wait()

    def register(self, callback, queue=None, consumer_tag=socket.gethostname()):
        if hasattr(self, 'queue') or queue:
            self.consumer_tag = consumer_tag
            self.channel.basic_qos(0, 50, False)
            self.channel.basic_consume(queue=getattr(self, 'queue', queue), no_ack=False, callback=callback,
                                       consumer_tag=consumer_tag)

    def unregister(self, consumer_tag=socket.gethostname()):
        self.channel.basic_cancel(consumer_tag)
