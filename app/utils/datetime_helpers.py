from datetime import date, datetime, timedelta, timezone
import dateutil.relativedelta

def get_future_datetime(hours: int = 0, days: int = 0):
    return datetime.now(timezone.utc) + timedelta(hours=hours, days=days)

def get_current_datetime():
    return datetime.now(timezone.utc)

def get_past_datetime(hours: int = 0, days: int = 0) -> datetime:
    return datetime.now(timezone.utc) - timedelta(hours=hours, days=days)

def get_current_date() -> date:
    return datetime.now(timezone.utc).date()

def get_future_date(hours: int = 0, days: int = 0) -> date:
    return (datetime.now(timezone.utc) + timedelta(hours=hours, days=days)).date()

def get_past_date(hours: int = 0, days: int = 0, months: int = 0) -> date:
    current = datetime.now(timezone.utc).date()
    past = current - dateutil.relativedelta.relativedelta(hours=hours, days=days, months=months)
    return past