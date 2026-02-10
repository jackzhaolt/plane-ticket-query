"""Selenium-based searcher for Amex Travel portal."""

import time
from datetime import date
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from .base import Flight, FlightSearcher


class AmexTravelSearcher(FlightSearcher):
    """Scrape Amex Travel portal for actual points pricing."""

    def __init__(self, headless: bool = True, amex_username: str = None, amex_password: str = None):
        """
        Initialize Selenium WebDriver for Amex Travel.

        Args:
            headless: Run browser in headless mode
            amex_username: Amex login username (optional, for logged-in pricing)
            amex_password: Amex login password (optional)
        """
        self.headless = headless
        self.amex_username = amex_username
        self.amex_password = amex_password
        self.driver = None
        self.logged_in = False

    def _init_driver(self):
        """Initialize Chrome WebDriver."""
        if self.driver:
            return

        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

        print("✓ Chrome WebDriver initialized")

    def _login_to_amex(self):
        """Login to Amex account to see member pricing."""
        if self.logged_in or not self.amex_username or not self.amex_password:
            return

        try:
            print("🔐 Logging into Amex account...")
            self.driver.get("https://travel.americanexpress.com/")
            time.sleep(3)

            # Look for login button/link
            # Note: Actual selectors will need to be updated based on current Amex site
            # This is a template that needs to be customized
            try:
                login_btn = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Log In"))
                )
                login_btn.click()
                time.sleep(2)

                # Fill in credentials
                username_field = self.driver.find_element(By.ID, "eliloUserID")
                password_field = self.driver.find_element(By.ID, "eliloPassword")

                username_field.send_keys(self.amex_username)
                password_field.send_keys(self.amex_password)

                # Submit
                submit_btn = self.driver.find_element(By.ID, "loginSubmit")
                submit_btn.click()

                time.sleep(5)
                self.logged_in = True
                print("✓ Logged into Amex")

            except Exception as e:
                print(f"⚠ Could not login to Amex (will search as guest): {e}")

        except Exception as e:
            print(f"⚠ Amex login failed: {e}")

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
        Search Amex Travel for flights.

        Note: This implementation needs to be customized based on the actual
        Amex Travel website structure. This is a template showing the approach.
        """
        self._init_driver()
        self._login_to_amex()

        all_flights = []

        # Search each airport combination
        for dep_airport in departure_airports:
            for arr_airport in arrival_airports:
                try:
                    print(f"🌐 Searching Amex Travel: {dep_airport} → {arr_airport}")

                    flights = self._search_route(
                        dep_airport, arr_airport, departure_date,
                        return_date, adults, cabin_class
                    )

                    all_flights.extend(flights)
                    print(f"✓ Found {len(flights)} flights on Amex Travel")

                    # Be nice to the website
                    time.sleep(2)

                except Exception as e:
                    print(f"✗ Error searching {dep_airport} → {arr_airport}: {e}")
                    continue

        return all_flights

    def _search_route(
        self,
        dep_airport: str,
        arr_airport: str,
        departure_date: date,
        return_date: Optional[date],
        adults: int,
        cabin_class: str
    ) -> List[Flight]:
        """
        Search a specific route on Amex Travel.

        NOTE: This is a TEMPLATE implementation. The actual Amex Travel website
        structure will require customization of selectors and logic.
        """
        flights = []

        try:
            # Navigate to Amex Travel flights page
            self.driver.get("https://travel.americanexpress.com/flights")
            time.sleep(3)

            # Fill in search form
            # NOTE: These selectors are PLACEHOLDERS and need to be updated
            # based on actual Amex Travel website structure

            # Origin
            origin_field = self.driver.find_element(By.ID, "flight-origin")
            origin_field.clear()
            origin_field.send_keys(dep_airport)
            time.sleep(1)

            # Destination
            dest_field = self.driver.find_element(By.ID, "flight-destination")
            dest_field.clear()
            dest_field.send_keys(arr_airport)
            time.sleep(1)

            # Departure date
            dep_date_field = self.driver.find_element(By.ID, "flight-departure-date")
            dep_date_field.clear()
            dep_date_field.send_keys(departure_date.strftime('%m/%d/%Y'))
            time.sleep(1)

            # Return date (if round trip)
            if return_date:
                ret_date_field = self.driver.find_element(By.ID, "flight-return-date")
                ret_date_field.clear()
                ret_date_field.send_keys(return_date.strftime('%m/%d/%Y'))
                time.sleep(1)

            # Submit search
            search_btn = self.driver.find_element(By.ID, "flight-search-button")
            search_btn.click()

            # Wait for results
            print("  ⏳ Waiting for search results...")
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "flight-result"))
            )

            time.sleep(3)

            # Parse results
            flights = self._parse_results(dep_airport, arr_airport, departure_date, return_date)

        except Exception as e:
            print(f"  ✗ Error during search: {e}")
            # Take screenshot for debugging
            try:
                screenshot_path = f"/tmp/amex_error_{dep_airport}_{arr_airport}.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"  📸 Screenshot saved: {screenshot_path}")
            except:
                pass

        return flights

    def _parse_results(
        self,
        dep_airport: str,
        arr_airport: str,
        departure_date: date,
        return_date: Optional[date]
    ) -> List[Flight]:
        """
        Parse Amex Travel search results.

        NOTE: This is a TEMPLATE. Actual parsing will depend on Amex Travel's
        HTML structure. You'll need to inspect the page and update selectors.
        """
        flights = []

        try:
            # Find all flight result cards
            # NOTE: Update selector based on actual Amex Travel structure
            flight_elements = self.driver.find_elements(By.CLASS_NAME, "flight-result")

            print(f"  📋 Parsing {len(flight_elements)} results...")

            for element in flight_elements[:20]:  # Limit to first 20 results
                try:
                    # Extract flight details
                    # NOTE: These are PLACEHOLDER selectors - customize based on actual site

                    # Airline
                    airline = element.find_element(By.CLASS_NAME, "airline-code").text

                    # Price in cash
                    price_elem = element.find_element(By.CLASS_NAME, "price-cash")
                    price_text = price_elem.text.replace('$', '').replace(',', '')
                    price = float(price_text)

                    # Price in points (key feature!)
                    try:
                        points_elem = element.find_element(By.CLASS_NAME, "price-points")
                        points_text = points_elem.text.replace(',', '').replace(' points', '')
                        points = int(points_text)
                    except:
                        points = None

                    # Stops
                    stops_elem = element.find_element(By.CLASS_NAME, "stops")
                    stops_text = stops_elem.text.lower()
                    if 'nonstop' in stops_text or 'direct' in stops_text:
                        stops = 0
                    elif '1 stop' in stops_text:
                        stops = 1
                    elif '2 stop' in stops_text:
                        stops = 2
                    else:
                        stops = 3

                    # Cabin class
                    try:
                        cabin = element.find_element(By.CLASS_NAME, "cabin-class").text.upper()
                    except:
                        cabin = "ECONOMY"

                    # Booking URL
                    try:
                        booking_link = element.find_element(By.TAG_NAME, "a")
                        booking_url = booking_link.get_attribute("href")
                    except:
                        booking_url = None

                    flight = Flight(
                        departure_airport=dep_airport,
                        arrival_airport=arr_airport,
                        departure_date=departure_date,
                        return_date=return_date,
                        price_usd=price,
                        points=points,
                        airline=airline,
                        cabin_class=cabin,
                        stops=stops,
                        booking_url=booking_url
                    )

                    flights.append(flight)

                except Exception as e:
                    # Skip flights we can't parse
                    continue

        except Exception as e:
            print(f"  ✗ Error parsing results: {e}")

        return flights

    def close(self):
        """Clean up Selenium resources."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("✓ WebDriver closed")
