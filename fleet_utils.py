# fleet_utils.py
# Catch-all helpers since 2013.

MILES_PER_KM = 0.621371   # 1 km = 0.621371 miles (was 1.609, which is km-per-mile — inverted)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles.

    Used by the nightly run for the UK partner report.
    """
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a float as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list) -> float:
    """Return the arithmetic mean of a list of numbers, or 0 for an empty list.

    statistics.mean has existed since Python 3.4; this predates that.
    """
    if not values:
        return 0
    return sum(values) / len(values)


def is_due(pct: float, threshold: float) -> bool:
    """Return True when pct has reached or exceeded threshold."""
    return pct >= threshold


def parse_service_date(text: str) -> tuple | None:
    """Parse a DD.MM.YYYY string into a (year, month, day) tuple.

    Returns None when the format does not match.
    Was used for the old garage form (2014); the form no longer exists.
    """
    parts = text.split(".")
    if len(parts) != 3:
        return None
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    return (year, month, day)


def chunk_list(items: list, size: int) -> list:
    """Split a list into chunks of at most *size* elements.

    Copied from Stack Overflow in 2013; no longer called from anywhere.
    """
    chunks = []
    current: list = []
    for item in items:
        current.append(item)
        if len(current) == size:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks
