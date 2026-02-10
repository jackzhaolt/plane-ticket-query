"""Mapping of countries to their major airports for flexible search configuration."""

from typing import Dict, List

# Country to airports mapping
COUNTRY_AIRPORTS: Dict[str, List[str]] = {
    # United States
    "US": [
        # East Coast
        "JFK", "EWR", "LGA",  # New York area
        "BOS",  # Boston
        "PHL",  # Philadelphia
        "IAD", "DCA",  # Washington DC
        "ATL",  # Atlanta
        "MIA",  # Miami
        "MCO",  # Orlando

        # West Coast
        "LAX",  # Los Angeles
        "SFO",  # San Francisco
        "SEA",  # Seattle
        "PDX",  # Portland
        "SAN",  # San Diego

        # Central
        "ORD",  # Chicago
        "DFW",  # Dallas
        "IAH",  # Houston
        "DEN",  # Denver
        "PHX",  # Phoenix
        "LAS",  # Las Vegas
    ],

    # Canada
    "CA": [
        "YYZ",  # Toronto
        "YVR",  # Vancouver
        "YUL",  # Montreal
        "YYC",  # Calgary
    ],

    # Japan
    "JP": [
        "NRT",  # Tokyo Narita
        "HND",  # Tokyo Haneda
        "KIX",  # Osaka
        "NGO",  # Nagoya
        "FUK",  # Fukuoka
    ],

    # South Korea
    "KR": [
        "ICN",  # Seoul Incheon
        "GMP",  # Seoul Gimpo
    ],

    # Taiwan
    "TW": [
        "TPE",  # Taipei
    ],

    # China
    "CN": [
        "PVG",  # Shanghai Pudong
        "PEK",  # Beijing
        "CAN",  # Guangzhou
        "HKG",  # Hong Kong
    ],

    # Hong Kong (separate)
    "HK": [
        "HKG",  # Hong Kong
    ],

    # Singapore
    "SG": [
        "SIN",  # Singapore
    ],

    # Thailand
    "TH": [
        "BKK",  # Bangkok
        "HKT",  # Phuket
    ],

    # India
    "IN": [
        "DEL",  # Delhi
        "BOM",  # Mumbai
        "BLR",  # Bangalore
    ],

    # United Kingdom
    "GB": [
        "LHR",  # London Heathrow
        "LGW",  # London Gatwick
        "MAN",  # Manchester
    ],

    # France
    "FR": [
        "CDG",  # Paris
        "ORY",  # Paris Orly
    ],

    # Germany
    "DE": [
        "FRA",  # Frankfurt
        "MUC",  # Munich
    ],

    # Netherlands
    "NL": [
        "AMS",  # Amsterdam
    ],

    # Spain
    "ES": [
        "MAD",  # Madrid
        "BCN",  # Barcelona
    ],

    # Italy
    "IT": [
        "FCO",  # Rome
        "MXP",  # Milan
    ],

    # Switzerland
    "CH": [
        "ZRH",  # Zurich
    ],

    # Australia
    "AU": [
        "SYD",  # Sydney
        "MEL",  # Melbourne
        "BNE",  # Brisbane
    ],

    # New Zealand
    "NZ": [
        "AKL",  # Auckland
    ],

    # UAE
    "AE": [
        "DXB",  # Dubai
        "AUH",  # Abu Dhabi
    ],

    # Qatar
    "QA": [
        "DOH",  # Doha
    ],

    # Brazil
    "BR": [
        "GRU",  # Sao Paulo
        "GIG",  # Rio de Janeiro
    ],

    # Argentina
    "AR": [
        "EZE",  # Buenos Aires
    ],

    # Mexico
    "MX": [
        "MEX",  # Mexico City
        "CUN",  # Cancun
    ],
}


def get_airports_for_country(country_code: str) -> List[str]:
    """
    Get list of airports for a country code.

    Args:
        country_code: 2-letter ISO country code (e.g., "US", "JP")

    Returns:
        List of airport codes for that country
    """
    return COUNTRY_AIRPORTS.get(country_code.upper(), [])


def get_airports_for_countries(country_codes: List[str]) -> List[str]:
    """
    Get list of airports for multiple countries.

    Args:
        country_codes: List of 2-letter ISO country codes

    Returns:
        Combined list of airport codes (deduplicated)
    """
    airports = []
    for country_code in country_codes:
        airports.extend(get_airports_for_country(country_code))

    # Remove duplicates while preserving order
    seen = set()
    result = []
    for airport in airports:
        if airport not in seen:
            seen.add(airport)
            result.append(airport)

    return result


def expand_country_config(
    departure_countries: List[str] = None,
    arrival_countries: List[str] = None,
    departure_airports: List[str] = None,
    arrival_airports: List[str] = None
) -> tuple:
    """
    Expand country codes to airports, combining with any explicitly specified airports.

    Args:
        departure_countries: List of departure country codes
        arrival_countries: List of arrival country codes
        departure_airports: List of explicit departure airports
        arrival_airports: List of explicit arrival airports

    Returns:
        Tuple of (departure_airports_list, arrival_airports_list)
    """
    # Start with explicitly specified airports
    dep_airports = list(departure_airports or [])
    arr_airports = list(arrival_airports or [])

    # Add airports from countries
    if departure_countries:
        dep_airports.extend(get_airports_for_countries(departure_countries))

    if arrival_countries:
        arr_airports.extend(get_airports_for_countries(arrival_countries))

    # Deduplicate
    dep_airports = list(dict.fromkeys(dep_airports))  # Preserves order
    arr_airports = list(dict.fromkeys(arr_airports))

    return dep_airports, arr_airports


def add_country(country_code: str, airports: List[str]):
    """
    Add a new country to the mapping.

    Args:
        country_code: 2-letter ISO country code
        airports: List of airport codes for that country
    """
    COUNTRY_AIRPORTS[country_code.upper()] = airports


# Example usage
if __name__ == "__main__":
    print("Country-to-Airport Mapping Examples")
    print("="*60)

    # Example 1: Single country
    print("\nUS airports:")
    us_airports = get_airports_for_country("US")
    print(f"  {len(us_airports)} airports: {', '.join(us_airports[:5])}...")

    # Example 2: Multiple countries
    print("\nAsian airports (JP, KR, TW):")
    asia_airports = get_airports_for_countries(["JP", "KR", "TW"])
    print(f"  {len(asia_airports)} airports: {', '.join(asia_airports)}")

    # Example 3: Expansion
    print("\nExpanding configuration:")
    print("  departure_countries: ['US']")
    print("  arrival_countries: ['JP', 'KR']")

    dep, arr = expand_country_config(
        departure_countries=["US"],
        arrival_countries=["JP", "KR"]
    )

    print(f"\nExpanded to:")
    print(f"  Departure airports ({len(dep)}): {', '.join(dep[:5])}...")
    print(f"  Arrival airports ({len(arr)}): {', '.join(arr)}")
    print(f"\nTotal route combinations: {len(dep)} × {len(arr)} = {len(dep) * len(arr)}")
