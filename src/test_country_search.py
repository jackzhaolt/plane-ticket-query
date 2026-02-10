"""Test country-based search configuration."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from country_airports import (
    get_airports_for_country,
    get_airports_for_countries,
    expand_country_config
)


def main():
    """Test country-to-airport expansion."""
    print("\n" + "="*70)
    print("🌍 COUNTRY-BASED SEARCH CONFIGURATION TEST")
    print("="*70 + "\n")

    # Test 1: Single country
    print("Test 1: Single Country")
    print("-" * 70)

    us_airports = get_airports_for_country("US")
    print(f"US airports ({len(us_airports)}):")
    print(f"  {', '.join(us_airports)}\n")

    jp_airports = get_airports_for_country("JP")
    print(f"JP airports ({len(jp_airports)}):")
    print(f"  {', '.join(jp_airports)}\n")

    # Test 2: Multiple countries
    print("\nTest 2: Multiple Countries")
    print("-" * 70)

    asia_airports = get_airports_for_countries(["JP", "KR", "TW"])
    print(f"Asia airports (JP, KR, TW) - {len(asia_airports)} total:")
    print(f"  {', '.join(asia_airports)}\n")

    # Test 3: Configuration expansion
    print("\nTest 3: Configuration Expansion")
    print("-" * 70)

    print("Configuration:")
    print("  departure_countries: ['US']")
    print("  arrival_countries: ['JP', 'KR']\n")

    dep_airports, arr_airports = expand_country_config(
        departure_countries=["US"],
        arrival_countries=["JP", "KR"]
    )

    print(f"Expanded to {len(dep_airports)} departure × {len(arr_airports)} arrival airports:")
    print(f"\nDeparture airports ({len(dep_airports)}):")
    for i in range(0, len(dep_airports), 5):
        print(f"  {', '.join(dep_airports[i:i+5])}")

    print(f"\nArrival airports ({len(arr_airports)}):")
    print(f"  {', '.join(arr_airports)}")

    print(f"\nTotal route combinations: {len(dep_airports) * len(arr_airports)}")

    # Test 4: Mixed configuration (countries + specific airports)
    print("\n\nTest 4: Mixed Configuration")
    print("-" * 70)

    print("Configuration:")
    print("  departure_countries: ['US']")
    print("  departure_airports: ['YYZ']  # Add Toronto")
    print("  arrival_countries: ['JP']")
    print("  arrival_airports: ['TPE']  # Add Taipei\n")

    dep_airports, arr_airports = expand_country_config(
        departure_countries=["US"],
        arrival_countries=["JP"],
        departure_airports=["YYZ"],
        arrival_airports=["TPE"]
    )

    print(f"Expanded to {len(dep_airports)} departure × {len(arr_airports)} arrival airports:")
    print(f"  Departure: {len(dep_airports)} airports (US + YYZ)")
    print(f"  Arrival: {len(arr_airports)} airports (JP + TPE)")
    print(f"  Combinations: {len(dep_airports) * len(arr_airports)}")

    # Test 5: Real-world example
    print("\n\nTest 5: Real-World Example")
    print("-" * 70)

    configs = [
        {
            "name": "US → Asia",
            "dep_countries": ["US"],
            "arr_countries": ["JP", "KR", "TW", "SG"],
        },
        {
            "name": "North America → Europe",
            "dep_countries": ["US", "CA"],
            "arr_countries": ["GB", "FR", "DE", "NL"],
        },
        {
            "name": "US East Coast → Asia",
            "dep_airports": ["JFK", "EWR", "BOS", "IAD"],
            "arr_countries": ["JP", "KR"],
        },
    ]

    for config in configs:
        dep, arr = expand_country_config(
            departure_countries=config.get("dep_countries"),
            arrival_countries=config.get("arr_countries"),
            departure_airports=config.get("dep_airports"),
            arrival_airports=config.get("arr_airports")
        )

        print(f"\n{config['name']}:")
        print(f"  {len(dep)} departure airports × {len(arr)} arrival airports")
        print(f"  = {len(dep) * len(arr)} total route combinations")

    print("\n" + "="*70)
    print("✅ COUNTRY-BASED SEARCH READY!")
    print("="*70 + "\n")

    print("Benefits:")
    print("  ✓ Easy configuration (just specify countries)")
    print("  ✓ Comprehensive coverage (all major airports)")
    print("  ✓ Flexible (mix countries + specific airports)")
    print("  ✓ Scalable (add/remove countries easily)\n")

    print("Configuration example (config/settings.yaml):")
    print("""
search:
  departure_countries:
    - "US"
  arrival_countries:
    - "JP"
    - "KR"
  departure_airports: []  # Optional
  arrival_airports: []    # Optional
    """)


if __name__ == '__main__':
    main()
