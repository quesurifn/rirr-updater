from mq.connecton import connection
from mq.publisher import publisher
from allocated import allocated


def download() -> None:
    conn = connection.Connection()
    pub = publisher.Publisher(conn, "rirr", "default")
    allocated.RirrAllocated(pub, "ARIN").download_and_publish()
    allocated.RirrAllocated(pub, "APNIC").download_and_publish()
    allocated.RirrAllocated(pub, "AFRINIC").download_and_publish()
    allocated.RirrAllocated(pub, "RIPENCC").download_and_publish()
    allocated.RirrAllocated(pub, "LACNIC").download_and_publish()
