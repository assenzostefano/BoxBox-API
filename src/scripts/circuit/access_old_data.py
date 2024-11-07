from src.scripts.general.wikipedia_data import wikipedia_data
from src.scripts.general.ergast import Ergast

def circuit_1950_to_2017(year):
    ergast_data = Ergast.circuits_data(year)

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