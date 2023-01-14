import ntplib
from datetime import datetime, timedelta, timezone
import time


def getNTPTime(timezone=timezone.utc):
    c = ntplib.NTPClient()
    response = c.request('time.windows.com', version=3)
    current_time = datetime.fromtimestamp(response.tx_time)
    return current_time.astimezone(timezone)


def startAtUtc(input_time):
    current_time = getNTPTime()
    print("Current time (UTC):", current_time.strftime("%H:%M:%S %Y-%m-%d"))

    target_time = datetime.strptime(input_time, "%H:%M:%S")
    target_time = current_time.replace(hour=target_time.hour,
                                       minute=target_time.minute,
                                       second=target_time.second,
                                       microsecond=0)

    if target_time < getNTPTime():
        target_time += timedelta(days=1)

    # Sleep until target time
    sleep_time = (target_time - getNTPTime()).total_seconds()
    print("Starting in:", sleep_time, "seconds")
    time.sleep(sleep_time)
    print("Starting script at:", target_time)
