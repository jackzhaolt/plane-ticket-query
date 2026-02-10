# Amex Travel Scraping Customization Guide

The Selenium scraper for Amex Travel (`src/searchers/amex_selenium_searcher.py`) is a **template** that needs customization based on the actual Amex Travel website structure.

## Why Customization is Needed

Websites frequently change their HTML structure, CSS classes, and element IDs. The current implementation uses **placeholder selectors** that need to be updated with the actual selectors from Amex Travel.

## How to Customize

### Step 1: Inspect the Amex Travel Website

1. Go to [travel.americanexpress.com](https://travel.americanexpress.com)
2. Open Chrome DevTools (F12 or right-click → Inspect)
3. Navigate to the flights search page
4. Identify the actual HTML elements:
   - Search form fields (origin, destination, dates)
   - Submit button
   - Result cards
   - Price elements (cash and points!)
   - Airline, stops, cabin class info

### Step 2: Update Selectors

In `src/searchers/amex_selenium_searcher.py`, update these sections:

#### Form Fields (in `_search_route` method)

```python
# Current (PLACEHOLDER):
origin_field = self.driver.find_element(By.ID, "flight-origin")

# Update to actual selector:
origin_field = self.driver.find_element(By.ID, "actual-origin-field-id")
# Or by CSS selector:
origin_field = self.driver.find_element(By.CSS_SELECTOR, ".origin-input")
# Or by XPath:
origin_field = self.driver.find_element(By.XPATH, "//input[@name='origin']")
```

#### Result Parsing (in `_parse_results` method)

```python
# Current (PLACEHOLDER):
flight_elements = self.driver.find_elements(By.CLASS_NAME, "flight-result")

# Update to actual selector:
flight_elements = self.driver.find_elements(By.CSS_SELECTOR, ".flight-card")
# Or:
flight_elements = self.driver.find_elements(By.XPATH, "//div[@data-testid='flight-option']")
```

#### Price Extraction (MOST IMPORTANT for Amex Points!)

```python
# Cash price (update selector):
price_elem = element.find_element(By.CLASS_NAME, "actual-price-class")
price_text = price_elem.text.replace('$', '').replace(',', '')

# POINTS PRICE (this is the key feature!):
points_elem = element.find_element(By.CLASS_NAME, "actual-points-class")
points_text = points_elem.text.replace(',', '').replace(' points', '')
points = int(points_text)
```

### Step 3: Test and Debug

```bash
# Run with headless=False to see what's happening:
python -c "
from src.searchers.amex_selenium_searcher import AmexTravelSearcher
searcher = AmexTravelSearcher(headless=False)
# Watch the browser and see where it fails
"
```

### Step 4: Handle Dynamic Content

Amex Travel likely uses JavaScript to load results. You may need:

```python
# Wait for specific elements to appear
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait up to 30 seconds for results
WebDriverWait(self.driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "actual-result-class"))
)
```

## Common Selector Methods

| Method | When to Use | Example |
|--------|-------------|---------|
| `By.ID` | Element has unique ID | `By.ID, "search-button"` |
| `By.CLASS_NAME` | Single class name | `By.CLASS_NAME, "price"` |
| `By.CSS_SELECTOR` | Complex selectors | `By.CSS_SELECTOR, ".flight .price"` |
| `By.XPATH` | Complex navigation | `By.XPATH, "//div[@data-test='price']"` |
| `By.NAME` | Form inputs | `By.NAME, "departureDate"` |
| `By.TAG_NAME` | Generic elements | `By.TAG_NAME, "button"` |

## Finding the Right Selectors

### Method 1: Chrome DevTools
1. Right-click element → Inspect
2. In DevTools, right-click HTML element
3. Copy → Copy selector / Copy XPath
4. Test in console: `document.querySelector('your-selector')`

### Method 2: Browser Console
```javascript
// Test selectors in browser console:
document.getElementById('flight-origin')
document.querySelector('.price-points')
document.querySelectorAll('.flight-result')
```

### Method 3: Selenium Testing
```python
# Try different selectors until one works:
try:
    element = driver.find_element(By.ID, "test-id")
except:
    try:
        element = driver.find_element(By.CLASS_NAME, "test-class")
    except:
        element = driver.find_element(By.XPATH, "//div[@test]")
```

## Key Things to Find

### 1. Search Form
- [ ] Origin airport field
- [ ] Destination airport field
- [ ] Departure date picker
- [ ] Return date picker (if round-trip)
- [ ] Number of passengers
- [ ] Cabin class dropdown
- [ ] Search submit button

### 2. Results Page
- [ ] Result cards/containers
- [ ] Airline name
- [ ] **Cash price** element
- [ ] **Points price** element (CRITICAL!)
- [ ] Departure/arrival times
- [ ] Number of stops
- [ ] Cabin class
- [ ] Booking link/button

### 3. Login (Optional)
- [ ] Login button
- [ ] Username field
- [ ] Password field
- [ ] Submit button

## Example: Real-World Pattern

Here's what you might find on Amex Travel:

```python
# After inspecting the site, you might discover:

# Search form
origin = driver.find_element(By.CSS_SELECTOR, "input[data-testid='origin-input']")
destination = driver.find_element(By.CSS_SELECTOR, "input[data-testid='destination-input']")
search_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='search-flights']")

# Results
flight_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='flight-card']")

for card in flight_cards:
    # Cash price
    price = card.find_element(By.CSS_SELECTOR, ".currency-amount").text

    # Points price (THE IMPORTANT ONE!)
    points = card.find_element(By.CSS_SELECTOR, ".points-amount").text

    # Airline
    airline = card.find_element(By.CSS_SELECTOR, ".airline-code").text
```

## Testing Your Changes

```bash
# Test with a simple search
python src/test_selenium.py
```

Create `src/test_selenium.py`:
```python
from searchers.amex_selenium_searcher import AmexTravelSearcher
from datetime import date, timedelta

searcher = AmexTravelSearcher(headless=False)  # See browser

flights = searcher.search(
    departure_airports=["JFK"],
    arrival_airports=["LAX"],
    departure_date=date.today() + timedelta(days=30),
    adults=1
)

print(f"Found {len(flights)} flights")
for flight in flights:
    print(flight)

searcher.close()
```

## Alternative: Use Playwright MCP

If Selenium is too complex, you can use the **Playwright MCP** that's available in your environment:

```python
# The system has mcp__playwright__ tools available
# which might be easier for complex scraping
```

## Need Help?

If you get stuck:
1. Take screenshots of errors: `driver.save_screenshot("debug.png")`
2. Print page source: `print(driver.page_source)`
3. Check browser console for JavaScript errors
4. Try running with `headless=False` to watch what happens

## Summary

The Selenium scraper is **90% ready** - it just needs you to:
1. Visit Amex Travel website
2. Inspect the HTML elements
3. Update the placeholder selectors with real ones
4. Test and adjust

Once customized, it will give you **accurate Amex points pricing** that no API can provide!
