from ipwhois import IPWhois


class Rdap:
    @staticmethod
    def query_ip(self, start_ip: str):
        return IPWhois(address=start_ip).lookup_rdap(depth=5, retry_count=10, rate_limit_timeout=10, bootstrap=False,
                                                     asn_methods=['dns', 'whois', 'http'])
