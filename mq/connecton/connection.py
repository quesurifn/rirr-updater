import os
from amqplib import client_0_8 as amqp
from dotenv import load_dotenv

load_dotenv()


class Connection(object):
    def __init__(self, *args, **kwargs):
        self.connection = None
        self.host = kwargs.get('host', os.getenv('AMQP_SERVER'))
        self.user_id = kwargs.get('user_id', os.getenv('AMQP_USER'))
        self.password = kwargs.get('password', os.getenv('AMQP_PASSWORD'))
        self.vhost = kwargs.get('vhost', os.getenv('AMQP_VHOST', '/'))
        self.port = kwargs.get('port', os.getenv('AMQP_PORT', 5672))
        self.insist = False

        self.connect()

    def connect(self):
        self.connection = amqp.Connection(host='%s:%s' % (self.host, self.port), userid=self.user_id,
                                          password=self.password, virtual_host=self.vhost, insist=self.insist)

    def close(self):
        self.connection.close()
