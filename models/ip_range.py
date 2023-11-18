class IpRange:
    def __init__(self, start_ip_buffer: bytearray, end_ip_buffer: bytearray, meta_data: object):
        self.start_ip_buffer = bytearray
        self.end_ip_buffer = bytearray
        self.meta_data = meta_data

    def get_collection_name(self):
        return "ip_range"

