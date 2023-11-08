import os

import fastf1

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '../../..', 'cache')

fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

def circuit_info(year, db):
    return None