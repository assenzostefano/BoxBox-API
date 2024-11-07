import fastf1
import pandas as pd

year = int(2019)
session = fastf1.get_session(year, "1", "FP1")
session.load()

# Inizializza le liste per i dati
corners_data = []
marshal_lights_data = []
marshal_sectors_data = []

try:
    # Ottieni i dati del circuito
    session_data = session.get_circuit_info()
    
    # Verifica se i dati del circuito sono disponibili
    if session_data:
        corners = session_data.corners
        marshal_lights = session_data.marshal_lights
        marshal_sectors = session_data.marshal_sectors
        
        # Converti i dati in DataFrame di Pandas
        corners_df = pd.DataFrame(corners)
        marshal_lights_df = pd.DataFrame(marshal_lights)
        marshal_sectors_df = pd.DataFrame(marshal_sectors)
        
        # Stampa i dati ottenuti
        print("Curve del circuito:", corners_df)
        print("Luci dei Marshal:", marshal_lights_df)
        print("Settori del circuito:", marshal_sectors_df)
    else:
        print("Dati del circuito non disponibili.")
except Exception as e:
    print(f"Errore durante il caricamento dei dati del circuito: {e}")