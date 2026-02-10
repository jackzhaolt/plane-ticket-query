"""Hybrid searcher that combines API and Selenium approaches."""

import os
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict
import json

from .base import Flight, FlightSearcher
from .api_searcher import AmadeusSearcher
from .amex_selenium_searcher import AmexTravelSearcher


class HybridSearcher(FlightSearcher):
    """
    Intelligent hybrid searcher that combines fast API checks with accurate Selenium scraping.

    Strategy:
    - Use Amadeus API for daily/frequent checks (fast, general availability)
    - Use Amex Travel scraping weekly or for promising routes (slow, accurate points)
    - Cache results to avoid redundant scraping
    """

    def __init__(
        self,
        api_key: str = None,
        api_secret: str = None,
        use_selenium: bool = True,
        selenium_headless: bool = True,
        cache_dir: str = "/tmp/flight_cache"
    ):
        """
        Initialize hybrid searcher.

        Args:
            api_key: Amadeus API key
            api_secret: Amadeus API secret
            use_selenium: Enable Selenium scraping
            selenium_headless: Run browser in headless mode
            cache_dir: Directory to cache results
        """
        # Initialize API searcher
        try:
            self.api_searcher = AmadeusSearcher(api_key, api_secret)
            self.has_api = True
            print("✓ Amadeus API searcher initialized")
        except ValueError as e:
            print(f"⚠ Amadeus API not available: {e}")
            self.api_searcher = None
            self.has_api = False

        # Initialize Selenium searcher (lazy load)
        self.use_selenium = use_selenium
        self.selenium_headless = selenium_headless
        self.selenium_searcher = None
        self.selenium_initialized = False

        # Cache settings
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_expiry_hours = 6  # Cache expires after 6 hours

    def _init_selenium(self):
        """Lazy initialize Selenium searcher."""
        if self.selenium_initialized:
            return

        if self.use_selenium:
            try:
                amex_username = os.getenv('AMEX_USERNAME')
                amex_password = os.getenv('AMEX_PASSWORD')

                self.selenium_searcher = AmexTravelSearcher(
                    headless=self.selenium_headless,
                    amex_username=amex_username,
                    amex_password=amex_password
                )
                print("✓ Amex Travel scraper initialized")
            except Exception as e:
                print(f"⚠ Selenium scraper failed to initialize: {e}")
                self.selenium_searcher = None

        self.selenium_initialized = True

    def search(
        self,
        departure_airports: List[str],
        arrival_airports: List[str],
        departure_date: date,
        return_date: Optional[date] = None,
        adults: int = 1,
        cabin_class: str = "ECONOMY",
        mode: str = "auto"
    ) -> List[Flight]:
        """
        Search for flights using hybrid approach.

        Args:
            departure_airports: List of departure airport codes
            arrival_airports: List of arrival airport codes
            departure_date: Departure date
            return_date: Return date (None for one-way)
            adults: Number of adult passengers
            cabin_class: Cabin class
            mode: Search mode - "api", "selenium", or "auto" (default)

        Returns:
            List of Flight objects
        """
        # Determine search strategy
        if mode == "api":
            return self._search_api_only(
                departure_airports, arrival_airports, departure_date,
                return_date, adults, cabin_class
            )
        elif mode == "selenium":
            return self._search_selenium_only(
                departure_airports, arrival_airports, departure_date,
                return_date, adults, cabin_class
            )
        else:  # auto mode
            return self._search_hybrid(
                departure_airports, arrival_airports, departure_date,
                return_date, adults, cabin_class
            )

    def _search_hybrid(
        self,
        departure_airports: List[str],
        arrival_airports: List[str],
        departure_date: date,
        return_date: Optional[date],
        adults: int,
        cabin_class: str
    ) -> List[Flight]:
        """
        Hybrid search strategy:
        1. Check API first (fast screening)
        2. If good deals found, verify with Selenium (accurate points)
        3. Use cached Selenium results if recent enough
        """
        all_flights = []

        # Step 1: Fast API screening
        print("📡 Phase 1: Fast API screening...")
        api_flights = []
        if self.has_api:
            api_flights = self._search_api_only(
                departure_airports, arrival_airports, departure_date,
                return_date, adults, cabin_class
            )
            all_flights.extend(api_flights)

        # Step 2: Decide if we need Selenium verification
        if not self.use_selenium:
            return all_flights

        # Check if we should do Selenium scraping
        needs_selenium = self._should_use_selenium(api_flights, departure_date)

        if needs_selenium:
            print("\n🌐 Phase 2: Detailed Amex Travel scraping...")
            print("  (This may take a few minutes...)")

            self._init_selenium()

            if self.selenium_searcher:
                # Check cache first
                cached_flights = self._get_cached_flights(
                    departure_airports, arrival_airports, departure_date
                )

                if cached_flights:
                    print(f"  ✓ Using {len(cached_flights)} cached results")
                    all_flights.extend(cached_flights)
                else:
                    # Do the scraping
                    selenium_flights = self._search_selenium_only(
                        departure_airports, arrival_airports, departure_date,
                        return_date, adults, cabin_class
                    )

                    # Cache results
                    self._cache_flights(
                        selenium_flights, departure_airports, arrival_airports, departure_date
                    )

                    all_flights.extend(selenium_flights)

        # Deduplicate flights (prefer Selenium data over API)
        deduplicated = self._deduplicate_flights(all_flights)

        return deduplicated

    def _search_api_only(
        self,
        departure_airports: List[str],
        arrival_airports: List[str],
        departure_date: date,
        return_date: Optional[date],
        adults: int,
        cabin_class: str
    ) -> List[Flight]:
        """Search using only Amadeus API."""
        if not self.has_api:
            print("⚠ API searcher not available")
            return []

        return self.api_searcher.search(
            departure_airports, arrival_airports, departure_date,
            return_date, adults, cabin_class
        )

    def _search_selenium_only(
        self,
        departure_airports: List[str],
        arrival_airports: List[str],
        departure_date: date,
        return_date: Optional[date],
        adults: int,
        cabin_class: str
    ) -> List[Flight]:
        """Search using only Selenium scraper."""
        self._init_selenium()

        if not self.selenium_searcher:
            print("⚠ Selenium searcher not available")
            return []

        return self.selenium_searcher.search(
            departure_airports, arrival_airports, departure_date,
            return_date, adults, cabin_class
        )

    def _should_use_selenium(self, api_flights: List[Flight], departure_date: date) -> bool:
        """
        Decide if we should use Selenium scraping.

        Criteria:
        - Found promising deals in API results
        - Date is within next 6 months
        - Haven't scraped recently (check cache)
        """
        # Always scrape if no API results
        if not api_flights:
            return True

        # Check if date is in near future (within 6 months)
        days_until_departure = (departure_date - date.today()).days
        if days_until_departure < 0 or days_until_departure > 180:
            return False

        # Check if we found any promising deals (low prices)
        promising_deals = [f for f in api_flights if f.price_usd < 1000]
        if promising_deals:
            print(f"  💡 Found {len(promising_deals)} promising deals in API, will verify with Amex Travel")
            return True

        # Default: use Selenium every 7 days
        # (In practice, you'd check when last scraped)
        return False

    def _deduplicate_flights(self, flights: List[Flight]) -> List[Flight]:
        """
        Remove duplicate flights, preferring Selenium data over API data.
        """
        seen = {}

        for flight in flights:
            key = (
                flight.departure_airport,
                flight.arrival_airport,
                flight.departure_date,
                flight.airline,
                flight.departure_date  # Use departure date as part of key
            )

            if key not in seen:
                seen[key] = flight
            else:
                # Prefer flights with booking URLs (from Selenium) over API results
                if flight.booking_url and not seen[key].booking_url:
                    seen[key] = flight

        return list(seen.values())

    def _get_cached_flights(
        self,
        departure_airports: List[str],
        arrival_airports: List[str],
        departure_date: date
    ) -> Optional[List[Flight]]:
        """Check if we have recent cached Selenium results."""
        cache_key = f"{'-'.join(departure_airports)}_{'-'.join(arrival_airports)}_{departure_date}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        if not os.path.exists(cache_file):
            return None

        # Check if cache is still valid
        cache_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file))
        if cache_age > timedelta(hours=self.cache_expiry_hours):
            return None

        # Load cached flights
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)

            flights = []
            for item in data:
                flight = Flight(
                    departure_airport=item['departure_airport'],
                    arrival_airport=item['arrival_airport'],
                    departure_date=date.fromisoformat(item['departure_date']),
                    return_date=date.fromisoformat(item['return_date']) if item.get('return_date') else None,
                    price_usd=item['price_usd'],
                    points=item.get('points'),
                    airline=item['airline'],
                    cabin_class=item['cabin_class'],
                    stops=item['stops'],
                    booking_url=item.get('booking_url')
                )
                flights.append(flight)

            return flights

        except Exception as e:
            print(f"  ⚠ Error loading cache: {e}")
            return None

    def _cache_flights(
        self,
        flights: List[Flight],
        departure_airports: List[str],
        arrival_airports: List[str],
        departure_date: date
    ):
        """Cache Selenium search results."""
        cache_key = f"{'-'.join(departure_airports)}_{'-'.join(arrival_airports)}_{departure_date}"
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        try:
            data = []
            for flight in flights:
                data.append({
                    'departure_airport': flight.departure_airport,
                    'arrival_airport': flight.arrival_airport,
                    'departure_date': flight.departure_date.isoformat(),
                    'return_date': flight.return_date.isoformat() if flight.return_date else None,
                    'price_usd': flight.price_usd,
                    'points': flight.points,
                    'airline': flight.airline,
                    'cabin_class': flight.cabin_class,
                    'stops': flight.stops,
                    'booking_url': flight.booking_url
                })

            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"  ✓ Cached {len(flights)} flights")

        except Exception as e:
            print(f"  ⚠ Error caching flights: {e}")

    def close(self):
        """Clean up resources."""
        if self.api_searcher:
            self.api_searcher.close()

        if self.selenium_searcher:
            self.selenium_searcher.close()
