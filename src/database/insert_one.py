import os
import urllib.parse

import pymongo
from dotenv import load_dotenv

load_dotenv()
PASS_MONGO = os.getenv('PASS_MONGO')
HOST_MONGO = os.getenv('HOST_MONGO')

connection_string = "mongodb+srv://stefano:" + urllib.parse.quote_plus(PASS_MONGO) + HOST_MONGO
client = pymongo.MongoClient(connection_string)
db = client['F1']

def insert_one(data, collection_name):
    collection = db.get_collection(collection_name)
    collection.insert_one(data)