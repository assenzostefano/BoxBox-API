def weather(session, session_type):
    weather = session.weather_data  # Weather of session
    for j in range(0, len(weather)):
        weather_time = weather['Time']
        weather_air_temp = weather['AirTemp']
        weather_track_temp = weather['TrackTemp']
        weather_humidity = weather['Humidity']
        weather_pressure = weather['Pressure']
        weather_wind_speed = weather['WindSpeed']
        weather_wind_direction = weather['WindDirection']
        weather_rainfall = weather['Rainfall']

    print("Weather data")