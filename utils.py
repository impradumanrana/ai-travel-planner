from datetime import datetime


def validate_date(date_text: str):
    """
    Validate date format YYYY-MM-DD.
    """
    try:
        return datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")


def count_trip_days(start_date: str, end_date: str):
    start = validate_date(start_date)
    end = validate_date(end_date)

    if end < start:
        raise ValueError("End date cannot be before start date.")

    return (end - start).days + 1


def parse_trip_days(days_text: str, default: int = 5, max_days: int = 5):
    """
    Convert user input into a forecast-supported trip length.
    OpenWeather free 5-day forecast should not be treated like long-range planning.
    """
    if not days_text.strip():
        return default

    try:
        days = int(days_text)
    except ValueError:
        raise ValueError("Trip days must be a number, for example 3 or 5.")

    if days < 1:
        raise ValueError("Trip days must be at least 1.")

    if days > max_days:
        raise ValueError(f"This mini-project supports up to {max_days} days.")

    return days
