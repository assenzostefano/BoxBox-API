import logging
import os

import fastf1
from fastf1.ergast import Ergast

fastf1.logger.set_log_level(logging.ERROR)  # optionally set log level to reduce output

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '../../../../../', 'cache')

#fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

def race_schedule(year):
    ergast = Ergast(result_type='pandas', auto_cast=True)
    seasons = ergast.get_race_schedule(season=year, limit=1000)
    total_race = len(seasons)

    data = []
    for index, row in seasons.iterrows():
        season = row['season']
        round = row['round']
        raceUrl = row['raceUrl']
        raceName = row['raceName']
        raceDate = row['raceDate']
        raceTime = row['raceTime']
        circuitId = row['circuitId']
        circuitUrl = row['circuitUrl']
        circuitName = row['circuitName']
        lat = row['lat']
        long = row['long']
        locality = row['locality']
        country = row['country']
        fp1Date = row['fp1Date']
        fp2Date = row['fp2Date']
        fp3Date = row['fp3Date']
        qualifyingDate = row['qualifyingDate']
        sprintDate = row['sprintDate']
        try:
            fp1Time = row['fp1Time']
            fp2Time = row['fp2Time']
            fp3Time = row['fp3Time']
            qualifyingTime = row['qualifyingTime']
            sprintTime = row['sprintTime']
        except:
            fp1Time = None
            fp2Time = None
            fp3Time = None
            qualifyingTime = None
            sprintTime = None

        data.append({
            "Season": season,
            "Round": round,
            "url": raceUrl,
            "raceName": raceName,
            "raceDate": raceDate,
            "Circuit": {
                "circuitId": circuitId,
                "url": circuitUrl,
                "circuitName": circuitName,
                "Location": {
                    "lat": lat,
                    "long": long,
                    "locality": locality,
                    "country": country
                },
            },
            "date": raceTime,
            "First Practice": {
                "date": fp1Date,
                "time": fp1Time
            },
            "Second Practice": {
                "date": fp2Date,
                "time": fp2Time
            },
            "Third Practice": {
                "date": fp3Date,
                "time": fp3Time
            },
            "Qualifying": {
                "date": qualifyingDate,
                "time": qualifyingTime
            },
            "Sprint": {
                "date": sprintDate,
                "time": sprintTime
            }
        })

    return data