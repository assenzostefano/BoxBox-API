import pandas as pd
from fastf1.ergast import Ergast
def ergast_race_result(year):
    ergast = Ergast(result_type='pandas', auto_cast=True)
    seasons = ergast.get_race_results(season=year, limit=1000).content[0]
    df = pd.DataFrame(seasons)

    for index, row in df.iterrows():
        # https://docs.fastf1.dev/ergast.html#fastf1.ergast.Ergast.get_race_results
        number = row['number']
        position = row['position']
        position_text = row['positionText']
        print(position_text)
        points = row['points']
        grid = row['grid']
        laps = row['laps']
        status = row['status']
        driverid = row['driverId']
        drivernumber = row['driverNumber']
        drivercode = row['driverCode']
        driverurl = row['driverUrl']
        givenname = row['givenName']
        familyname = row['familyName']
        dateofbirth = row['dateOfBirth']
        drivernationality = row['driverNationality']
        constructorid = row['constructorId']
        constructorurl = row['constructorUrl']
        constructorname = row['constructorName']
        constructornationality = row['constructorNationality']
        totalracetimemillis = row['totalRaceTimeMillis']
        totalracetime = row['totalRaceTime']
        fastestlaprank = row['fastestLapRank']
        fastestlapnumber = row['fastestLapNumber']
        #fastestlaptimemillis = row['fastestLapTimeMillis']
        fastestlaptime = row['fastestLapTime']
        fastestlapavgspeedunits = row['fastestLapAvgSpeedUnits']
        fastestlapavgspeed = row['fastestLapAvgSpeed']

    return "Ergast data"