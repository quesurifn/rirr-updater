from fastapi import FastAPI
from logger.logger import init_logging
from fastapi_utils.tasks import repeat_every
from jobs.download import download
from mongo import mongo

app = FastAPI()

init_logging()
mongo = mongo.Mongo()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/ip")
async def get_ip(ip: str):
    rec = mongo.query('ip_range', {"$and": [
        {"start_ip": {"$gte": ip.encode()}},
        {"end_ip": {"$lte": ip.encode()}}]}, limit=1, offset=0)
    return rec


@app.get("/asn")
async def get_asn(asn: int):
    return {"message": "ok"}


# Download IP allocations daily
@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)
def download_new_allocations():
    download()
