"""API-based flight searcher using Amadeus API."""

import os
import time
from datetime import date, timedelta
from typing import List, Optional
from amadeus import Client, ResponseError

from .base import Flight, FlightSearcher


class AmadeusSearcher(FlightSearcher):
    """Flight searcher using Amadeus API."""

    def __init__(self, api_key: str = None, api_secret: str = None):
        """
        Initialize Amadeus API client.

        Args:
            api_key: Amadeus API key (defaults to AMADEUS_API_KEY env var)
            api_secret: Amadeus API secret (defaults to AMADEUS_API_SECRET env var)
        """
        self.api_key = api_key or os.getenv('AMADEUS_API_KEY')
        self.api_secret = api_secret or os.getenv('AMADEUS_API_SECRET')

        if not self.api_key or not self.api_secret:
            raise ValueError(
                "Amadeus API credentials not found. "
                "Set AMADEUS_API_KEY and AMADEUS_API_SECRET in .env file."
            )

        self.client = Client(
            client_id=self.api_key,
            client_secret=self.api_secret
        )

        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests

    def _rate_limit(self):
        """Implement simple rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()

    def search(
        self,
        departure_airports: List[str],
        arrival_airports: List[str],
        departure_date: date,
        return_date: Optional[date] = None,
        adults: int = 1,
        cabin_class: str = "ECONOMY"
    ) -> List[Flight]:
        """Search for flights using Amadeus API."""
        all_flights = []

        # Search all combinations of departure and arrival airports
        for dep_airport in departure_airports:
            for arr_airport in arrival_airports:
                try:
                    self._rate_limit()

                    # Build search parameters
                    params = {
                        'originLocationCode': dep_airport,
                        'destinationLocationCode': arr_airport,
                        'departureDate': departure_date.strftime('%Y-%m-%d'),
                        'adults': adults,
                        'travelClass': cabin_class,
                        'currencyCode': 'USD',
                        'max': 50  # Number of results
                    }

                    if return_date:
                        params['returnDate'] = return_date.strftime('%Y-%m-%d')

                    # Make API request
                    response = self.client.shopping.flight_offers_search.get(**params)

                    # Parse results
                    flights = self._parse_response(response.data)
                    all_flights.extend(flights)

                    print(f"✓ Found {len(flights)} flights: {dep_airport} → {arr_airport}")

                except ResponseError as error:
                    print(f"✗ Error searching {dep_airport} → {arr_airport}: {error}")
                    continue

        return all_flights

    def _parse_response(self, data: List) -> List[Flight]:
        """Parse Amadeus API response into Flight objects."""
        flights = []

        for offer in data:
            try:
                # Extract itinerary info
                itinerary = offer['itineraries'][0]
                first_segment = itinerary['segments'][0]
                last_segment = itinerary['segments'][-1]

                # Calculate stops
                stops = len(itinerary['segments']) - 1

                # Extract price
                price = float(offer['price']['total'])

                # Extract dates
                dep_date = date.fromisoformat(first_segment['departure']['at'].split('T')[0])

                # Return date if round trip
                return_date = None
                if len(offer['itineraries']) > 1:
                    return_itinerary = offer['itineraries'][1]
                    return_segment = return_itinerary['segments'][0]
                    return_date = date.fromisoformat(return_segment['departure']['at'].split('T')[0])

                # Extract airline
                airline_code = first_segment['carrierCode']

                # Estimate points (rough calculation: 1 cent per point)
                # In reality, this would need Amex transfer partner data
                estimated_points = int(price * 100)  # Placeholder logic

                flight = Flight(
                    departure_airport=first_segment['departure']['iataCode'],
                    arrival_airport=last_segment['arrival']['iataCode'],
                    departure_date=dep_date,
                    return_date=return_date,
                    price_usd=price,
                    points=estimated_points,
                    airline=airline_code,
                    cabin_class=first_segment['cabin'],
                    stops=stops,
                    booking_url=None  # API doesn't provide direct booking URL
                )

                flights.append(flight)

            except (KeyError, ValueError) as e:
                print(f"Warning: Could not parse flight offer: {e}")
                continue

        return flights

    def close(self):
        """Clean up resources."""
        # No cleanup needed for API client
        pass
