# Hybrid Flight Search System

## Overview

The system now uses an **intelligent hybrid approach** that combines the speed of APIs with the accuracy of web scraping for the best of both worlds.

```
┌─────────────────────────────────────────────────────────┐
│              HYBRID SEARCH STRATEGY                      │
└─────────────────────────────────────────────────────────┘

Step 1: FAST API SCREENING (Amadeus)
  ↓
  ├─ Search 100s of flights in seconds
  ├─ Get general cash prices
  ├─ Estimate points value
  └─ Identify promising routes
       ↓
       [Found deals under $1000?]
       ↓
Step 2: DEEP AMEX SCRAPING (Selenium)
  ↓
  ├─ Navigate to Amex Travel website
  ├─ Search specific routes from Step 1
  ├─ Extract ACTUAL Amex points pricing
  ├─ Get exact availability
  └─ Cache results (6 hours)
       ↓
Step 3: INTELLIGENT COMBINATION
  ↓
  ├─ Merge API + Selenium results
  ├─ Deduplicate flights
  ├─ Prefer Selenium data (more accurate)
  ├─ Rank by best value
  └─ Send alerts
```

## How It Works

### Phase 1: Fast API Screening
**Purpose**: Quickly scan for general availability
**Speed**: 10-30 seconds for 10 routes
**Data Source**: Amadeus API
**Frequency**: Every hour (or configured interval)

```python
# Amadeus checks for:
- Available flights
- Cash prices
- Basic availability
- Cabin classes

# Output:
"Found 50 flights, 5 under $800"
```

### Phase 2: Intelligent Decision
**Purpose**: Decide if deeper scraping is worth it
**Logic**:
```python
if found_cheap_flights:
    trigger_selenium_scraping()
elif not_scraped_in_7_days:
    trigger_selenium_scraping()
else:
    use_api_results_only()
```

### Phase 3: Deep Amex Scraping
**Purpose**: Get exact Amex points pricing
**Speed**: 2-5 minutes per route
**Data Source**: Amex Travel website (Selenium)
**Frequency**: As needed (cached for 6 hours)

```python
# Amex Travel scraping gets:
- Exact Amex points pricing (KEY!)
- Member-only deals
- Transfer partner availability
- Direct booking links

# Output:
"JFK→NRT: $650 or 45,000 Amex points"
```

### Phase 4: Smart Combination
**Purpose**: Combine both data sources intelligently
**Logic**:
```python
# Deduplication rules:
- Same flight found in both sources → Use Selenium data
- Flight only in API → Use API data
- Flight only in Selenium → Use Selenium data

# Ranking:
- Best points value first
- Direct flights preferred
- Lower prices preferred
```

## Configuration

### Enable Hybrid Mode

Edit `config/settings.yaml`:

```yaml
searcher:
  type: "hybrid"  # Enable hybrid mode

  hybrid:
    use_selenium: true  # Enable Selenium scraping
    selenium_headless: true  # Run browser in background
    cache_expiry_hours: 6  # Cache Selenium results

    trigger_conditions:
      max_api_price: 1000  # Trigger Selenium if API finds flights under $1000
      check_frequency: "weekly"  # How often to do deep checks
```

### Searcher Modes

You can force specific modes:

```python
# In code:
flights = searcher.search(..., mode="auto")     # Smart hybrid (default)
flights = searcher.search(..., mode="api")      # API only (fast)
flights = searcher.search(..., mode="selenium") # Selenium only (accurate)
```

```yaml
# In config:
searcher:
  type: "api"       # API only
  type: "selenium"  # Selenium only
  type: "hybrid"    # Smart hybrid (recommended)
```

## Benefits of Hybrid Approach

| Feature | API Only | Selenium Only | Hybrid |
|---------|----------|---------------|--------|
| **Speed** | ⚡ Very Fast | 🐌 Slow | ⚡🐌 Balanced |
| **Amex Points** | ❌ Estimated | ✅ Exact | ✅ Exact |
| **Coverage** | ✅ Broad | ⚠️ Limited | ✅ Broad |
| **Cost** | 💰 API calls | 🆓 Free | 💰 Minimal |
| **Reliability** | ✅ Stable | ⚠️ Fragile | ✅ Resilient |
| **Frequency** | ✅ Hourly | ❌ Daily max | ✅ Flexible |

## Usage Examples

