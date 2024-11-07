import logging
import os

import fastf1
import pandas as pd
from fastf1.ergast import Ergast

fastf1.logger.set_log_level(logging.ERROR)  # optionally set log level to reduce output

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '../../../../../', 'cache')
#fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

def race_result(year):
    ergast = Ergast(result_type='pandas', auto_cast=True)
    seasons = ergast.get_race_results(season=year, limit=1000)
    content_df = pd.DataFrame(seasons.content[0])
    description_df = pd.DataFrame(seasons.description)

    data = []
    for index, (content_row, description_row) in enumerate(zip(content_df.iterrows(), description_df.iterrows())):
        # https://docs.fastf1.dev/ergast.html#fastf1.ergast.Ergast.get_race_results
        content_row = content_row[1]
        description_row = description_row[1]

        season = description_row['season']
        round = description_row['round']
        raceUrl = description_row['raceUrl']
        raceName = description_row['raceName']
        raceDate = description_row['raceDate']
        circuitId = description_row['circuitId']
        circuitUrl = description_row['circuitUrl']
        circuitName = description_row['circuitName']
        lat = description_row['lat']
        long = description_row['long']
        locality = description_row['locality']
        country = description_row['country']

        number = content_row['number']
        position = content_row['position']
        position_text = content_row['positionText']
        points = content_row['points']
        grid = content_row['grid']
        laps = content_row['laps']
        status = content_row['status']
        driverid = content_row['driverId']
        driverurl = content_row['driverUrl']
        givenName = content_row['givenName']
        familyName = content_row['familyName']
        dateOfBirth = content_row['dateOfBirth']
        driverNationality = content_row['driverNationality']
        constructorId = content_row['constructorId']
        constructorUrl = content_row['constructorUrl']
        constructorName = content_row['constructorName']
        constructorNationality = content_row['constructorNationality']
        totalRaceTimeMillis = content_row['totalRaceTimeMillis']
        totalRaceTime = content_row['totalRaceTime']

        # TODO: fp1Time = row.get('fp1Time', None)
        try:
            raceTime = description_row['raceTime']
            driverNumber = content_row['driverNumber']
            driverCode = content_row['driverCode']
            fastestLapRank = content_row['fastestLapRank']
            fastestLapNumber = content_row['fastestLapNumber']
            fastestLapTime = content_row['fastestLapTime']
            fastestLapAvgSpeedUnits = content_row['fastestLapAvgSpeedUnits']
            fastestLapAvgSpeed = content_row['fastestLapAvgSpeed']
            fastestLapTimeMillis = content_row['fastestLapTimeMillis']
        except:
            raceTime = None
            driverNumber = None
            driverCode = None
            fastestLapRank = None
            fastestLapNumber = None
            fastestLapTime = None
            fastestLapAvgSpeedUnits = None
            fastestLapAvgSpeed = None
            fastestLapTimeMillis = None

        data.append({
        "Season": season,
        "Round": round,
        "Url": raceUrl,
        "RaceName": raceName,
        "Date": raceDate,
        "Time": raceTime,
        "Circuit": {
            "circuitId": circuitId,
            "url": circuitUrl,
            "circuitName": circuitName,
            "Location": {
                "lat": lat,
                "long": long,
                "locality": locality,
                "country": country
            }
        },
        "Results": [
            {
                number: number,
                "position": position,
                "positionText": position_text,
                "points": points,
                "grid": grid,
                "laps": laps,
                "status": status,
                "Driver": {
                    "driverId": driverid,
                    "permanentNumber": driverNumber,
                    "code": driverCode,
                    "url": driverurl,
                    "givenName": givenName,
                    "familyName": familyName,
                    "dateOfBirth": dateOfBirth,
                    "nationality": driverNationality
                },
                "Constructor": {
                    "constructorId": constructorId,
                    "url": constructorUrl,
                    "name": constructorName,
                    "nationality": constructorNationality
                },
                "Time": {
                    "millis": totalRaceTimeMillis,
                    "time": totalRaceTime
                },
                "FastestLap": {
                    "rank": fastestLapRank,
                    "lap": fastestLapNumber,
                    "Time": {
                        "millis": fastestLapTimeMillis,
                        "time": fastestLapTime
                    },
                    "AverageSpeed": {
                        "units": fastestLapAvgSpeedUnits,
                        "speed": fastestLapAvgSpeed
                    }
                },
                "AverageSpeed": {
                    "units": fastestLapAvgSpeedUnits ,
                    "speed": fastestLapAvgSpeed
                }
            }
        ]
    })

    return data