import fastf1
import pandas as pd
import time
from src.scripts.circuit.access_old_data import circuit_1950_to_2017

def circuit_info(year, identifier, round):
    if year >= 2018:
        session = fastf1.get_session(year=2019, gp=1, identifier='FP1')
        session.load()

        print("DAJE ROMA DAJE")
        try:
            session_data = session.get_circuit_info() #Ghe se un problema con questo
            print(session_data)
        except Exception as e:
            print(e)
        #if session_data:
        #    print(session_data)
        #    corners = session_data.corners
        #    marshal_lights = session_data.marshal_lights
        #    marshal_sectors = session_data.marshal_sectors
#
        #    # Converti i dati in DataFrame di Pandas
        #    corners_df = pd.DataFrame(corners)
        #    marshal_lights_df = pd.DataFrame(marshal_lights)
        #    marshal_sectors_df = pd.DataFrame(marshal_sectors)

    else:
        circuit_data_list = circuit_1950_to_2017(year)
        return circuit_data_list