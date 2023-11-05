import logging
import os
import threading

import fastf1
import pytz
import requests
from dotenv import load_dotenv
from fastf1.ergast import Ergast

from src.scripts.session.car import car
from src.scripts.session.lap import lap
from src.scripts.session.track import track
from src.scripts.session.weather import weather

load_dotenv()

rome_tz = pytz.timezone('Europe/Rome')

fastf1.logger.set_log_level(logging.ERROR)  # optionally set log level to reduce output

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '../..', 'cache')

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

        sessions = ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'R']
        for i in range(1, max_race_number):
            for session_type in sessions:
                try:
                    session = fastf1.get_session(year, i, session_type)
                    session.load(weather=True, telemetry=True, messages=True, laps=True)

                    year = session.date.year
                    date = session.date
                    circuit_name = session.event['EventName']

                    latitude = api.get_circuits(season=year, round=i, result_type='raw', auto_cast=False)[0]['Location']['lat']  # Latitude of circuite
                    longitude = api.get_circuits(season=year, round=i, result_type='raw', auto_cast=False)[0]['Location']['long']  # Longitude of circuite
                    locality = api.get_circuits(season=year, round=i, result_type='raw', auto_cast=False)[0]['Location']['locality']  # Locality of circuite
                    country = api.get_circuits(season=year, round=i, result_type='raw', auto_cast=False)[0]['Location']['country']  # Country of circuite

                    start_time_session = session.t0_date  # Start time of session
                    start_time_session = start_time_session.tz_localize('UTC').tz_convert('Europe/Rome')

                    # Estrai l'orario
                    start_time_session = start_time_session.strftime("%H:%M:%S.%f")
                    total_laps = session.total_laps

                    session_status = session.session_status

                    weather_data = threading.Thread(target=weather, args=(session, session_type)).start()

                    track_data = threading.Thread(target=track, args=(session, session_type)).start()

                    cars_data = threading.Thread(target=car, args=(session, session_type)).start()

                    lap_data = threading.Thread(target=lap, args=(session, session_type)).start()

                except Exception as e:
                    print(e)
    else:
        ergast = Ergast(result_type='pandas', auto_cast=True)

        seasons = ergast.get_race_results(season=2021, limit=10)

        for i in seasons.content:
