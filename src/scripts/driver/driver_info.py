import logging
import os
from datetime import datetime

import fastf1

from src.scripts.general.ergast import Ergast
from src.scripts.general.wikipedia_data import wikipedia_data

fastf1.logger.set_log_level(logging.ERROR)  # optionally set log level to reduce output

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '../../..', 'cache')

fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

def driver_info(year, identifier, round):
    driver_data = []
    try:
        session = fastf1.get_session(year, round, identifier)
        session.load(laps=True, telemetry=True, weather=True, messages=True, livedata=True)
    except Exception as e:
        try:
            session = fastf1.get_session(year, round, identifier)
            session.load(livedata=True)
        except Exception as e:
            print("Error: " + str(e))
            return None

    for i in session.drivers:
        driver = session.get_driver(i)
        ergast_data = Ergast.drivers_data(year=year)
        for b in ergast_data:
            if b.driverId == driver.DriverId:
                ergast_data = b
                break

        driver_data.append({
            "_id": driver.DriverId,
            "BroadcastName": driver.BroadcastName,
            "FullName": driver.FullName,
            "FirstName": driver.FirstName,
            "LastName": driver.LastName,
            "Abbreviation": driver.Abbreviation,
            "CountryCode": driver.CountryCode,
            "BirthDate": datetime.strftime(ergast_data.dateOfBirth, "%Y-%m-%d"),
            "HeadshotUrl": driver.HeadshotUrl,
            "Wikipedia Data": wikipedia_data(url_wikipedia=ergast_data.url),
            "Years": {
                str(year) + "-" + identifier: {
                    "TeamName": driver.TeamName,
                    "TeamId": driver.TeamId,
                    "TeamColor": driver.TeamColor,
            }
        }})
    return driver_data