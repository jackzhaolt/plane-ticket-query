"""Test distance calculations and deal detection with distance metrics."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date, timedelta
from random import randint, choice
from searchers.base import Flight
from deal_detector import DealDetector
from distance_calculator import get_flight_distance
import yaml


def test_distances():
    """Test distance calculations for common routes."""
    print("\n" + "="*60)
    print("✈️  FLIGHT DISTANCE CALCULATIONS")
    print("="*60 + "\n")

    routes = [
        ("JFK", "NRT", "New York → Tokyo"),
        ("JFK", "LHR", "New York → London"),
        ("LAX", "HKG", "Los Angeles → Hong Kong"),
        ("SFO", "SIN", "San Francisco → Singapore"),
        ("ORD", "CDG", "Chicago → Paris"),
        ("MIA", "GRU", "Miami → São Paulo"),
    ]

    for dep, arr, name in routes:
        distance = get_flight_distance(dep, arr)
        print(f"{name:35} {distance:>7,.0f} miles")


def test_deal_detection():
    """Test deal detection with distance-based metrics."""
    print("\n" + "="*60)
    print("💰 DEAL DETECTION WITH DISTANCE METRICS")
    print("="*60 + "\n")

    # Load config
    with open('config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)

    deal_detector = DealDetector(config['deals'])

    # Create test flights with realistic data
    test_flights = [
        # EXCEPTIONAL DEAL: Long-haul for reasonable points
        Flight(
            departure_airport="JFK",
            arrival_airport="NRT",
            departure_date=date.today() + timedelta(days=60),
            return_date=None,
            price_usd=650,
            points=45000,  # ~6,800 miles / 45k points = 0.15 miles/point
            airline="NH",
            cabin_class="ECONOMY",
            stops=0
        ),

        # GOOD DEAL: Long-haul, slightly more points
        Flight(
            departure_airport="JFK",
            arrival_airport="NRT",
            departure_date=date.today() + timedelta(days=60),
            return_date=None,
            price_usd=720,
            points=60000,  # ~6,800 miles / 60k points = 0.11 miles/point
            airline="DL",
            cabin_class="ECONOMY",
            stops=1
        ),

        # POOR DEAL: Short domestic for too many points
        Flight(
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_date=date.today() + timedelta(days=60),
            return_date=None,
            price_usd=350,
            points=50000,  # ~2,500 miles / 50k points = 0.05 miles/point
            airline="AA",
            cabin_class="ECONOMY",
            stops=0
        ),

        # EXCELLENT: Business class long-haul
        Flight(
            departure_airport="SFO",
            arrival_airport="SIN",
            departure_date=date.today() + timedelta(days=90),
            return_date=None,
            price_usd=3500,
            points=85000,  # ~8,400 miles / 85k points = 0.10 miles/point
            airline="SQ",
            cabin_class="BUSINESS",
            stops=0
        ),
    ]

    print("Analyzing flights:\n")

    for i, flight in enumerate(test_flights, 1):
        distance = get_flight_distance(flight.departure_airport, flight.arrival_airport)
        is_deal = deal_detector.is_good_deal(flight)

        if flight.points:
            miles_per_point = distance / flight.points
            cpp = (flight.price_usd * 100) / flight.points
        else:
            miles_per_point = 0
            cpp = 0

        print(f"Flight {i}:")
        print(f"  Route: {flight.departure_airport} → {flight.arrival_airport} ({distance:,.0f} miles)")
        print(f"  Class: {flight.cabin_class}, Stops: {flight.stops}")
        print(f"  Price: ${flight.price_usd:,.0f} or {flight.points:,} points")
        print(f"  Metrics:")
        print(f"    • Cents per point: {cpp:.2f}¢")
        print(f"    • Miles per point: {miles_per_point:.3f}")
        print(f"    • Distance efficiency: ", end="")

        if miles_per_point >= 0.15:
            print("⭐⭐⭐ EXCEPTIONAL")
        elif miles_per_point >= 0.10:
            print("⭐⭐ GREAT")
        elif miles_per_point >= 0.05:
            print("⭐ GOOD")
        else:
            print("❌ Poor")

        print(f"  Result: {'✅ GOOD DEAL' if is_deal else '❌ Not a deal'}\n")

    # Test ranking
    print("="*60)
    print("RANKING BY DEAL QUALITY")
    print("="*60 + "\n")

    ranked = deal_detector.rank_deals(test_flights)

    for i, flight in enumerate(ranked, 1):
        distance = get_flight_distance(flight.departure_airport, flight.arrival_airport)
        miles_per_point = distance / flight.points if flight.points else 0

        print(f"{i}. {flight.departure_airport}→{flight.arrival_airport} "
              f"({miles_per_point:.3f} mi/pt, "
              f"${flight.price_usd:.0f}, "
              f"{flight.points:,} pts)")


def main():
    """Run distance and deal detection tests."""
    test_distances()
    test_deal_detection()

    print("\n" + "="*60)
    print("✅ DISTANCE-BASED DEAL DETECTION READY!")
    print("="*60 + "\n")

    print("Key Improvements:")
    print("  ✓ Calculates actual flight distances")
    print("  ✓ Evaluates miles-per-point ratio")
    print("  ✓ Ranks by distance efficiency")
    print("  ✓ Shows deal quality (⭐⭐⭐ = exceptional)\n")

    print("Configuration (config/settings.yaml):")
    print("  min_miles_per_point: 0.05  # Adjust based on preferences\n")

    print("Distance Efficiency Guide:")
    print("  0.15+ miles/point = ⭐⭐⭐ EXCEPTIONAL")
    print("  0.10+ miles/point = ⭐⭐ GREAT")
    print("  0.05+ miles/point = ⭐ GOOD")
    print("  <0.05 miles/point = ❌ Poor value\n")


if __name__ == '__main__':
    main()
