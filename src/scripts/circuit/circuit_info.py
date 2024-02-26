import logging
import os

import fastf1
import pandas as pd

from src.scripts.general.wikipedia_data import wikipedia_data

fastf1.logger.set_log_level(logging.ERROR)  # optionally set log level to reduce output

# Ottieni il percorso della cartella corrente
current_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso della cartella di cache relativo al percorso corrente
cache_directory = os.path.join(current_directory, '../../..', 'cache')

fastf1.Cache.enable_cache(cache_directory)  # optionally change cache location

def circuit_info(year, identifier, round, ergast_data):
    if year >= 2018:
        try:
            corners_data = []
            marshal_lights_data = []
            marshal_sectors_data = []
            print("Round: " + str(round) + " Identifier: " + identifier + " Year: " + str(year))

            try:
                session = fastf1.get_session(year, round, identifier)

                session.load(laps=True, telemetry=True, weather=True, messages=True, livedata=True)
            except:
                session = fastf1.get_session(year=year, gp=round, identifier='FP2')
                session.load(laps=True, telemetry=True, weather=True, messages=True, livedata=True)

            session_data = session.get_circuit_info()
            corners = session_data.corners
            marshal_lights = session_data.marshal_lights
            marshal_sectors = session_data.marshal_sectors
            rotation = session_data.rotation

            corners = pd.DataFrame(corners)
            marshal_lights = pd.DataFrame(marshal_lights)
            marshal_sectors = pd.DataFrame(marshal_sectors)
            for index, row in corners.iterrows():
                X = row['X']
                Y = row['Y']
                number = row['Number']
                letter = row['Letter']
                angle = row['Angle']
                distance = row['Distance']
                corners_data.append(
                    {
                        'X': X,
                        'Y': Y,
                        'Number': number,
                        'Letter': letter,
                        'Angle': angle,
                        'Distance': distance
                    }
                )
            for index, row in marshal_lights.iterrows():
                X = row['X']
                Y = row['Y']
                number = row['Number']
                letter = row['Letter']
                angle = row['Angle']
                distance = row['Distance']
                marshal_lights_data.append(
                    {
                        'X': X,
                        'Y': Y,
                        'Number': number,
                        'Letter': letter,
                        'Angle': angle,
                        'Distance': distance
                    }
                )
            for index, row in marshal_sectors.iterrows():
                X = row['X']
                Y = row['Y']
                number = row['Number']
                letter = row['Letter']
                angle = row['Angle']
                distance = row['Distance']
                marshal_sectors_data.append(
                    {
                        'X': X,
                        'Y': Y,
                        'Number': number,
                        'Letter': letter,
                        'Angle': angle,
                        'Distance': distance
                    }
                )

            circuit_data_list = []
            for count in range(0, len(ergast_data)):
                circuit_data_dict = {
                    "_id": ergast_data[count]['circuitId'],
                    "Circuit Name": ergast_data[count]['circuitName'],
                    "Circuit URL": ergast_data[count]['circuitUrl'],
                    "Wikipedia Data": wikipedia_data(url_wikipedia=ergast_data[count]['circuitUrl']),
                    "Location": {
                        "Latitude": ergast_data[count]['Location']['lat'],
                        "Longitude": ergast_data[count]['Location']['long'],
                        "Locality": ergast_data[count]['Location']['locality'],
                        "Country": ergast_data[count]['Location']['country'],
                    },
                    "Years": {
                        str(year): {
                            "Rotation": rotation,
                            "Corners": corners_data,
                            "Marshal Lights": marshal_lights_data,
                            "Marshal Sectors": marshal_sectors_data
                        }
                    }
                }

                circuit_data_list.append(circuit_data_dict)

            return circuit_data_list

        except Exception as error:
            print("Error: " + str(error))
            return None
            #circuit_data_list = []
            #for count in range(0, len(ergast_data)):
            #    circuit_data_dict = {
            #        "_id": ergast_data[count]['circuitId'],
            #        "Circuit Name": ergast_data[count]['circuitName'],
            #        "Circuit URL": ergast_data[count]['circuitUrl'],
            #        "Wikipedia Data": wikipedia_data(url_wikipedia=ergast_data[count]['circuitUrl']),
            #        "Location": {
            #            "Latitude": ergast_data[count]['Location']['lat'],
            #            "Longitude": ergast_data[count]['Location']['long'],
            #            "Locality": ergast_data[count]['Location']['locality'],
            #            "Country": ergast_data[count]['Location']['country'],
            #        },
            #        "Years": {
            #            str(year): {
            #                "Rotation": "",
            #                "Corners": [],
            #                "Marshal Lights": [],
            #                "Marshal Sectors": []
            #            }
            #        }
            #    }
#
            #    circuit_data_list.append(circuit_data_dict)
            #return circuit_data_list

    else:
        print("Round: " + str(round) + " Identifier: " + identifier + " Year: " + str(year))
        circuit_data_list = []
        for count in range(0, len(ergast_data)):
            circuit_data_dict = {
                "_id": ergast_data[count]['circuitId'],
                "Circuit Name": ergast_data[count]['circuitName'],
                "Circuit URL": ergast_data[count]['circuitUrl'],
                "Wikipedia Data": wikipedia_data(url_wikipedia=ergast_data[count]['circuitUrl']),
                "Location": {
                    "Latitude": ergast_data[count]['Location']['lat'],
                    "Longitude": ergast_data[count]['Location']['long'],
                    "Locality": ergast_data[count]['Location']['locality'],
                    "Country": ergast_data[count]['Location']['country'],
                },
                "Years": {
                    str(year): {
                        "Rotation": "",
                        "Corners": [],
                        "Marshal Lights": [],
                        "Marshal Sectors": []
                    }
                }
            }

            circuit_data_list.append(circuit_data_dict)

        return circuit_data_list