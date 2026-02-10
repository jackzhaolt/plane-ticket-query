# Award Chart-Based Deal Detection

## Overview

The system now uses **real award chart logic** based on distance bands - exactly how airlines price award tickets! This is far more accurate than simple point thresholds.

## How Airline Award Charts Work

Airlines price award tickets based on **distance flown**, not just destination:

```
Traditional Method (Simple):
  ❌ "Any flight under 60k points is good"
  Problem: 2,500 miles for 50k points = bad deal
           6,800 miles for 60k points = great deal!

Award Chart Method (Smart):
  ✅ "6,800 miles should cost 75k-90k economy"
  60k points = EXCEPTIONAL (40% below standard!)
  50k points for 2,500 miles = FAIR (within 55k-69k range)
```

## Distance Bands

### Standard Award Chart

Based on your examples:

| Distance Range | Economy | Premium Economy | Business | First |
|----------------|---------|-----------------|----------|-------|
| **0-5,000 mi** | 55k-69k | 75k-95k | 110k-140k | 165k-210k |
| **5,001-7,500 mi** | 75k-90k | 100k-120k | 150k-180k | 225k-270k |
| **7,501-11,000 mi** | 87.5k-103.5k | 120k-145k | 175k-210k | 262k-315k |
| **11,001-15,000 mi** | 110k-132k | 150k-180k | 220k-264k | 330k-396k |

### Real-World Examples

| Route | Distance | Band | Expected (Econ) | Good Deal |
|-------|----------|------|-----------------|-----------|
| JFK → LAX | 2,470 | 0-5k | 55k-69k | < 58k |
| JFK → LHR | 3,443 | 0-5k | 55k-69k | < 58k |
| JFK → NRT | 6,730 | 5k-7.5k | 75k-90k | < 80k |
| LAX → HKG | 7,248 | 5k-7.5k | 75k-90k | < 80k |
| SFO → SIN | 8,439 | 7.5k-11k | 87.5k-103.5k | < 93k |
| ORD → SYD | 9,272 | 7.5k-11k | 87.5k-103.5k | < 93k |

## Deal Quality Ratings

The system evaluates each flight and assigns a rating:

### ⭐⭐⭐ EXCEPTIONAL
**Below the minimum of the range**

```
Example: JFK → NRT (6,730 miles)
Expected: 75,000-90,000 points
Found: 45,000 points
Rating: ⭐⭐⭐ EXCEPTIONAL (40% below minimum!)

Action: BOOK IMMEDIATELY!
```

### ⭐⭐ GREAT
**Lower third of the range**

```
Example: JFK → NRT (6,730 miles)
Expected: 75,000-90,000 points
Found: 78,000 points
Rating: ⭐⭐ GREAT (Low end of range)

Action: Excellent value, book if dates work
```

### ⭐ GOOD
**Middle third of the range**

```
Example: JFK → NRT (6,730 miles)
Expected: 75,000-90,000 points
Found: 82,000 points
Rating: ⭐ GOOD (Mid-range pricing)

Action: Fair standard pricing
```

### 😐 FAIR
**Upper third of the range**

```
Example: JFK → NRT (6,730 miles)
Expected: 75,000-90,000 points
Found: 88,000 points
Rating: 😐 FAIR (High end of range)

Action: Wait for better if not urgent
```

### ❌ POOR
**Above the maximum of the range**

```
Example: JFK → NRT (6,730 miles)
Expected: 75,000-90,000 points
Found: 110,000 points
Rating: ❌ POOR (22% above maximum!)

Action: DO NOT BOOK - terrible value
```

## Configuration

### config/settings.yaml

```yaml
deals:
  # Award Chart Settings (PRIMARY)
  use_award_chart: true  # Enable award chart evaluation
  award_chart: "standard"  # Which chart to use
  award_chart_min_quality: "good"  # Minimum quality to accept

  # Options for award_chart_min_quality:
  # "exceptional" - Only show exceptional deals
  # "great"       - Show great or better
  # "good"        - Show good or better (recommended)
  # "fair"        - Show fair or better
```

### Quality Thresholds

Adjust `award_chart_min_quality` based on your flexibility:

| Setting | What You Get | Best For |
|---------|--------------|----------|
| `exceptional` | Only sub-minimum pricing | Wait for perfect deals |
| `great` | Low end of range | Patient, flexible dates |
| `good` | Standard pricing | Most travelers |
| `fair` | High end of range | Need to book soon |

## Available Award Charts

### 1. Standard (Default)
Based on typical airline award pricing:
```yaml
award_chart: "standard"
```

Uses the distance bands you provided as examples.

### 2. ANA Mileage Club
Real ANA award chart:
```yaml
award_chart: "ana"
```

Optimized for:
- Japan routes (JFK/LAX → NRT/HND)
- Star Alliance partners
- Known for excellent value

Example: JFK → NRT economy for 50k-60k (vs 75k-90k standard)

### 3. Delta SkyMiles
Dynamic pricing ranges:
```yaml
award_chart: "delta"
```

Note: Delta has no fixed chart, but we use typical observed ranges.

### Adding Custom Charts

Edit `src/award_charts.py`:

```python
CUSTOM_CHART = AwardChart(
    name="My Custom Chart",
    distance_bands=[
        {
            'min_miles': 0,
            'max_miles': 5000,
            'economy': {'min': 50000, 'max': 65000},
            'business': {'min': 100000, 'max': 130000},
        },
        # Add more bands...
    ]
)

# Register it
AWARD_CHARTS['custom'] = CUSTOM_CHART
```

## Alert Format

When a deal is found, you'll see:

