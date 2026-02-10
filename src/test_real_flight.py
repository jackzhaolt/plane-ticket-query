"""Test with a real flight example: TPE → SFO on EVA Air."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date
from searchers.base import Flight
from deal_detector import DealDetector
from distance_calculator import get_flight_distance
from award_charts import STANDARD_AWARD_CHART, DealQuality
import yaml


def main():
    """Test the real flight: TPE → SFO business for 75k points."""
    print("\n" + "="*70)
    print("🧪 REAL FLIGHT TEST: TPE → SFO Business Class")
    print("="*70 + "\n")

    # Load config
    with open('config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)

    deal_detector = DealDetector(config['deals'])

    # Calculate distance
    distance = get_flight_distance("TPE", "SFO")
    print(f"Route: TPE (Taipei) → SFO (San Francisco)")
    print(f"Distance: {distance:,.0f} miles")
    print(f"Airline: EVA Air (BR)")
    print(f"Date: September 4, 2026")
    print(f"Class: BUSINESS")
    print(f"Points: 75,000\n")

    # Determine which distance band
    print("="*70)
    print("DISTANCE BAND ANALYSIS")
    print("="*70 + "\n")

    if distance <= 5000:
        band = "0-5,000 miles"
        expected = "110k-140k business"
    elif distance <= 7500:
        band = "5,001-7,500 miles"
        expected = "150k-180k business"
    elif distance <= 11000:
        band = "7,501-11,000 miles"
        expected = "175k-210k business"
    else:
        band = "11,001-15,000 miles"
        expected = "220k-264k business"

    print(f"This route falls in: {band}")
    print(f"Expected range: {expected}\n")

    # Create the flight object
    flight = Flight(
        departure_airport="TPE",
        arrival_airport="SFO",
        departure_date=date(2026, 9, 4),
        return_date=None,
        price_usd=3200,  # Estimated business class cash price
        points=75000,
        airline="BR",  # EVA Air
        cabin_class="BUSINESS",
        stops=0  # Assuming direct
    )

    # Evaluate with award chart
    print("="*70)
    print("AWARD CHART EVALUATION")
    print("="*70 + "\n")

    expected_range = STANDARD_AWARD_CHART.get_expected_points(distance, "BUSINESS")
    quality, explanation = STANDARD_AWARD_CHART.evaluate_deal(
        distance, flight.points, "BUSINESS"
    )

    if expected_range:
        min_pts, max_pts = expected_range
        print(f"Expected Range: {min_pts:,}-{max_pts:,} points")
        print(f"This Flight: {flight.points:,} points")
        print(f"\nSavings: {min_pts - flight.points:,} points below minimum!")
        print(f"Percentage: {((min_pts - flight.points) / min_pts * 100):.0f}% below expected minimum\n")

    print(f"Quality Rating: ", end="")
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

    print(f"\n{explanation}\n")

    # Check if it's a deal
    is_deal = deal_detector.is_good_deal(flight)

    print("="*70)
    print("DEAL EVALUATION")
    print("="*70 + "\n")

    print(f"Is this a good deal? {'✅ YES!' if is_deal else '❌ NO'}\n")

    if is_deal:
        print("Why this is a great deal:")
        print("  ✓ Business class on premium carrier (EVA Air)")
        print("  ✓ Trans-Pacific long-haul flight")
        print(f"  ✓ {distance:,.0f} miles for {flight.points:,} points")

        # Calculate metrics
        cpp = (flight.price_usd * 100) / flight.points
        miles_per_point = distance / flight.points

        print(f"  ✓ {cpp:.2f}¢ per point value")
        print(f"  ✓ {miles_per_point:.3f} miles per point")

        if expected_range:
            savings = expected_range[0] - flight.points
            print(f"  ✓ Save {savings:,} points vs standard pricing!")

    # Full formatted summary
    print("\n" + "="*70)
    print("FULL DEAL SUMMARY")
    print("="*70 + "\n")

    summary = deal_detector.format_deal_summary(flight)
    print(summary)

    print("="*70)
    print("RECOMMENDATION")
    print("="*70 + "\n")

    if quality == DealQuality.EXCEPTIONAL:
        print("🎯 BOOK THIS IMMEDIATELY!")
        print("\nThis is an exceptional business class deal on a premium carrier.")
        print(f"You're saving {expected_range[0] - flight.points:,} points compared to")
        print("standard award chart pricing. Deals like this don't come often!\n")
    elif quality == DealQuality.GREAT:
        print("👍 Excellent deal - book if dates work!")
    elif quality == DealQuality.GOOD:
        print("✓ Good standard pricing")
    else:
        print("⚠️ Consider waiting for better availability")


if __name__ == '__main__':
    main()
