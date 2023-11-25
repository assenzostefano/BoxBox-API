import os
import urllib.parse

import pymongo
from dotenv import load_dotenv

load_dotenv()
USER_MONGO = os.getenv("USER_MONGO")
PASS_MONGO = os.getenv("PASS_MONGO")
HOST_MONGO = os.getenv("HOST_MONGO")

connection_string = "mongodb+srv://stefano:" + urllib.parse.quote_plus(PASS_MONGO) + HOST_MONGO
client = pymongo.MongoClient(connection_string)
db = client['F1']

def update_one(data, collection_name, value_search_db, existing_doc, data_search):
    collection = db.get_collection(collection_name)

    data_dict = existing_doc.get(data_search, {})
    new_data = data.get(data_search)
    if new_data is not None:
        data_dict.update(new_data)

        collection.update_one({"_id": data["_id"]}, {"$set": {data_search: data_dict}})