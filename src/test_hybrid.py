"""Test script for hybrid searcher with demo data."""

import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from searchers.hybrid_searcher import HybridSearcher
from deal_detector import DealDetector
import yaml


def main():
    """Test hybrid searcher."""
    print("\n" + "="*60)
    print("🧪 HYBRID SEARCHER TEST")
    print("="*60 + "\n")

    # Load config
    with open('config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)

    print("Initializing hybrid searcher...")
    print("  📡 API Mode: Will use Amadeus API if credentials provided")
    print("  🌐 Selenium Mode: Will scrape Amex Travel for accurate points")
    print("  🔄 Hybrid Mode: Combines both intelligently\n")

    try:
        # Initialize hybrid searcher
        searcher = HybridSearcher(
            use_selenium=False,  # Set to False for now (Selenium needs customization)
            selenium_headless=True
        )

        print("✓ Hybrid searcher initialized\n")

        # Test search
        departure_date = date.today() + timedelta(days=60)

        print(f"🔍 Searching for flights:")
        print(f"  Route: {config['search']['departure_airports'][0]} → {config['search']['arrival_airports'][0]}")
        print(f"  Date: {departure_date}")
        print(f"  Mode: Hybrid (API first, then Selenium if needed)\n")

        flights = searcher.search(
            departure_airports=config['search']['departure_airports'][:1],
            arrival_airports=config['search']['arrival_airports'][:1],
            departure_date=departure_date,
            adults=1,
            cabin_class=config['search']['cabin_class'],
            mode="auto"  # Use intelligent hybrid mode
        )

        print(f"\n✓ Found {len(flights)} flights\n")

        if flights:
            # Show results
            print("="*60)
            print("SEARCH RESULTS")
            print("="*60 + "\n")

            for i, flight in enumerate(flights[:10], 1):
                print(f"{i}. {flight}")

            # Analyze deals
            deal_detector = DealDetector(config['deals'])
            deals = deal_detector.filter_deals(flights)

            if deals:
                print(f"\n{'='*60}")
                print(f"💰 FOUND {len(deals)} DEAL(S)!")
                print(f"{'='*60}\n")

                ranked = deal_detector.rank_deals(deals)
                for i, deal in enumerate(ranked[:3], 1):
                    print(f"\nDeal #{i}:")
                    print("-" * 40)
                    print(deal_detector.format_deal_summary(deal))

        else:
            print("No flights found. This likely means:")
            print("  1. Amadeus API credentials not set in .env")
            print("  2. No flights available for this route/date")
            print("  3. API rate limit reached\n")

        searcher.close()

        print("\n" + "="*60)
        print("✅ Hybrid test complete!")
        print("="*60 + "\n")

        print("How Hybrid Mode Works:")
        print("  1. Fast API Check: Amadeus API screens for availability (seconds)")
        print("  2. Smart Decision: If promising deals found, triggers Selenium")
        print("  3. Deep Scraping: Selenium gets exact Amex points pricing (minutes)")
        print("  4. Caching: Selenium results cached for 6 hours")
        print("  5. Deduplication: Combines both sources, prefers Selenium data\n")

        print("Next Steps:")
        print("  1. Get Amadeus API key (for fast daily checks)")
        print("  2. Customize Selenium selectors (see AMEX_SCRAPING_GUIDE.md)")
        print("  3. Enable Selenium: set use_selenium=True in config")
        print("  4. Optional: Add Amex login credentials for member pricing\n")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  - .env file exists with API credentials")
        print("  - config/settings.yaml is properly configured\n")


if __name__ == '__main__':
    main()
