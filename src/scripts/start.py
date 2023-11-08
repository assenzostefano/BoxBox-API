import os
import urllib.parse

import pymongo
from dotenv import load_dotenv

from src.scripts.circuit.circuit_info import circuit_info
from src.scripts.constructor.constructor_info import constructor_info
from src.scripts.driver.driver_info import driver_info
from src.scripts.session.session_data import session_data

load_dotenv()

USER_MONGO = os.getenv("USER_MONGO")
PASS_MONGO = os.getenv("PASS_MONGO")
HOST_MONGO = os.getenv("HOST_MONGO")

connection_string = "mongodb+srv://stefano:" + urllib.parse.quote_plus(PASS_MONGO) + HOST_MONGO
client = pymongo.MongoClient(connection_string)
db = client['F1']

def start():
    # Circuit data
    for i in range(1950, 2023):
        circuit= circuit_info(year=i, db=db)

    # Driver data
    for i in range(1950, 2023):
        driver = driver_info(year=i, db=db)

    # Constructor data
    for i in range(1950, 2023):
        constructor = constructor_info(year=i, db=db)

    # Session data
    for i in range(1950, 2023):
        session = session_data(year=i, db=db)