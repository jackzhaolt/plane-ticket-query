"""Test award chart-based deal detection."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date, timedelta
from searchers.base import Flight
from deal_detector import DealDetector
from distance_calculator import get_flight_distance
from award_charts import STANDARD_AWARD_CHART, DealQuality
import yaml


def main():
    """Test award chart evaluation."""
    print("\n" + "="*70)
    print("🎯 AWARD CHART-BASED DEAL DETECTION")
    print("="*70 + "\n")

    # Load config
    with open('config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)

    deal_detector = DealDetector(config['deals'])

    print("Award Chart: STANDARD")
    print("\nDistance Bands:")
    print("  • 0-5,000 miles:     55k-69k economy, 110k-140k business")
    print("  • 5,001-7,500 miles: 75k-90k economy, 150k-180k business")
    print("  • 7,501-11,000 miles: 87.5k-103.5k economy, 175k-210k business")
    print("  • 11,001-15,000 miles: 110k-132k economy, 220k-264k business\n")

    # Create realistic test flights
    test_flights = [
        # EXCEPTIONAL: JFK-NRT for 45k (well below 75k-90k range)
        Flight(
            departure_airport="JFK",
            arrival_airport="NRT",
            departure_date=date.today() + timedelta(days=60),
            return_date=None,
            price_usd=650,
            points=45000,
            airline="NH",
            cabin_class="ECONOMY",
            stops=0
        ),

        # GREAT: JFK-NRT for 78k (low end of 75k-90k range)
        Flight(
            departure_airport="JFK",
            arrival_airport="NRT",
            departure_date=date.today() + timedelta(days=60),
            return_date=None,
            price_usd=750,
            points=78000,
            airline="DL",
            cabin_class="ECONOMY",
            stops=1
        ),

        # FAIR: JFK-NRT for 88k (high end of 75k-90k range)
        Flight(
            departure_airport="JFK",
            arrival_airport="NRT",
            departure_date=date.today() + timedelta(days=60),
            return_date=None,
            price_usd=850,
            points=88000,
            airline="UA",
            cabin_class="ECONOMY",
            stops=1
        ),

        # POOR: JFK-NRT for 110k (above 75k-90k range)
        Flight(
            departure_airport="JFK",
            arrival_airport="NRT",
            departure_date=date.today() + timedelta(days=60),
            return_date=None,
            price_usd=950,
            points=110000,
            airline="AA",
            cabin_class="ECONOMY",
            stops=2
        ),

        # EXCEPTIONAL: JFK-LAX for 50k (below 55k-69k range)
        Flight(
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_date=date.today() + timedelta(days=30),
            return_date=None,
            price_usd=350,
            points=50000,
            airline="AA",
            cabin_class="ECONOMY",
            stops=0
        ),

        # GOOD: JFK-LAX for 60k (mid-range of 55k-69k)
        Flight(
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_date=date.today() + timedelta(days=30),
            return_date=None,
            price_usd=380,
            points=60000,
            airline="DL",
            cabin_class="ECONOMY",
            stops=0
        ),

        # EXCEPTIONAL: Business class JFK-NRT for 115k (below 150k-180k)
        Flight(
            departure_airport="JFK",
            arrival_airport="NRT",
            departure_date=date.today() + timedelta(days=90),
            return_date=None,
            price_usd=3500,
            points=115000,
            airline="NH",
            cabin_class="BUSINESS",
            stops=0
        ),
    ]

    print("="*70)
    print("EVALUATING FLIGHTS")
    print("="*70 + "\n")

    for i, flight in enumerate(test_flights, 1):
        distance = get_flight_distance(flight.departure_airport, flight.arrival_airport)
        is_deal = deal_detector.is_good_deal(flight)

        print(f"Flight {i}: {flight.departure_airport} → {flight.arrival_airport}")
        print(f"  Distance: {distance:,.0f} miles")
        print(f"  Class: {flight.cabin_class}")
        print(f"  Price: ${flight.price_usd:.0f} or {flight.points:,} points")
        print(f"  Stops: {'Direct' if flight.stops == 0 else flight.stops}")

        # Get award chart evaluation
        expected = STANDARD_AWARD_CHART.get_expected_points(distance, flight.cabin_class)
        quality, explanation = STANDARD_AWARD_CHART.evaluate_deal(
            distance, flight.points, flight.cabin_class
        )

        if expected:
            print(f"  Expected: {expected[0]:,}-{expected[1]:,} points")

        print(f"  Rating: ", end="")
        if quality == DealQuality.EXCEPTIONAL:
            print("⭐⭐⭐ EXCEPTIONAL")
        elif quality == DealQuality.GREAT:
            print("⭐⭐ GREAT")
        elif quality == DealQuality.GOOD:
            print("⭐ GOOD")
        elif quality == DealQuality.FAIR:
            print("😐 FAIR")
        else:
            print("❌ POOR")

        print(f"  {explanation}")
        print(f"  Result: {'✅ DEAL' if is_deal else '❌ Not a deal'}\n")

    # Test filtering
    print("="*70)
    print("DEAL FILTERING")
    print("="*70 + "\n")

    deals = deal_detector.filter_deals(test_flights)
    print(f"Found {len(deals)} deals out of {len(test_flights)} flights\n")

    # Test ranking
    print("="*70)
    print("RANKED DEALS (Best First)")
    print("="*70 + "\n")

    ranked = deal_detector.rank_deals(deals)

    for i, flight in enumerate(ranked, 1):
        distance = get_flight_distance(flight.departure_airport, flight.arrival_airport)
        expected = STANDARD_AWARD_CHART.get_expected_points(distance, flight.cabin_class)
        quality, _ = STANDARD_AWARD_CHART.evaluate_deal(distance, flight.points, flight.cabin_class)

        rating_emoji = {
            DealQuality.EXCEPTIONAL: "⭐⭐⭐",
            DealQuality.GREAT: "⭐⭐",
            DealQuality.GOOD: "⭐",
            DealQuality.FAIR: "😐",
            DealQuality.POOR: "❌"
        }.get(quality, "?")

        if expected:
            range_str = f"(exp: {expected[0]//1000}k-{expected[1]//1000}k)"
        else:
            range_str = ""

        print(f"{i}. {rating_emoji} {flight.departure_airport}→{flight.arrival_airport} "
              f"{flight.cabin_class[:3]}: {flight.points//1000}k pts {range_str}")

    # Show full summary for top deal
    if ranked:
        print("\n" + "="*70)
        print("TOP DEAL DETAILS")
        print("="*70 + "\n")
        print(deal_detector.format_deal_summary(ranked[0]))

    print("="*70)
    print("✅ AWARD CHART SYSTEM READY!")
    print("="*70 + "\n")

    print("Key Features:")
    print("  ✓ Distance-based award chart bands")
    print("  ✓ Evaluates deals against standard ranges")
    print("  ✓ Rates: Exceptional, Great, Good, Fair, Poor")
    print("  ✓ Configurable minimum quality threshold")
    print("  ✓ Multiple award charts (standard, ANA, Delta)")
    print("\nConfiguration in config/settings.yaml:")
    print("  use_award_chart: true")
    print("  award_chart: 'standard'  # or 'ana', 'delta'")
    print("  award_chart_min_quality: 'good'  # minimum to accept\n")


if __name__ == '__main__':
    main()
