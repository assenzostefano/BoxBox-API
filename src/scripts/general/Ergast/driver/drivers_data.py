import os

from fastf1.ergast import Ergast

current_directory = os.path.dirname(os.path.abspath(__file__))
cache_directory = os.path.join(current_directory, '../../../../../', 'cache')

ergast = Ergast()

def drivers_data(year, round, result_type):
    driver = ergast.get_driver_info(season=year, round=round, result_type=result_type)
    return driver