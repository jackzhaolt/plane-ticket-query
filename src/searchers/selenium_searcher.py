"""Selenium-based flight searcher (future implementation).

This will be implemented to scrape Amex Travel and other booking sites
when API access is insufficient or unavailable.
"""

from datetime import date
from typing import List, Optional

from .base import Flight, FlightSearcher


class SeleniumSearcher(FlightSearcher):
    """Flight searcher using Selenium web automation."""

    def __init__(self, headless: bool = True):
        """
        Initialize Selenium WebDriver.

        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.driver = None

        # TODO: Initialize Selenium WebDriver
        raise NotImplementedError("Selenium searcher not yet implemented")

    def search(
        self,
        departure_airports: List[str],
        arrival_airports: List[str],
        departure_date: date,
        return_date: Optional[date] = None,
        adults: int = 1,
        cabin_class: str = "ECONOMY"
    ) -> List[Flight]:
        """Search for flights using Selenium web scraping."""
        # TODO: Implement Selenium-based search
        # 1. Navigate to Amex Travel or airline website
        # 2. Fill in search form
        # 3. Submit and wait for results
        # 4. Parse results from page
        # 5. Return Flight objects
        raise NotImplementedError("Selenium searcher not yet implemented")

    def close(self):
        """Clean up Selenium resources."""
        if self.driver:
            self.driver.quit()