### Daily Monitoring (Recommended)
```python
# config/settings.yaml
alerts:
  check_interval: 60  # Check every hour

searcher:
  type: "hybrid"
  hybrid:
    use_selenium: true
    trigger_conditions:
      max_api_price: 800  # Only scrape if API finds deals
```

**Result**:
- Checks 24x/day with API (fast)
- Scrapes Amex 1-2x/day when deals found (accurate)
- Best of both worlds!

### API-Only Mode (Fast & Frequent)
```python
# config/settings.yaml
searcher:
  type: "api"

alerts:
  check_interval: 30  # Check every 30 minutes
```

**Use When**:
- Testing the system
- Don't need exact Amex points yet
- Want maximum speed
- Just tracking price trends

### Selenium-Only Mode (Accuracy First)
```python
# config/settings.yaml
searcher:
  type: "selenium"

alerts:
  check_interval: 360  # Check every 6 hours
```

**Use When**:
- Only care about Amex points pricing
- Don't have Amadeus API key
- Can wait longer between checks
- Want exact booking links

### One-Time Deep Search
```bash
# Force deep Selenium scraping once
python src/main.py --once --mode selenium
```

## Caching Strategy

Selenium results are cached to avoid redundant scraping:

```python
# Cache key: route + date
"JFK-NRT_2026-06-15" → cached for 6 hours

# Next search within 6 hours:
✓ Use cached data (instant)

# After 6 hours:
↻ Re-scrape for fresh data
```

**Cache location**: `/tmp/flight_cache/`

Clear cache:
```bash
rm -rf /tmp/flight_cache/*
```

## Setting Up Selenium

The Selenium scraper is **90% ready** but needs customization for Amex Travel:

### Quick Start
1. Read `AMEX_SCRAPING_GUIDE.md` (detailed instructions)
2. Visit Amex Travel website
3. Inspect HTML elements (F12 in browser)
4. Update selectors in `src/searchers/amex_selenium_searcher.py`
5. Test with: `python src/test_selenium.py`

### Key Selectors to Find
- [ ] Search form fields (origin, destination, dates)
- [ ] Search submit button
- [ ] Result cards/containers
- [ ] **Price in points** (most important!)
- [ ] Price in cash
- [ ] Airline, stops, cabin class
- [ ] Booking links

See `AMEX_SCRAPING_GUIDE.md` for detailed steps.

## Optional: Amex Login

Add credentials to `.env` for member-only pricing:

```bash
AMEX_USERNAME=your_amex_username
AMEX_PASSWORD=your_amex_password
```

**Benefits**:
- See member-exclusive deals
- Personalized point values
- Your specific transfer partners

**Note**: Use at your own risk. Consider security implications.

## Monitoring Strategy

### Recommended Setup

```yaml
# config/settings.yaml

# Daily monitoring
alerts:
  check_interval: 60  # Every hour

searcher:
  type: "hybrid"
  hybrid:
    use_selenium: true
    trigger_conditions:
      max_api_price: 1000

# Target specific dates
search:
  date_ranges:
    - start: "2026-06-01"
      end: "2026-08-31"
```

**Result**:
- 24 API checks/day (fast screening)
- 2-3 Selenium scrapes/day (when deals found)
- Alerts sent immediately when good deals appear

### Cost-Effective Setup

```yaml
# Minimize API calls, maximize accuracy

searcher:
  type: "hybrid"
  hybrid:
    use_selenium: true

alerts:
  check_interval: 360  # Every 6 hours
```

**Result**:
- 4 API checks/day
- 1-2 Selenium scrapes/day
- Still catches most deals

## Troubleshooting

### "No flights found"
1. Check API credentials in `.env`
2. Try `mode="api"` to test API separately
3. Try `mode="selenium"` to test scraping separately

### Selenium not working
1. Customize selectors (see `AMEX_SCRAPING_GUIDE.md`)
2. Run with `headless=False` to watch browser
3. Check screenshots in `/tmp/`

### Too slow
1. Reduce Selenium frequency
2. Increase cache expiry time
3. Use API-only mode during testing

### API rate limits
1. Reduce check frequency
2. Limit airport combinations
3. Use Selenium-only mode

## Summary

The hybrid system gives you:

✅ **Speed**: Fast API checks every hour
✅ **Accuracy**: Exact Amex points when needed
✅ **Efficiency**: Smart caching avoids redundant work
✅ **Flexibility**: Use API, Selenium, or both
✅ **Reliability**: Falls back if one source fails

**Best for**: Finding Amex points deals without constant manual checking!
