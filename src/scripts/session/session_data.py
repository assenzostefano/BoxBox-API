import logging
import os

import fastf1
import pytz
from dotenv import load_dotenv

from src.scripts.general.ergast import Ergast
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
cache_directory = os.path.join(current_directory, '../../..', 'cache')

fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

# Funzione per salvare i risultati delle gare per un dato anno
def session_data(year, db):
    if year >= 2018:
        race_schedule = Ergast(year=year).race_schedule()
        max_race_number = len(race_schedule)

        sessions = ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'R']
        for i in range(1, max_race_number):
            for session_type in sessions:
                try:
                    session = fastf1.get_session(year, i, session_type)
                    session.load(weather=True, telemetry=True, messages=True, laps=True)

                    year = session.date.year
                    date = session.date
                    circuit_name = session.event['EventName']

                    latitude = race_schedule[0]['Location']['lat']  # Latitude of circuite
                    longitude = race_schedule[0]['Location']['long']  # Longitude of circuite
                    locality = race_schedule[0]['Location']['locality']  # Locality of circuite
                    country = race_schedule[0]['Location']['country']  # Country of circuite

                    start_time_session = session.t0_date  # Start time of session
                    start_time_session = start_time_session.tz_localize('UTC').tz_convert('Europe/Rome')

                    # Estrai l'orario
                    start_time_session = start_time_session.strftime("%H:%M:%S.%f")
                    total_laps = session.total_laps

                    session_status = session.session_status

                    weather_data = weather(session=session, session_type=session_type)

                    track_data = track(session=session, session_type=session_type)

                    cars_data = car(session=session, session_type=session_type)

                    lap_data = lap(session=session, session_type=session_type)

                except Exception as e:
                    print(e)
    else:
        ergast_data = Ergast(year=year).race_result()