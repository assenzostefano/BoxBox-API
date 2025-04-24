from fastf1.ergast.interface import ErgastError, ErgastJsonError, ErgastInvalidRequestError
from fastf1.ergast import Ergast
import requests
import logging
import fastf1
import os

current_directory = os.path.dirname(os.path.abspath(__file__)) # Take the current directory
cache_directory = os.path.join(current_directory, '../../../../../', 'cache') # Join the current directory with the cache folder

fastf1.logger.set_log_level(logging.ERROR)  # Only show errors FASTF1

# FastF1 Cache
try:
    fastf1.Cache.enable_cache(cache_directory)
except:
    print("Impossibile accedere alla cache")

def jolpi_api(year, round):
    try:
        circuit_id = fastf1.get_session()

        url = "https://api.jolpi.ca/ergast/f1/circuits/"

    except Exception as e:
        print(f"Error: {e}")

def circuits_data(year, round):
    ergast = Ergast(result_type='pandas', auto_cast=True)

    try:
        circuits = ergast.get_circuits(season=year, round=round, limit=30)
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, ErgastInvalidRequestError, ErgastJsonError, ErgastError) as e:
        print(f"Error: {e}")
        


    data = []
    
    for index, row in circuits.iterrows():
        circuitId = row['circuitId']
        circuitUrl = row['circuitUrl']
        circuitName = row['circuitName']
        lat = row['lat']
        long = row['long']
        locality = row['locality']
        country = row['country']
        data.append({
            "circuitId": circuitId,
            "circuitUrl": circuitUrl,
            "circuitName": circuitName,
            "Location": {
                "lat": lat,
                "long": long,
                "locality": locality,
                "country": country
            }
        })
    
    return data