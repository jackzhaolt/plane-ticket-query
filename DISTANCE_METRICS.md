# Distance-Based Deal Detection

## Overview

The system now uses **distance efficiency** (miles per point) as a key metric for evaluating award flight deals - the gold standard for points travelers!

## Why Distance Matters

For award flights, **miles per point** is often more important than absolute price or even cents per point:

```
❌ BAD:  JFK → LAX (2,470 mi) for 50,000 points = 0.049 mi/pt
✅ GOOD: JFK → NRT (6,730 mi) for 60,000 points = 0.112 mi/pt
⭐ GREAT: JFK → NRT (6,730 mi) for 45,000 points = 0.150 mi/pt
```

**Why?** You're "paying" 50k points either way, but one gets you 10,000 miles of travel while the other gets you only 2,500 miles!

## How It Works

### 1. Distance Calculation

Uses **Haversine formula** to calculate great circle distance between airports:

```python
JFK (40.64°N, 73.78°W) → NRT (35.77°N, 140.39°E) = 6,730 miles
```

**Airport database includes 50+ major airports:**
- US: JFK, LAX, SFO, ORD, ATL, MIA, etc.
- Asia: NRT, HND, ICN, PVG, HKG, SIN, etc.
- Europe: LHR, CDG, FRA, AMS, etc.
- More can be easily added

### 2. Deal Evaluation

Three metrics now considered:

| Metric | Formula | Good Value | Best For |
|--------|---------|------------|----------|
| **Cash Price** | Absolute $ | < $800 | Budget travelers |
| **Cents per Point** | (price × 100) / points | > 1.5¢ | General value |
| **Miles per Point** | distance / points | > 0.05 | Award flights ⭐ |

A flight is a "good deal" if it meets **ANY** of these thresholds.

### 3. Ranking Algorithm

Flights ranked by composite score:

```python
score = price_score + cpp_score + (miles_per_point × 10000) + direct_bonus
```

**Miles per point is weighted heavily** because it's the most important metric for award travel!

### 4. Deal Quality Indicators

```
⭐⭐⭐ EXCEPTIONAL: 0.15+ miles/point
  Example: 6,800 mi for 45k pts
  This is what you should aim for!

⭐⭐ GREAT: 0.10+ miles/point
  Example: 6,800 mi for 68k pts
  Still excellent value

⭐ GOOD: 0.05+ miles/point
  Example: 6,800 mi for 136k pts
  Acceptable for hard-to-book routes

❌ Poor: <0.05 miles/point
  Example: 2,500 mi for 50k pts
  Save your points!
```

## Configuration

### Adjust Thresholds

Edit `config/settings.yaml`:

```yaml
deals:
  # Traditional thresholds
  max_cash_price: 800
  max_points: 60000
  min_cpp: 1.5

  # Distance efficiency (NEW!)
  min_miles_per_point: 0.05  # Minimum acceptable ratio

  # Increase for stricter filtering:
  # 0.08 = Good deals only
  # 0.10 = Great deals only
  # 0.15 = Exceptional deals only
```

### Real-World Examples

| Route | Distance | Points | Mi/Pt | Rating | Notes |
|-------|----------|--------|-------|--------|-------|
| JFK → NRT | 6,730 | 45,000 | 0.150 | ⭐⭐⭐ | Sweet spot! |
| LAX → HKG | 7,248 | 60,000 | 0.121 | ⭐⭐ | Great value |
| SFO → SIN | 8,439 | 85,000 | 0.099 | ⭐⭐ | Good for premium |
| ORD → LHR | 3,943 | 60,000 | 0.066 | ⭐ | OK for Europe |
| JFK → LAX | 2,470 | 50,000 | 0.049 | ❌ | Poor - save points! |

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
Distance Efficiency: 0.150 miles per point
  ⭐⭐⭐ EXCEPTIONAL value!
```

## Adding New Airports

To add airports not in the database:

```python
# In src/distance_calculator.py

