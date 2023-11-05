import os
import urllib
from urllib.parse import urlsplit

import pymongo
import requests
from dotenv import load_dotenv

from src.scripts.constructor_info import constructor
from src.scripts.general.wikipedia_data import wikipedia_data
from src.scripts.session_data import race_data

load_dotenv()

USER_MONGO = os.getenv("USER_MONGO")
PASS_MONGO = os.getenv("PASS_MONGO")
HOST_MONGO = os.getenv("HOST_MONGO")

# use urllib.parse.quote_plus
connection_string = "mongodb+srv://stefano:" + urllib.parse.quote_plus(PASS_MONGO) + HOST_MONGO

def get_driver_info():
    # Connessione al database
    count = 0
    client = pymongo.MongoClient(connection_string)
    db = client['F1']
    collection = db['drivers']

    # Ergast API Drivers base data
    url = 'https://ergast.com/api/f1/drivers.json?limit=10000' # Take all drivers (limit=10000)
    response = requests.get(url).json()
    drivers = response['MRData']['DriverTable']['Drivers']

    for driver in drivers:
        count += 1
        # Take all drivers info from Ergast API
        id = driver['driverId']
        url = driver['url']
        given_name = driver['givenName']
        family_name = driver['familyName']
        date_of_birth = driver['dateOfBirth']
        nationality = driver['nationality']

        # Wikipedia API Biography Driver
        wikipedia_driver = wikipedia_data(url_wikipedia=url)

        # Ergast API Drivers standings
        url_standings = 'https://ergast.com/api/f1/drivers/' + id + '/driverStandings.json'
        driver_info = requests.get(url_standings).json()

        driver_standings = []
        for standings in driver_info['MRData']['StandingsTable']['StandingsLists']:
            year = standings['season']
            round = standings['round']
            for standings in standings['DriverStandings']:
                race_data(year=int(year), db=db)
                for constructors in standings['Constructors']:
                    constructor(constructors=constructors, db=db)

        # Insert data into MongoDB
        collection.insert_one({
            "ID": id,
            "Given Name": given_name,
            "Family Name": family_name,
            "Date of Birth": date_of_birth,
            "Nationality": nationality,
            "Driver Standings": driver_standings,
            "URL Wikipedia": url,
            wikipedia_driver['type']: wikipedia_driver,
        })

        print('ID: ' + id)
        print('Given Name: ' + given_name)
        print('Family Name: ' + family_name)
        print('Date of Birth: ' + date_of_birth)
        print('Nationality: ' + nationality)
        print('Biography Driver: ' + str(wikipedia_driver))
        print('--------')

get_driver_info()
