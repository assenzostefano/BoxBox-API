import logging
import os
import time

import fastf1
import requests
from fastf1.ergast import Ergast

fastf1.logger.set_log_level(logging.ERROR)  # optionally set log level to reduce output

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# FastF1 Cache
try:
    cache_directory = os.path.join(current_directory, '../../../../../', 'cache')
    fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location
except:
    print("Impossibile accedere alla cache")

def circuits_data(year, round):
    ergast = Ergast(result_type='pandas', auto_cast=True)
    circuits = ergast.get_circuits(season=year, round=round, limit=30)
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