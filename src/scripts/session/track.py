def track(session, session_type):
    track_status = session.track_status  # Track status of session
    for i in range(0, len(track_status)):
        track_status_time = track_status['Time']
        track_status_status = track_status['Status']
        track_status_message = track_status['Message']

    print("Track status data")