```
🎉 GREAT DEAL FOUND!

Route: JFK → NRT (6,730 miles)
Date: 2026-07-15
Airline: NH (ANA)
Class: ECONOMY
Stops: Direct

Price: $650.00 USD
Points: 45,000 (1.44¢ per point)

Award Chart Analysis (standard):
  Expected Range: 75,000-90,000 points
  This Flight: 45,000 points
  Rating: ⭐⭐⭐ EXCEPTIONAL - 40% below standard minimum (75,000 pts)
  Distance Efficiency: 0.150 miles/point
```

## Understanding the Math

### Example 1: JFK → NRT (6,730 miles)

**Falls in band: 5,001-7,500 miles**
- Expected economy: 75,000-90,000 points

**Option A: 45,000 points**
```
45,000 vs 75,000-90,000
Below minimum by: 30,000 points (40%)
Rating: ⭐⭐⭐ EXCEPTIONAL
Action: BOOK NOW!
```

**Option B: 78,000 points**
```
78,000 vs 75,000-90,000
Position: 3,000 into 15,000 range = lower 20%
Rating: ⭐⭐ GREAT
Action: Good deal, book if dates work
```

**Option C: 110,000 points**
```
110,000 vs 75,000-90,000
Above maximum by: 20,000 points (22%)
Rating: ❌ POOR
Action: Wait or use cash
```

### Example 2: JFK → LAX (2,470 miles)

**Falls in band: 0-5,000 miles**
- Expected economy: 55,000-69,000 points

**Option A: 50,000 points**
```
50,000 vs 55,000-69,000
Below minimum by: 5,000 points (9%)
Rating: ⭐⭐⭐ EXCEPTIONAL
Action: Great domestic deal
```

**Option B: 60,000 points**
```
60,000 vs 55,000-69,000
Position: 5,000 into 14,000 range = middle 36%
Rating: ⭐ GOOD
Action: Standard pricing
```

## Why This is Better

### Before (Simple Threshold)
```yaml
max_points: 60000  # Any flight under 60k is good
```

**Problems:**
- JFK → LAX (2,470 mi) for 60k = Not great (should be 55k)
- JFK → NRT (6,730 mi) for 60k = AMAZING (should be 75k-90k!)
- Treats all flights the same regardless of distance

### After (Award Chart)
```yaml
use_award_chart: true
award_chart: "standard"
```

**Benefits:**
- JFK → LAX for 60k = ⭐ GOOD (mid-range of 55k-69k)
- JFK → NRT for 60k = ⭐⭐⭐ EXCEPTIONAL (40% below 75k-90k!)
- Treats each flight based on distance traveled

**Result: Find truly exceptional long-haul deals!**

## Strategy Tips

### 1. Focus on Long-Haul
Long-haul international flights in the 5k-11k mile bands offer the best value:

```
Sweet spot: 6,000-8,000 miles
Example routes:
  - US East Coast → Asia (JFK/EWR → NRT/HND/ICN)
  - US West Coast → Asia (LAX/SFO → HKG/SIN/BKK)
  - US → Europe (Various)
```

### 2. Watch for Sub-Minimum Pricing
⭐⭐⭐ EXCEPTIONAL deals (below range minimum) are rare - grab them!

```
These happen when:
  - Airlines have promotions
  - Off-peak dates
  - Less popular routes
  - Last-minute availability
```

### 3. Business Class Sweet Spots
Business class uses the same distance bands but higher ranges:

```
JFK → NRT (6,730 miles)
Economy: 75k-90k → Great at < 80k
Business: 150k-180k → Great at < 160k

Business sweet spot: ~1.8-2x economy pricing
If you find business for 2x economy or less = BOOK IT!
```

### 4. Avoid Poor Deals
❌ Flights above range maximum are almost never worth it:

```
Better to:
  - Use cash
  - Wait for better availability
  - Try different dates
  - Consider alternative routes
```

## Integration with System

### Works with All Search Modes
- **API Mode**: Estimates points, evaluates against chart
- **Selenium Mode**: Real Amex points, exact chart evaluation
- **Hybrid Mode**: Best of both worlds

### Automatic Filtering
System automatically:
1. Calculates flight distance
2. Determines which distance band applies
3. Gets expected point range for cabin class
4. Evaluates actual points vs expected
5. Assigns quality rating
6. Filters based on `award_chart_min_quality`
7. Ranks deals (exceptional first)

### Testing

```bash
# Test award chart evaluation
python src/award_charts.py

# Test with full system
python src/test_award_chart.py

# Test with demo data
python src/test_demo.py
```

## Comparison: Old vs New

### Old Method
```
Simple threshold: max_points: 60000

JFK → LAX (2,470 mi) for 60k: ✅ (but not great value)
JFK → NRT (6,730 mi) for 60k: ✅ (AMAZING value!)
JFK → NRT (6,730 mi) for 110k: ❌ (correctly rejected)
```

### New Method (Award Chart)
```
Distance-based evaluation:

JFK → LAX (2,470 mi) for 60k: ⭐ GOOD
  Expected: 55k-69k, you're at mid-range

JFK → NRT (6,730 mi) for 60k: ⭐⭐⭐ EXCEPTIONAL!
  Expected: 75k-90k, you're 20% below minimum!

JFK → NRT (6,730 mi) for 110k: ❌ POOR
  Expected: 75k-90k, you're 22% above maximum!
```

**The award chart method finds truly exceptional deals and avoids overpaying!**

## Summary

✅ **Distance-based award chart bands** (just like real airlines)
✅ **Quality ratings** (Exceptional, Great, Good, Fair, Poor)
✅ **Multiple airline charts** (Standard, ANA, Delta)
✅ **Configurable thresholds** (set minimum quality)
✅ **Smart filtering** (only show deals you want)
✅ **Proper ranking** (best deals first)
✅ **Works with all search modes** (API, Selenium, Hybrid)

**This is how professional award travel experts evaluate deals!** 🎯
