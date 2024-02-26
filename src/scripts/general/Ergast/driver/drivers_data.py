import os

import yukinator

current_directory = os.path.dirname(os.path.abspath(__file__))
cache_directory = os.path.join(current_directory, '../../../../../', 'cache')

y = yukinator.Yuki()
y = yukinator.Yuki(cache_dir=cache_directory, expires_after=9000, force_clear=True)

def drivers_data(year):
    data = y.get_drivers(year=year)
    return data

#print(drivers_data(year=2021)[0].dateOfBirth)