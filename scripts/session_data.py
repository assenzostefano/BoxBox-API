import datetime
import logging
import os

import fastf1
import pandas as pd
import psycopg2
import pytz
import requests
from dotenv import load_dotenv

load_dotenv()

HOST_POSTGRESS = os.getenv('HOST_POSTGRESS')
PORT_POSTGRESS = os.getenv('PORT_POSTGRESS')
DB_POSTGRESS = os.getenv('DBNAME_POSTGRESS')
USER_POSTGRESS = os.getenv('USER_POSTGRESS')
PASSWORD_POSTGRESS = os.getenv('PASSWORD_POSTGRESS')

rome_tz = pytz.timezone('Europe/Rome')

fastf1.logger.set_log_level(logging.ERROR)  # optionally set log level to reduce output

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '..', 'cache')

fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

# Funzione per salvare i risultati delle gare per un dato anno
def save_race_results():
    conn = psycopg2.connect(
        host=HOST_POSTGRESS,
        port=PORT_POSTGRESS,
        database=DB_POSTGRESS,
        user=USER_POSTGRESS,
        password=PASSWORD_POSTGRESS,
        sslmode='require'
    )
    cur = conn.cursor()
    # Take current year
    current_year = datetime.datetime.now().year
    current_year += 1
    for year in range(1950, current_year):
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
                        session_data = fastf1.get_session(year, i, session)
                        session_data.load(weather=True, telemetry=True, messages=True, laps=True, )
                        name_session = session_data.name # e.g. 'FP1'
                        print(name_session)
                        circuit_name = session_data.event['EventName'] # e.g. 'Monaco Grand Prix'
                        print(circuit_name)
                        date = session_data.date.tz_localize(pytz.UTC).astimezone(rome_tz) # Start time of session
                        session_info = session_data.session_info # Session info e.g. {'Meeting': {'Key': 979, 'Name': 'Australian Grand Prix', 'Location': 'Melbourne', 'Country': {'Key': 5, 'Code': 'AUS', 'Name': 'Australia'}, 'Circuit': {'Key': 10, 'ShortName': 'Melbourne'}}, 'ArchiveStatus': {'Status': 'Generating'}, 'Key': 5067, 'Type': 'Practice', 'Number': 1, 'Name': 'Practice 1', 'StartDate': datetime.datetime(2018, 3, 23, 12, 0), 'EndDate': datetime.datetime(2018, 3, 23, 13, 30), 'GmtOffset': datetime.timedelta(seconds=39600), 'Path': '2018/2018-03-25_Australian_Grand_Prix/2018-03-23_Practice_1/'}
                        drivers = session_data.drivers # List of drivers
                        results = session_data.results # Final result session
                        total_laps = session_data.total_laps # Total laps of session
                        car_data = session_data.car_data # Car data (Speed, RPM, etc.)
                        pos_data = session_data.pos_data
                        session_status = session_data.session_status # Status session e.g. 'Finished'
                        track_status = session_data.track_status # Status track e.g. 'Green'
                        t0_date = session_data.t0_date # Start time of session
                        weather = session_data.weather_data
                        weather_time = weather['Time']
                        weather_air_temp = weather['AirTemp']
                        weather_track_temp = weather['TrackTemp']
                        weather_humidity = weather['Humidity']
                        weather_pressure = weather['Pressure']
                        weather_wind_speed = weather['WindSpeed']
                        weather_wind_direction = weather['WindDirection']
                        weather_rainfall = weather['Rainfall']
                        with open('data.txt', 'a') as r:
                            r.write("Year: " + str(year) + "\n")
                            r.write("Session: " + session + "\n")
                            r.write("Circuit Name: " + str(circuit_name) + "\n")
                        with open('data.txt', 'a') as r:
                            for j in range(0, len(weather_time)):
                                r.write("Time: " + str(weather_time[j]) + "\n")
                                r.write("AirTemp: " + str(weather_air_temp[j]) + "\n")
                                r.write("TrackTemp: " + str(weather_track_temp[j]) + "\n")
                                r.write("Humidity: " + str(weather_humidity[j]) + "\n")
                                r.write("Pressure: " + str(weather_pressure[j]) + "\n")
                                r.write("WindSpeed: " + str(weather_wind_speed[j]) + "\n")
                                r.write("WindDirection: " + str(weather_wind_direction[j]) + "\n")
                                r.write("Rainfall: " + str(weather_rainfall[j]) + "\n")
                                r.write("------------------------" + "\n")
                        
                        # Get laps data
                        laps_data = session_data.laps
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
                            with open('data.txt', 'a') as r:
                                r.write("Time: " + str(time) + "\n")
                                r.write("Driver: " + str(driver) + "\n")
                                r.write("DriverNumber: " + str(driver_number) + "\n")
                                r.write("LapTime: " + str(lap_time) + "\n")
                                r.write("LapNumber: " + str(lap_number) + "\n")
                                r.write("Stint: " + str(stint) + "\n")
                                r.write("PitOutTime: " + str(pit_out_time) + "\n")
                                r.write("PitInTime: " + str(pit_in_time) + "\n")
                                r.write("Sector1Time: " + str(sector1_time) + "\n")
                                r.write("Sector2Time: " + str(sector2_time) + "\n")
                                r.write("Sector3Time: " + str(sector3_time) + "\n")
                                r.write("Sector1SessionTime: " + str(sector1_session_time) + "\n")
                                r.write("Sector2SessionTime: " + str(sector2_session_time) + "\n")
                                r.write("Sector3SessionTime: " + str(sector3_session_time) + "\n")
                                r.write("SpeedI1: " + str(speedI1) + "\n")
                                r.write("SpeedI2: " + str(speedI2) + "\n")
                                r.write("SpeedFL: " + str(speedFL) + "\n")
                                r.write("SpeedST: " + str(speedST) + "\n")
                                r.write("IsPersonalBest: " + str(isPersonalBest) + "\n")
                                r.write("Compound: " + str(compound) + "\n")
                                r.write("TyreLife: " + str(tyrelife) + "\n")
                                r.write("FreshTyre: " + str(freshtyre) + "\n")
                                r.write("Team: " + str(team) + "\n")
                                r.write("LapStartTime: " + str(lap_start_time) + "\n")
                                r.write("LapStartDate: " + str(lap_start_date) + "\n")
                                r.write("TrackStatus: " + str(track_status) + "\n")
                                r.write("Position: " + str(position) + "\n")
                                r.write("Deleted: " + str(deleted) + "\n")
                                r.write("DeletedReason: " + str(deleted_reason) + "\n")
                                r.write("FastF1Generated: " + str(fastf1_generated) + "\n")
                                r.write("IsAccurate: " + str(isaccurate) + "\n")
                                r.write("------------------------" + "\n")
                        
                        # Get telemetry data and car data
                        telemetry_data = session_data.car_data
                        for car_number, car_data in telemetry_data.items():
                            with open('test.txt', 'a') as r:
                                print(f"Dati di telemetria per l'auto numero {car_number}:")
                                r.write(f"Dati di telemetria per l'auto numero {car_number}:\n")
                                # Converti i dati di telemetria in un DataFrame di Pandas
                                df = pd.DataFrame(car_data)

                                # Itera su ogni riga del DataFrame e stampa i dati
                                for index, row in df.iterrows():
                                        for field in ['Time', 'Speed', 'RPM', 'NGear', 'Throttle', 'Brake', 'DRS', 'X', 'Y', 'Z', 'Status', 'SessionTime', 'Date', 'Source']:
                                            if field in row:
                                                print(f"{field}: {row[field]}")
                                                r.write(f"{field}: {row[field]}\n")
                                            else:
                                                print(f"{field}: Non disponibile")
                                                r.write(f"{field}: Non disponibile\n")
                                        print("------------------------")  # Stampa una linea di separazione dopo ogni lista
                                print("========================")  # Stampa una linea di separazione dopo i dati di ogni auto
                        
                        continue
                    except Exception as e:
                        print(e)
                        continue

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

    cur.close()
    conn.close()

save_race_results()