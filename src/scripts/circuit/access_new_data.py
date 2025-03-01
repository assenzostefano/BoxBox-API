import fastf1
import pandas as pd
import time
from src.scripts.circuit.access_old_data import circuit_1950_to_2017
from src.scripts.general.ergast import Ergast

def circuit_info(year, identifier, round):
    if year >= 2018:
        session = fastf1.get_session(year=year, gp=round, identifier='R')
        session.load()

        print("Round: " + str(round))

        try:
            circuit_info_gen = Ergast.circuits_data(year, round)
            circuit_info_spec = session.get_circuit_info().corners #Ghe se un problema con questo
            circuit_info = session.get_circuit_info()
            marshal_lights_df = circuit_info.marshal_lights
            marshal_sectors_df = circuit_info.marshal_sectors

            corners_list = []
            for i, row in circuit_info_spec.iterrows():
                corners_list.append({
                    "Corner Number": i,
                    "Corner Name": row['Number'],
                    "Corner Letter": row['Letter'],
                    "Corner Angle": row['Angle'],
                    "Corner Distance": row['Distance'],
                    "Coordinates": {"X": row["X"], "Y": row["Y"]}
                })
        
            marshal_lights = []
            for i, row in marshal_lights_df.iterrows():
                marshal_lights.append({
                    "Number": row['Number'],
                    "Coordinates": {"X": row["X"], "Y": row["Y"]}
                })
        
            marshal_sectors = []
            for i, row in marshal_sectors_df.iterrows():
                marshal_sectors.append({
                    "Number": row['Number'],
                    "Coordinates": {"X": row["X"], "Y": row["Y"]},
                })


            circuit_data = {
                "_id": circuit_info_gen[0]['circuitId'],
                "Circuit Name": circuit_info_gen[0]["circuitName"],
                "Circuit URL": circuit_info_gen[0]["circuitUrl"],
                "Wikipedia Data": [
                "TODO: Wikipedia Data"
                ],
                "Location": {
                "Latitude": circuit_info_gen[0]['Location']["lat"],
                "Longitude": circuit_info_gen[0]['Location']["long"],
                "Locality": circuit_info_gen[0]['Location']["locality"],
                "Country": circuit_info_gen[0]['Location']["country"]
                },
                "Years": {
                    str(year): {
                        "Corners": corners_list,
                        "Marshal Lights": marshal_lights,
                        "Marshal Sectors": marshal_sectors,
                    }
                }
            }
    
            return circuit_data
        except Exception as e:
            print(e)
            return None

    else:
        circuit_data_list = circuit_1950_to_2017(year)
        return circuit_data_list