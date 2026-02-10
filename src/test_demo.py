"""Demo script to test the flight search system without real API calls."""

import sys
import os
from datetime import date, timedelta
from random import randint, choice

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from searchers.base import Flight
from deal_detector import DealDetector
from notifiers.email_notifier import EmailNotifier


def generate_demo_flights():
    """Generate realistic demo flight data for testing."""
    airlines = ["AA", "DL", "UA", "NH", "JL", "LH", "BA", "AF"]
    cabin_classes = ["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS"]

    flights = []

    # Generate 10 sample flights
    for i in range(10):
        departure_date = date.today() + timedelta(days=randint(30, 180))

        # Mix of good and bad deals
        if i < 3:  # Good deals
            price = randint(450, 750)
            points = randint(40000, 60000)
            stops = choice([0, 1])
        elif i < 6:  # Medium deals
            price = randint(800, 1200)
            points = randint(65000, 85000)
            stops = choice([1, 2])
        else:  # Poor deals
            price = randint(1300, 2000)
            points = randint(90000, 130000)
            stops = choice([1, 2, 3])

        flight = Flight(
            departure_airport="JFK",
            arrival_airport="NRT",
            departure_date=departure_date,
            return_date=None,
            price_usd=price,
            points=points,
            airline=choice(airlines),
            cabin_class=choice(cabin_classes),
            stops=stops,
            currency="USD"
        )

        flights.append(flight)

    return flights


def main():
    """Run demo test."""
    print("\n" + "="*60)
    print("🧪 DEMO MODE - Flight Search System Test")
    print("="*60 + "\n")

    print("📋 Configuration loaded")
    print("✓ Deal detector initialized")
    print("✓ Demo flight data generated\n")

    # Load deal detector config
    import yaml
    with open('config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)

    deal_detector = DealDetector(config['deals'])

    # Generate demo flights
    print("🔍 Searching for flights...\n")
    flights = generate_demo_flights()

    print(f"Found {len(flights)} flights:\n")
    for i, flight in enumerate(flights, 1):
        print(f"{i}. {flight}")

    # Filter for deals
    print(f"\n{'='*60}")
    print("💰 Analyzing deals...")
    print(f"{'='*60}\n")

    deals = deal_detector.filter_deals(flights)

    if deals:
        print(f"✓ Found {len(deals)} good deal(s)!\n")

        # Rank deals
        ranked_deals = deal_detector.rank_deals(deals)

        # Show deal summaries
        for i, deal in enumerate(ranked_deals, 1):
            print(f"\n{'='*60}")
            print(f"DEAL #{i}")
            print(f"{'='*60}")
            summary = deal_detector.format_deal_summary(deal)
            print(summary)

        # Show what would be sent via email
        print(f"\n{'='*60}")
        print("📧 Email Alert Preview")
        print(f"{'='*60}\n")

        print("Subject: ✈️ 3 Flight Deals Found!")
        print("\nBody:")
        print("-" * 40)
        summaries = [deal_detector.format_deal_summary(deal) for deal in ranked_deals[:3]]
        print("\n\n" + "="*60 + "\n\n".join(summaries))

    else:
        print("📭 No deals found matching your criteria.")
        print("\nTip: Adjust thresholds in config/settings.yaml:")
        print(f"  - Current max price: ${config['deals']['max_cash_price']}")
        print(f"  - Current max points: {config['deals']['max_points']:,}")
        print(f"  - Current min cents per point: {config['deals']['min_cpp']}")

    print(f"\n{'='*60}")
    print("✅ Demo test complete!")
    print(f"{'='*60}\n")

    print("Next steps:")
    print("1. Get Amadeus API key from https://developers.amadeus.com")
    print("2. Update .env file with your credentials")
    print("3. Run: python src/main.py --once")
    print("4. For continuous monitoring: python src/main.py\n")


if __name__ == '__main__':
    main()
