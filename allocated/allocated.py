import requests
from models import allocated


class RirrAllocated:
    ripencc_base_url = "https://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-latest"
    lacnic_base_url = "https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-latest"
    apnic_base_url = "https://ftp.apnic.net/stats/apnic/delegated-apnic-latest"
    afrinic_base_url = "https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-latest"
    arin_base_url = "https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest"

    def __init__(self, publisher, rirr: str):
        self.rirr = rirr
        self.publisher = publisher

        match rirr:
            case "AFRINIC":
                self.url = self.afrinic_base_url
            case "LACNIC":
                self.url = self.lacnic_base_url
            case "APNIC":
                self.url = self.apnic_base_url
            case "ARIN":
                self.url = self.arin_base_url
            case "RIPENCC":
                self.url = self.ripencc_base_url
            case _:
                raise ValueError("Invalid RIRR")

    def download_and_publish(self):
        # NOTE the stream=True parameter below
        r = requests.get(self.url, stream=True)
        for line in r.iter_lines():
            if line and len(line.strip()) and line.strip()[0] == '#':
                continue
            parts = [part.strip() for part in line.split('|')]
            if len(parts) < 7:
                continue

            cleaned = parts[:7]
            cleaned_allocated = allocated.Allocated(cleaned[0], cleaned[1], cleaned[2], cleaned[3], cleaned[4], cleaned[5], cleaned[6])
            self.publisher.publish(vars(cleaned_allocated))
