class Allocated:
    def __init__(self, rir: str, country: str, record_type: str, address: str, size: str, date_allocated: str, status: str):
        self.rir = rir
        self.country = country
        self.record_type = record_type
        self.address = address
        self.size = int(size)
        self.date_allocated = int(date_allocated)
        self.status = status
    def get_collection_name(self):
        return "rir_allocated"
