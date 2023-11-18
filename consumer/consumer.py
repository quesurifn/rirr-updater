import json
from mongo import mongo
from rdap import rdap
from models import ip_range
from mq.connecton import connection
from mq.consumer import consumer
from ipwhois import HTTPRateLimitError
from iptools.ipv4 import ip2long, long2ip
from netaddr import iprange_to_cidrs

consumer = consumer.Consumer(connection.Connection()).declare("rir", "default", 'default', auto_delete=False)
mongo_instance = mongo.Mongo()


def message_callback(message):
    record = json.loads(message.body)
    try:
        if record['record_type'] != 'ipv4' or record['record_type'] != 'ipv6':
            return

        results = rdap.Rdap().query_ip(record['address'])
        cidr = get_cidr(record['address'], record['size'])

        irange = ip_range.IpRange(record['address'].encode(), cidr['last_ip'].encode(), results)
        mongo_instance.upsert({"$and": [
            {"start_ip": {"$gte": record["address"].encode()}},
            {"end_ip": {"$lte": cidr["last_ip"].encode()}}
        ]}, irange)
        consumer.channel.basic_ack(message.delivery_tag)
    except HTTPRateLimitError:
        consumer.channel.basic_nack(message.delivery_tag)


def get_cidr(first_ip, num_ips):
    last_ip = long2ip(ip2long(first_ip) + int(num_ips))
    # Cast the list of IPNetwork objects to a list of strings
    cidrs = iprange_to_cidrs(first_ip, last_ip)
    return {"last_ip": last_ip, "cidr": cidrs[0]}


consumer.register(message_callback)
consumer.wait()
