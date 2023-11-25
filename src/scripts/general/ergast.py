from src.scripts.general.Ergast.circuit.circuits_data import circuits_data
from src.scripts.general.Ergast.race.race_result import race_result
from src.scripts.general.Ergast.race.race_schedule import race_schedule


class Ergast:
    def circuits_data(year):
        data = circuits_data(year=year)
        return data

    def race_result(year):
        data = race_result(year=year)
        return data

    def race_schedule(year):
        data = race_schedule(year=year)
        return data


