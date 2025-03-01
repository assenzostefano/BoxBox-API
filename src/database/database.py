import os
import urllib.parse

import pymongo
from dotenv import load_dotenv

from src.database.insert_one import insert_one
from src.database.update_one import update_one

load_dotenv()
USER_MONGO = os.getenv("USER_MONGO")
PASS_MONGO = os.getenv("PASS_MONGO")
HOST_MONGO = os.getenv("HOST_MONGO")

def database(data, data_search, collection_name, value_search_db):
    connection_string = "mongodb+srv://stefano:" + urllib.parse.quote_plus(PASS_MONGO) + HOST_MONGO
    client = pymongo.MongoClient(connection_string)
    db = client['F1']

    collection = db.get_collection(collection_name)

    # Check if data is a list
    if isinstance(data, list):
        print("è una lista")
        for i in data:
            id = i['_id']
            # Search on Mongodb if the document exists
            existing_doc = collection.find_one({'_id': id})
            if existing_doc is None:
                # If the document doesn't exist, insert it
                insert_one(data=i, collection_name=collection_name)
            else:
                update_one(data=i, collection_name=collection_name, value_search_db=value_search_db, existing_doc=existing_doc, data_search=data_search)
    else:
        # If data is not a list, insert only one document
        print("ok")

        try:
            id = data['_id']
            # Search on Mongodb if the document exists
            existing_doc = collection.find_one({'_id': id})
            if existing_doc is not None:
                # If the document exists, update it
                update_one(data=data, collection_name=collection_name, value_search_db=value_search_db, existing_doc=existing_doc, data_search=data_search)
            else:
                # If the document doesn't exist, insert it
                insert_one(data=data, collection_name=collection_name)
        except:
            print("PROBLEMA COL DB")
            print(data)

    client.close()