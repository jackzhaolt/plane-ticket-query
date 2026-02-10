"""Calculate flight distances for deal evaluation."""

from math import radians, sin, cos, sqrt, atan2
from typing import Dict


# Airport coordinates database (lat, lon)
AIRPORT_COORDINATES: Dict[str, tuple] = {
    # US East Coast
    "JFK": (40.6413, -73.7781),
    "EWR": (40.6895, -74.1745),
    "LGA": (40.7769, -73.8740),
    "BOS": (42.3656, -71.0096),
    "PHL": (39.8729, -75.2437),
    "IAD": (38.9531, -77.4565),
    "DCA": (38.8512, -77.0402),
    "ATL": (33.6407, -84.4277),
    "MIA": (25.7959, -80.2870),

    # US West Coast
    "LAX": (33.9416, -118.4085),
    "SFO": (37.6213, -122.3790),
    "SEA": (47.4502, -122.3088),
    "PDX": (45.5898, -122.5951),
    "SAN": (32.7338, -117.1933),

    # US Central
    "ORD": (41.9742, -87.9073),
    "DFW": (32.8998, -97.0403),
    "IAH": (29.9902, -95.3368),
    "DEN": (39.8561, -104.6737),
    "PHX": (33.4352, -112.0101),

    # Asia - Japan
    "NRT": (35.7653, 140.3854),
    "HND": (35.5494, 139.7798),
    "KIX": (34.4273, 135.2440),

    # Asia - Other
    "TPE": (25.0777, 121.2328),  # Taipei
    "ICN": (37.4602, 126.4407),  # Seoul
    "PVG": (31.1443, 121.8083),  # Shanghai
    "HKG": (22.3080, 113.9185),  # Hong Kong
    "SIN": (1.3644, 103.9915),   # Singapore
    "BKK": (13.6900, 100.7501),  # Bangkok
    "DEL": (28.5562, 77.1000),   # Delhi

    # Europe
    "LHR": (51.4700, -0.4543),   # London
    "CDG": (49.0097, 2.5479),    # Paris
    "FRA": (50.0379, 8.5622),    # Frankfurt
    "AMS": (52.3086, 4.7639),    # Amsterdam
    "MAD": (40.4983, -3.5676),   # Madrid
    "FCO": (41.8003, 12.2389),   # Rome
    "MUC": (48.3537, 11.7750),   # Munich
    "ZRH": (47.4647, 8.5492),    # Zurich

    # Oceania
    "SYD": (-33.9399, 151.1753),  # Sydney
    "MEL": (-37.6690, 144.8410),  # Melbourne
    "AKL": (-37.0082, 174.7850),  # Auckland

    # Middle East
    "DXB": (25.2532, 55.3657),   # Dubai
    "DOH": (25.2731, 51.6080),   # Doha
    "AUH": (24.4330, 54.6511),   # Abu Dhabi

    # South America
    "GRU": (-23.4356, -46.4731),  # Sao Paulo
    "EZE": (-34.8222, -58.5358),  # Buenos Aires
    "LIM": (-12.0219, -77.1143),  # Lima
}


def get_airport_coordinates(airport_code: str) -> tuple:
    """
    Get coordinates for an airport.

    Args:
        airport_code: 3-letter IATA code

    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    return AIRPORT_COORDINATES.get(airport_code.upper())


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great circle distance between two points using Haversine formula.

    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates

    Returns:
        Distance in miles
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    # Earth's radius in miles
    radius_miles = 3959

    return radius_miles * c


def get_flight_distance(departure_airport: str, arrival_airport: str) -> float:
    """
    Get distance between two airports in miles.

    Args:
        departure_airport: 3-letter IATA code
        arrival_airport: 3-letter IATA code

    Returns:
        Distance in miles, or 0 if airports not found
    """
    dep_coords = get_airport_coordinates(departure_airport)
    arr_coords = get_airport_coordinates(arrival_airport)

    if not dep_coords or not arr_coords:
        # If airports not in database, return 0
        # In production, you might want to call an external API
        return 0

    return calculate_distance(
        dep_coords[0], dep_coords[1],
        arr_coords[0], arr_coords[1]
    )


def add_airport(code: str, latitude: float, longitude: float):
    """
    Add an airport to the database.

    Args:
        code: 3-letter IATA code
        latitude: Latitude in degrees
        longitude: Longitude in degrees
    """
    AIRPORT_COORDINATES[code.upper()] = (latitude, longitude)


# Example usage
if __name__ == "__main__":
    # Test some common routes
    routes = [
        ("JFK", "NRT", "New York to Tokyo"),
        ("LAX", "HKG", "Los Angeles to Hong Kong"),
        ("SFO", "SIN", "San Francisco to Singapore"),
        ("ORD", "LHR", "Chicago to London"),
        ("MIA", "GRU", "Miami to Sao Paulo"),
    ]

    print("Flight Distance Examples:")
    print("="*60)

    for dep, arr, name in routes:
        distance = get_flight_distance(dep, arr)
        print(f"{name:40} {distance:,.0f} miles")
