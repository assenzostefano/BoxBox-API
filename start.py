import threading
import time
import fastf1

from fastf1.core import DataNotLoadedError

from src.database.database import database
from src.scripts.circuit.access_new_data import circuit_info
from src.scripts.constructor.constructor_info import constructor_info
from src.scripts.driver.driver_info import driver_info
from src.scripts.driver.driver_info import get_data
from src.scripts.general.ergast import Ergast


def start():
    identifier = ['FP1']
    print("Starting...")

    # TODO: Driver data
    #for i in range(1950, 2023):
    #    identifier = ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'R']
    #    for a in identifier:
    #        for b in range(1, 50):
    #            print("Year: " + str(i) + " Identifier: " + str(a) + " Round: " + str(b))
    #            time.sleep(2)
    #            driver = driver_info(year=i, identifier=a, round=b)
#
    #            if driver == None:
    #                try:
    #                    print("Sto qua")
    #                    time.sleep(2)
    #                    session = fastf1.get_session(year=i, gp=b, identifier=a)
    #                    session.load(telemetry=True)
    #                    driver_pick = session.drivers
    #                    print(driver_pick[0])
    #                    driver = session.get_driver(driver_pick[0])
    #                except DataNotLoadedError as e:
    #                    print(f"DataNotLoadedError: " + {e})
    #                except Exception as e:
    #                    if str(e) == "Failed to load any schedule data.":
    #                        time.sleep(20)
    #                        session = fastf1.get_session(year=i, gp=b, identifier=a)
    #                        session.load(telemetry=True)
    #                        driver_pick = session.drivers
    #                        print(driver_pick[0])
    #                        driver = session.get_driver(driver_pick[0])
    #                        driver = driver_info(year=i, identifier=a, round=b)
    #                    else:
    #                        print("NOPE")
    #                        break
    #            else:
    #                print("djasidjiasdjsaijds")
    #                t = threading.Thread(target=database, args=(driver, 'Years', 'drivers', '_id')).start()

    # Circuit data
    for i in range(2019, 2024):
        print("Year: " + str(i))
        if i <= 2017:
            circuit = circuit_info(year=i, identifier="FP1", round=1)
            t = threading.Thread(target=database, args=(circuit, 'Years', 'circuits', '_id')).start()
        else:
            for a in identifier:
                for b in range(1, 50):
                    try:
                        circuit_data = circuit_info(year=i, identifier="FP1", round=1)
                        print(list(circuit_data))
                        if circuit_data == None:
                            continue
                        else:
                            t = threading.Thread(target=database, args=(circuit_data, 'Years', 'circuits', '_id')).start()
                    except Exception as e:
                        print("Error: " + str(e))
    print("Finito")

    # Constructor data
    for i in range(1950, 2023):
        for a in identifier:
            for b in range(1, 50):
                #data = fastf1.get_session(i, b, a)
                constructor = constructor_info(year=i, db=db)

    # Session data
    for i in range(1950, 2023):
        for a in identifier:
            for b in range(1, 50):
                print("Eccomi")
                #session = session_data(year=i, db=db)

start()