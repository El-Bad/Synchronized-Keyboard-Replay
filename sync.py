import ntplib
from datetime import datetime, timezone


def getNTPTime(timezone=timezone.utc):
    c = ntplib.NTPClient()
    response = c.request('time.windows.com', version=3)
    current_time = datetime.fromtimestamp(response.tx_time)
    return current_time.astimezone(timezone)
