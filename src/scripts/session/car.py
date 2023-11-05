def car(session, session_type):
    laps = session.laps
    for index, row in laps.iterrows():
        driver = row['Driver']
        telemetry = laps.pick_driver(driver)
        for i in telemetry.iterlaps():
            driver_telemetry = i[1].get_telemetry()  # https://docs.fastf1.dev/core.html#fastf1.core.Telemetry

    print("Laps data")