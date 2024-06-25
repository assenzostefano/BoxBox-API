import threading
import time

from src.database.database import database
from src.scripts.circuit.circuit_info import circuit_info
from src.scripts.constructor.constructor_info import constructor_info
from src.scripts.driver.driver_info import driver_info
from src.scripts.general.ergast import Ergast


def start():
    identifier = ['FP1']
    print("Starting...")

    # Driver data
    for i in range(1950, 2023):
        identifier = ['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'R']
        for a in identifier:
            for b in range(1, 50):
                print("Year: " + str(i) + " Identifier: " + str(a) + " Round: " + str(b))
                time.sleep(2)
                driver = driver_info(year=i, identifier=a, round=b)
                print(driver)

                if driver == None:
                    break
                else:
                    t = threading.Thread(target=database, args=(driver, 'Years', 'drivers', '_id')).start()

    # Circuit data
    for i in range(1950, 2024):
        print("Year: " + str(i))
        data_circuit = Ergast.circuits_data(year=i)
        if i <= 2017:
            time.sleep(5)
            circuit = circuit_info(year=i, identifier="", round="", ergast_data=data_circuit)
            t = threading.Thread(target=database, args=(circuit, 'Years', 'circuits', '_id')).start()
        else:
            for a in identifier:
                for b in range(1, 50):
                    try:
                        time.sleep(5)
                        circuit_data = circuit_info(year=i, identifier=a, round=b, ergast_data=data_circuit)
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