AIRPORT_COORDINATES = {
    "CODE": (latitude, longitude),
    # Example:
    "TPE": (25.0777, 121.2328),  # Taipei
}
```

Or use the helper function:

```python
from distance_calculator import add_airport
add_airport("TPE", 25.0777, 121.2328)
```

## Understanding the Math

### Example: JFK → Tokyo

**Option A: 45,000 points**
```
Distance: 6,730 miles
Points: 45,000
Miles per point: 6,730 / 45,000 = 0.150

Rating: ⭐⭐⭐ EXCEPTIONAL
Take this deal immediately!
```

**Option B: 80,000 points**
```
Distance: 6,730 miles
Points: 80,000
Miles per point: 6,730 / 80,000 = 0.084

Rating: ⭐ GOOD
OK, but wait for better if not urgent
```

**Option C: Domestic for same points**
```
Distance: 2,470 miles (JFK → LAX)
Points: 45,000
Miles per point: 2,470 / 45,000 = 0.055

Rating: ⭐ Marginal
Better to use cash for domestic
```

### Why This Matters

**Scenario**: You have 100,000 points to spend

**Option 1**: Two domestic flights (25k each)
- 2 × 2,500 miles = 5,000 miles of travel

**Option 2**: One international flight (50k)
- 1 × 6,800 miles = 6,800 miles of travel

**Option 2 gives you 36% more travel for the same points!**

## Transfer Partners Context

Different airlines have different sweet spots:

```yaml
# Examples of good redemptions by partner:

ANA (transfer from Amex):
  - JFK → NRT: 45k points (0.15 mi/pt) ⭐⭐⭐
  - Round trip business: 88k points

Virgin Atlantic (transfer from Amex):
  - JFK → LHR: 50k points (0.07 mi/pt) ⭐

Delta (transfer from Amex):
  - Varies widely
  - Best for domestic + international combos
```

## Strategy Tips

### 1. Long-Haul = Best Value
Focus searches on:
- US ↔ Asia (6,000-8,000 miles)
- US ↔ Europe (3,500-5,500 miles)
- US ↔ South America (4,000-5,500 miles)

### 2. Avoid Points for Domestic
Unless:
- Last-minute booking (cash prices high)
- Peak travel (holidays)
- No availability otherwise

### 3. Sweet Spots to Target

| Route Type | Target Mi/Pt | Example |
|------------|--------------|---------|
| US-Asia | 0.12+ | JFK-NRT for 55k |
| US-Europe | 0.08+ | ORD-LHR for 50k |
| US-Australia | 0.10+ | LAX-SYD for 80k |
| Domestic | 0.08+ | Usually not worth it |

### 4. Business Class Value

Business class long-haul can have **exceptional** mi/pt:

```
JFK → NRT Business: 85,000 points
Distance: 6,730 miles
Mi/Pt: 0.079 (⭐ Good)

BUT: Cash price = $4,500
CPP: 5.3¢ per point (⭐⭐⭐ Exceptional!)
```

Use **both** metrics to find true deals!

## Integration with Hybrid System

Distance metrics work with **all search modes**:

- **API Mode**: Estimates points, calculates distance
- **Selenium Mode**: Real points from Amex, exact distance
- **Hybrid Mode**: Combines both for best accuracy

## Testing

```bash
# Test distance calculations
python src/test_distance.py

# Test with demo data
python src/test_demo.py  # Now includes distance metrics!

# Test hybrid with real searches
python src/test_hybrid.py
```

## Summary

✅ **Calculates real flight distances** using Haversine formula
✅ **Evaluates miles-per-point** ratio for award efficiency
✅ **Ranks by distance efficiency** (heavily weighted)
✅ **Shows deal quality** (⭐⭐⭐ = exceptional)
✅ **Configurable thresholds** in settings.yaml
✅ **50+ airports included**, easily extensible
✅ **Works with all search modes** (API, Selenium, Hybrid)

**This is the metric serious points travelers use!** 🎯
