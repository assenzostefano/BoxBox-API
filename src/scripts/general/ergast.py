from src.scripts.general.Ergast.circuit.circuits_data import circuits_data
from src.scripts.general.Ergast.driver.drivers_data import drivers_data
from src.scripts.general.Ergast.race.race_schedule import race_schedule
from src.scripts.general.Ergast.race.race_result import race_result


class Ergast:
    def circuits_data(year, round):
        data = circuits_data(year=year, round=round)
        return data

    def race_result(year):
        data = race_result(year=year)
        return data

    def race_schedule(year):
        data = race_schedule(year=year)
        return data

    def drivers_data(year, round, result_type):
        data = drivers_data(year, round, result_type)
        return data