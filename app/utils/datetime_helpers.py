from datetime import datetime, timedelta, timezone

def get_future_datetime(hours: int = 0, days: int = 0):
    return datetime.now(timezone.utc) + timedelta(hours=hours, days=days)

def get_current_datetime():
    return datetime.now(timezone.utc)