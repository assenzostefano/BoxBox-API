from src.scripts.general.wikipedia_data import wikipedia_data
from src.scripts.general.ergast import Ergast

from datetime import datetime
import logging
import fastf1
import time
import os

fastf1.logger.set_log_level(logging.ERROR)  # optionally set log level to reduce output

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '../../..', 'cache')

#fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

def driver_info(year, identifier, round):
    driver_data = []
    driver = Ergast.drivers_data(year=year, round=round, result_type='raw')
    session = fastf1.get_session(year, round, identifier, backend='ergast')
    session.load()

    for i in session.drivers:
        print("i'm here " + i)
        session = session.get_driver(i)

        if driver[i]['driverId'] == session.DriverId:
            driver = drivers
            break
        for drivers in driver:
            driver_data.append({
                    "_id": drivers['driverId'],
                    "BroadcastName": drivers['givenName'] + " " + drivers['familyName'],
                    "FullName": drivers['givenName'] + " " + drivers['familyName'],
                    "FirstName": drivers['givenName'],
                    "LastName": drivers['familyName'],
                    "Abbreviation": session.Abbreviation,
                    "CountryCode": drivers['nationality'],
                    "BirthDate": drivers['dateOfBirth'],
                    "Wikipedia Data": wikipedia_data(url_wikipedia=drivers['url']),
                    "Years": {
                        str(year) + "-" + identifier: {
                            "TeamName": session.TeamName,
                            "TeamId": session.TeamId,
                            "TeamColor": session.TeamColor,
                    }
                }}
            )
            print(driver_data)
    
    #print(driver_data)
    return driver_data

def get_data(year, session, identifier):
    driver_data = []
    try:
        ergast_data = Ergast.drivers_data(year=year, ) # Data from Ergast (Yukinator)

        for i in session.drivers:
            driver = session.get_driver(i) # Data from FastF1

            selected_driver = next((drivers for drivers in ergast_data if drivers.driverId == driver.DriverId), None)
            if selected_driver:
                driver_data.append({
                "_id": driver.DriverId,
                "BroadcastName": driver.BroadcastName,
                "FullName": driver.FullName,
                "FirstName": driver.FirstName,
                "LastName": driver.LastName,
                "Abbreviation": driver.Abbreviation,
                "CountryCode": driver.CountryCode,
                "BirthDate": selected_driver.dateOfBirth.strftime("%Y-%m-%d"),
                "HeadshotUrl": driver.HeadshotUrl,
                "Wikipedia Data": wikipedia_data(url_wikipedia=selected_driver.url),
                "Years": {
                    str(year) + "-" + identifier: {
                        "TeamName": driver.TeamName,
                        "TeamId": driver.TeamId,
                        "TeamColor": driver.TeamColor,
                }
            }}
        )

            else:
                print("Info Ergast non trovate")
                driver_data.append({
                "_id": driver.DriverId,
                "BroadcastName": driver.BroadcastName,
                "FullName": driver.FullName,
                "FirstName": driver.FirstName,
                "LastName": driver.LastName,
                "Abbreviation": driver.Abbreviation,
                "CountryCode": driver.CountryCode,
                "BirthDate": "",
                "HeadshotUrl": driver.HeadshotUrl,
                "Wikipedia Data": "",
                "Years": {
                    str(year) + "-" + identifier: {
                        "TeamName": driver.TeamName,
                        "TeamId": driver.TeamId,
                        "TeamColor": driver.TeamColor,
                }
            }}
        )


        return driver_data
    except:
        print("Impossibile continuare")