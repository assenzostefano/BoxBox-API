import logging
import os

import fastf1
import pytz
import requests
from dotenv import load_dotenv
from fastf1.ergast import Ergast

load_dotenv()

rome_tz = pytz.timezone('Europe/Rome')

fastf1.logger.set_log_level(logging.ERROR)  # optionally set log level to reduce output

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '..', 'cache')

fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

# Funzione per salvare i risultati delle gare per un dato anno
def race_data(year, db):
    api = Ergast()
    print(year)
    url = f"http://ergast.com/api/f1/{year}/results.json"
    get_number_session = f"http://ergast.com/api/f1/{year}.json"
    if year >= 2018:
        print("yes")
        # Get data from url
        response = requests.get(get_number_session)
        # Convert to json
        json_data = response.json()
        # Get data from json
        results = json_data['MRData']['RaceTable']['Races']
        # Count number of list in results
        max_race_number = len(results)

        sessions = ['FP1', 'FP2', 'FP3', 'Q', 'R']
        for i in range(1, max_race_number):
            for session in sessions:
                try:
                    session = fastf1.get_session(year, i, session)
                    session.load(weather=True, telemetry=True, messages=True, laps=True)

                    year = session.date.year
                    date = session.date
                    circuit_name = session.event['EventName']

                    latitude = api.get_circuits(season=year, round=i, result_type='raw', auto_cast=False)[0]['Location'][
                    'lat']  # Latitude of circuite
                    longitude = api.get_circuits(season=year, round=i, result_type='raw', auto_cast=False)[0]['Location'][
                    'long']  # Longitude of circuite
                    locality = api.get_circuits(season=year, round=i, result_type='raw', auto_cast=False)[0]['Location'][
                    'locality']  # Locality of circuite
                    country = api.get_circuits(season=year, round=i, result_type='raw', auto_cast=False)[0]['Location'][
                    'country']  # Country of circuite

                    start_time_session = session.t0_date  # Start time of session
                    start_time_session = start_time_session.tz_localize('UTC').tz_convert('Europe/Rome')

                    # Estrai l'orario
                    start_time_session = start_time_session.strftime("%H:%M:%S.%f")
                    total_laps = session.total_laps

                    session_status = session.session_status

                    weather = session.weather_data  # Weather of session
                    for j in range(0, len(weather)):
                        weather_time = weather['Time']
                        weather_air_temp = weather['AirTemp']
                        weather_track_temp = weather['TrackTemp']
                        weather_humidity = weather['Humidity']
                        weather_pressure = weather['Pressure']
                        weather_wind_speed = weather['WindSpeed']
                        weather_wind_direction = weather['WindDirection']
                        weather_rainfall = weather['Rainfall']
                        print("Weather Time" + str(weather_time[j]))
                        print("AirTemp: " + str(weather_air_temp[j]))
                        print("TrackTemp: " + str(weather_track_temp[j]))
                        print("Humidity: " + str(weather_humidity[j]))
                        print("Pressure: " + str(weather_pressure[j]))
                        print("WindSpeed: " + str(weather_wind_speed[j]))
                        print("WindDirection: " + str(weather_wind_direction[j]))
                        print("Rainfall: " + str(weather_rainfall[j]))
                        print("------------------------")

                    track_status = session.track_status  # Track status of session
                    for i in range(0, len(track_status)):
                        track_status_time = track_status['Time']
                        track_status_status = track_status['Status']
                        track_status_message = track_status['Message']
                        print("Track status time: " + str(track_status_time[i]))
                        print("Track status status: " + str(track_status_status[i]))
                        print("Track status message: " + str(track_status_message[i]))

                    laps = session.laps
                    for index, row in laps.iterrows():
                        driver = row['Driver']
                        print(driver)
                        telemetry = laps.pick_driver(driver)
                        for i in telemetry.iterlaps():
                            driver_telemetry = i[
                            1].get_telemetry()  # https://docs.fastf1.dev/core.html#fastf1.core.Telemetry
                            print(driver_telemetry['Speed'])
                            print(driver_telemetry['nGear'])

                    laps_data = session.laps
                    for index, row in laps_data.iterrows():
                        time = row['Time']
                        driver = row['Driver']
                        driver_number = row['DriverNumber']
                        lap_time = row['LapTime']
                        lap_number = row['LapNumber']
                        stint = row['Stint']
                        pit_out_time = row['PitOutTime']
                        pit_in_time = row['PitInTime']
                        sector1_time = row['Sector1Time']
                        sector2_time = row['Sector2Time']
                        sector3_time = row['Sector3Time']
                        sector1_session_time = row['Sector1SessionTime']
                        sector2_session_time = row['Sector2SessionTime']
                        sector3_session_time = row['Sector3SessionTime']
                        speedI1 = row['SpeedI1']
                        speedI2 = row['SpeedI2']
                        speedFL = row['SpeedFL']
                        speedST = row['SpeedST']
                        isPersonalBest = row['IsPersonalBest']
                        compound = row['Compound']
                        tyrelife = row['TyreLife']
                        freshtyre = row['FreshTyre']
                        team = row['Team']
                        lap_start_time = row['LapStartTime']
                        lap_start_date = row['LapStartDate']
                        track_status = row['TrackStatus']
                        position = row['Position']
                        deleted = row['Deleted']
                        deleted_reason = row['DeletedReason']
                        fastf1_generated = row['FastF1Generated']
                        isaccurate = row['IsAccurate']

                        print("Time: " + str(time))
                        print("Driver: " + str(driver))
                        print("DriverNumber: " + str(driver_number))
                        print("LapTime: " + str(lap_time))
                        print("LapNumber: " + str(lap_number))
                        print("Stint: " + str(stint))
                        print("PitOutTime: " + str(pit_out_time))
                        print("PitInTime: " + str(pit_in_time))
                        print("Sector1Time: " + str(sector1_time))
                        print("Sector2Time: " + str(sector2_time))
                        print("Sector3Time: " + str(sector3_time))
                        print("Sector1SessionTime: " + str(sector1_session_time))
                        print("Sector2SessionTime: " + str(sector2_session_time))
                        print("Sector3SessionTime: " + str(sector3_session_time))
                        print("SpeedI1: " + str(speedI1))
                        print("SpeedI2: " + str(speedI2))
                        print("SpeedFL: " + str(speedFL))
                        print("SpeedST: " + str(speedST))
                        print("IsPersonalBest: " + str(isPersonalBest))
                        print("Compound: " + str(compound))
                        print("TyreLife: " + str(tyrelife))
                        print("FreshTyre: " + str(freshtyre))
                        print("Team: " + str(team))
                        print("LapStartTime: " + str(lap_start_time))
                        print("LapStartDate: " + str(lap_start_date))
                        print("TrackStatus: " + str(track_status))
                        print("Position: " + str(position))
                        print("Deleted: " + str(deleted))
                        print("DeletedReason: " + str(deleted_reason))
                        print("FastF1Generated: " + str(fastf1_generated))
                        print("IsAccurate: " + str(isaccurate))
                        print("------------------------")
                except Exception as e:
                    print("ok")
    else:
        response = requests.get(url)
        data = response.json()
        races = data['MRData']['RaceTable']['Races']
        for race in races:
            season = float(race['season'])
            print(season)
            circuit_name = race['raceName']
            circuit_id = race['Circuit']['circuitId']
            date = race['date']
            time = race.get('time', '')
            lat = race['Circuit']['Location']['lat']
            long = race['Circuit']['Location']['long']
            locality = race['Circuit']['Location']['locality']
            country = race['Circuit']['Location']['country']
            for result in race['Results']:
                number = result['number']
                position = result['position']
                position_text = result['positionText']
                points = result['points']
                driver_id = result['Driver']['driverId']
                driver_name = result['Driver']['givenName'] + ' ' + result['Driver']['familyName']
                driver_nationality = result['Driver']['nationality']
                constructor_id = result['Constructor']['constructorId']
                constructor_name = result['Constructor']['name']
                constructor_nationality = result['Constructor']['nationality']
                constructor_grid = result['grid']
                constructor_laps = result['laps']
                constructor_status = result['status']
                time = result.get('Time', {}).get('time', '')
                fastest_lap_rank = result.get('FastestLap', {}).get('rank', '')
                fastest_lap_lap = result.get('FastestLap', {}).get('lap', '')

                try:
                    average_speed_units = result['FastestLap']['AverageSpeed']['units']
                except:
                    average_speed_units = ''
                try:
                    average_speed_speed = result['FastestLap']['AverageSpeed']['speed']
                except:
                    average_speed_speed = ''

                print(f"Season: {season}")
                print(f"Circuit: {circuit_name} ({circuit_id})")
                print(f"Date: {date} Time: {time}")
                print(f"Location: {locality}, {country} (Lat: {lat}, Long: {long})")
                print(f"Number: {number}")
                print(f"Position: {position} ({position_text})")
                print(f"Points: {points}")
                print(f"Driver: {driver_name} ({driver_id}), Nationality: {driver_nationality}")
                print(f"Constructor: {constructor_name} ({constructor_id}), Nationality: {constructor_nationality}")
                print(f"Grid: {constructor_grid}")
                print(f"Laps: {constructor_laps}")
                print(f"Status: {constructor_status}")
                print(f"Time: {time}")
                print(f"Fastest Lap: Rank: {fastest_lap_rank}, Lap: {fastest_lap_lap}")
                print(f"Average Speed: {average_speed_speed} {average_speed_units}")
                print("------------------------")