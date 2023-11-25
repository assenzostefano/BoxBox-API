import logging
import os
import time

import fastf1
import requests
from fastf1.ergast import Ergast

fastf1.logger.set_log_level(logging.ERROR)  # optionally set log level to reduce output

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '../../../../../', 'cache')

fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

def circuits_data(year):
    try:
        for attempt in range(5):
            try:
                print("Year Ergast: " + str(year))
                ergast = Ergast(result_type='pandas', auto_cast=True)
                circuits = ergast.get_circuits(season=year, limit=30)
                data = []
                for index, row in circuits.iterrows():
                    try:
                        time.sleep(5)
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
                    except:
                        time.sleep(5)
                        data.clear()
                        circuits_data(year=year)
                return data
            except requests.exceptions.ConnectionError as e:
                time.sleep(2 ** attempt)
                circuits_data(year=year)
            except:
                time.sleep(2 ** attempt)
                circuits_data(year=year)
    except:
        time.sleep(10)
        circuits_data(year=year)