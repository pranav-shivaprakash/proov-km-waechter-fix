# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Cleaned up 2024.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: int | float, interval: int | float) -> float:
    """Return the percentage of the service interval that has been used up."""
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True when a car has consumed at least WARN_AT_PERCENT of its service interval.

    If the car has no recorded last-service reading, km_since is treated as 0
    (we cannot tell how far it has driven since service, so we do not flag it).
    """
    last = car.get("last_service_km", car["odometer"])  # unknown → assume just serviced
    km_since = car["odometer"] - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list:
    """Return the IDs of all cars that are due for service and print each one."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
