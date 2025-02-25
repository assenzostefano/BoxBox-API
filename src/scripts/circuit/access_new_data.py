import fastf1
import pandas as pd
import time
from src.scripts.circuit.access_old_data import circuit_1950_to_2017
from src.scripts.general.ergast import Ergast

def circuit_info(year, identifier, round):
    if year >= 2018:
        session = fastf1.get_session(year=year, gp=round, identifier='FP1')
        session.load()

        try:
            circuit_info_gen = Ergast.circuits_data(year)
            circuit_info_spec = session.get_circuit_info() #Ghe se un problema con questo
            
            circuit_data = {
                "_id": circuit_info_gen["circuitId"],
                "Circuit Name": circuit_info_gen["circuitName"],
                "Circuit URL": circuit_info_gen["circuitUrl"],

                "Wikipedia Data": [
                    "TODO: Wikipedia Data"
                ],

                "Location": {
                    "Latitude": circuit_info_gen["lat"],
                    "Longitude": circuit_info_gen["long"],
                    "Locality": circuit_info_gen["locality"],
                    "Country": circuit_info_gen["country"]
                },

                "Years": {
                    year: {
                        "Rotation": circuit_info_spec.rotation,
                        "Corners": [
                            {
                                "Corner Number": i,
                                "Corner Name": circuit_info_spec.corners[i],
                                "Corner Type": circuit_info_spec.corner_types[i],
                                "Corner Coordinates": {
                                    "Latitude": circuit_info_spec.corner_latitudes[i],
                                    "Longitude": circuit_info_spec.corner_longitudes[i]
                                },
                            } for i in range(len(circuit_info_spec.corners))
                        ],
                    },
                },
            }
    

            return circuit_data
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