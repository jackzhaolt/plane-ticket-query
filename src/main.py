"""Main script for flight deal monitoring and alerts."""

import os
import sys
import yaml
import schedule
import time
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from typing import List

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from searchers.base import Flight
from searchers.api_searcher import AmadeusSearcher
from deal_detector import DealDetector
from notifiers.email_notifier import EmailNotifier
from notifiers.sms_notifier import SMSNotifier
from country_airports import expand_country_config


class FlightMonitor:
    """Main flight monitoring and alert system."""

    def __init__(self, config_path: str = "config/settings.yaml"):
        """
        Initialize flight monitor.

        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Initialize components
        self.searcher = self._init_searcher()
        self.deal_detector = DealDetector(self.config['deals'])

        # Initialize notifiers
        self.email_notifier = None
        self.sms_notifier = None

        if self.config['alerts']['email']:
            try:
                self.email_notifier = EmailNotifier()
                print("✓ Email notifier initialized")
            except ValueError as e:
                print(f"⚠ Email notifier disabled: {e}")

        if self.config['alerts']['sms']:
            try:
                self.sms_notifier = SMSNotifier()
                print("✓ SMS notifier initialized")
            except ValueError as e:
                print(f"⚠ SMS notifier disabled: {e}")

    def _init_searcher(self):
        """Initialize the appropriate flight searcher based on config."""
        searcher_type = self.config['searcher']['type']

        if searcher_type == 'api':
            return AmadeusSearcher()
        elif searcher_type == 'selenium':
            from searchers.amex_selenium_searcher import AmexTravelSearcher
            return AmexTravelSearcher()
        elif searcher_type == 'hybrid':
            from searchers.hybrid_searcher import HybridSearcher
            hybrid_config = self.config['searcher'].get('hybrid', {})
            return HybridSearcher(
                use_selenium=hybrid_config.get('use_selenium', True),
                selenium_headless=hybrid_config.get('selenium_headless', True)
            )
        else:
            raise ValueError(f"Unknown searcher type: {searcher_type}")

    def _generate_search_dates(self) -> List[date]:
        """Generate dates to search based on configuration."""
        dates = []
        date_ranges = self.config['search'].get('date_ranges', [])

        if not date_ranges:
            # Default: search next 6 months
            start = date.today()
            for i in range(180):
                dates.append(start + timedelta(days=i))
        else:
            # Use configured date ranges
            for range_config in date_ranges:
                start = datetime.strptime(range_config['start'], '%Y-%m-%d').date()
                end = datetime.strptime(range_config['end'], '%Y-%m-%d').date()

                current = start
                while current <= end:
                    dates.append(current)
                    current += timedelta(days=7)  # Weekly searches

        return dates

    def check_for_deals(self):
        """Check for flight deals and send alerts if found."""
        print(f"\n{'='*60}")
        print(f"🔍 Checking for deals at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        search_config = self.config['search']

        # Expand countries to airports
        departure_airports, arrival_airports = expand_country_config(
            departure_countries=search_config.get('departure_countries'),
            arrival_countries=search_config.get('arrival_countries'),
            departure_airports=search_config.get('departure_airports'),
            arrival_airports=search_config.get('arrival_airports')
        )

        print(f"📍 Search Configuration:")
        print(f"   Departure: {len(departure_airports)} airports in {search_config.get('departure_countries', [])}")
        print(f"   Arrival: {len(arrival_airports)} airports in {search_config.get('arrival_countries', [])}")
        print(f"   Total combinations: {len(departure_airports)} × {len(arrival_airports)} = {len(departure_airports) * len(arrival_airports)}\n")

        dates = self._generate_search_dates()

        all_deals = []

        # Search for deals
        for departure_date in dates[:3]:  # Limit to first 3 dates for testing
            print(f"\nSearching for flights on {departure_date}...")

            try:
                flights = self.searcher.search(
                    departure_airports=departure_airports,
                    arrival_airports=arrival_airports,
                    departure_date=departure_date,
                    return_date=None,  # One-way for now
                    adults=search_config['adults'],
                    cabin_class=search_config['cabin_class']
                )

                # Filter for good deals
                deals = self.deal_detector.filter_deals(flights)

                if deals:
                    print(f"✓ Found {len(deals)} deal(s) on {departure_date}")
                    all_deals.extend(deals)
                else:
                    print(f"  No deals found on {departure_date}")

            except Exception as e:
                print(f"✗ Error searching {departure_date}: {e}")
                continue

        # Send alerts if deals found
        if all_deals:
            self._send_alerts(all_deals)
        else:
            print("\n📭 No deals found in this check.")

    def _send_alerts(self, deals: List[Flight]):
        """
        Send alerts for found deals.

        Args:
            deals: List of flight deals
        """
        # Rank deals
        ranked_deals = self.deal_detector.rank_deals(deals)

        print(f"\n🎉 Found {len(ranked_deals)} deal(s)! Sending alerts...")

        # Send email alert
        if self.email_notifier:
            summaries = [self.deal_detector.format_deal_summary(deal) for deal in ranked_deals]
            self.email_notifier.send_deals_alert(summaries)

        # Send SMS alert (only for top deal to keep message short)
        if self.sms_notifier and ranked_deals:
            top_deal = ranked_deals[0]
            summary = self.deal_detector.format_deal_summary(top_deal)
            self.sms_notifier.send_deals_alert(len(ranked_deals), summary)

    def run_once(self):
        """Run a single check for deals."""
        try:
            self.check_for_deals()
        except KeyboardInterrupt:
            print("\n\n👋 Stopping...")
            self.cleanup()
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Error during check: {e}")

    def run_scheduled(self):
        """Run continuous monitoring with scheduled checks."""
        interval = self.config['alerts']['check_interval']

        print(f"\n{'='*60}")
        print(f"🚀 Starting flight monitor")
        print(f"⏱  Checking every {interval} minutes")
        print(f"📍 Route: {self.config['search']['departure_country']} → {self.config['search']['arrival_country']}")
        print(f"{'='*60}\n")

        # Schedule regular checks
        schedule.every(interval).minutes.do(self.check_for_deals)

        # Run first check immediately
        self.check_for_deals()

        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n\n👋 Stopping monitor...")
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        if self.searcher:
            self.searcher.close()
        print("✓ Cleanup complete")


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    # Check for required environment variables
    if not os.getenv('AMADEUS_API_KEY'):
        print("\n⚠ Missing configuration!")
        print("Please copy .env.example to .env and fill in your API keys.\n")
        sys.exit(1)

    # Create monitor
    try:
        monitor = FlightMonitor()

        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == '--once':
            # Run once and exit
            monitor.run_once()
        else:
            # Run continuous monitoring
            monitor.run_scheduled()

    except FileNotFoundError:
        print("\n✗ Configuration file not found!")
        print("Make sure config/settings.yaml exists.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Failed to start: {e}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
