"""Base searcher interface for flight searches.

This abstract base class defines the interface that all flight searchers must implement.
Allows easy swapping between API and Selenium implementations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class Flight:
    """Represents a flight search result."""
    departure_airport: str
    arrival_airport: str
    departure_date: date
    return_date: Optional[date]
    price_usd: float
    points: Optional[int]
    airline: str
    cabin_class: str
    stops: int
    currency: str = "USD"
    booking_url: Optional[str] = None

    def __str__(self):
        route = f"{self.departure_airport} → {self.arrival_airport}"
        date_str = f"{self.departure_date}"
        if self.return_date:
            date_str += f" - {self.return_date}"

        price_str = f"${self.price_usd:.2f}"
        if self.points:
            price_str += f" or {self.points:,} points"

        stops_str = "Direct" if self.stops == 0 else f"{self.stops} stop(s)"

        return f"{route} | {date_str} | {self.airline} | {price_str} | {stops_str}"


class FlightSearcher(ABC):
    """Abstract base class for flight searchers."""

    @abstractmethod
    def search(
        self,
        departure_airports: List[str],
        arrival_airports: List[str],
        departure_date: date,
        return_date: Optional[date] = None,
        adults: int = 1,
        cabin_class: str = "ECONOMY"
    ) -> List[Flight]:
        """
        Search for flights matching the criteria.

        Args:
            departure_airports: List of departure airport codes
            arrival_airports: List of arrival airport codes
            departure_date: Departure date
            return_date: Return date (None for one-way)
            adults: Number of adult passengers
            cabin_class: Cabin class (ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST)

        Returns:
            List of Flight objects matching the search criteria
        """
        pass

    @abstractmethod
    def close(self):
        """Clean up resources (close browser, connections, etc.)"""
        pass
