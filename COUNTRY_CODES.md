# Country Codes Reference

## What Are Country Codes?

The system uses **ISO 3166-1 alpha-2** country codes - the standard 2-letter codes used worldwide.

These are the same codes you see in:
- Domain names (.us, .jp, .uk)
- Olympic broadcasts (USA, JPN, KOR)
- International shipping
- Airline booking systems

## Currently Supported Countries

### North America
| Code | Country | Airports |
|------|---------|----------|
| **US** | United States | 21 airports (JFK, LAX, SFO, ORD, etc.) |
| **CA** | Canada | 4 airports (YYZ, YVR, YUL, YYC) |
| **MX** | Mexico | 2 airports (MEX, CUN) |

### Asia
| Code | Country | Airports |
|------|---------|----------|
| **JP** | Japan | 5 airports (NRT, HND, KIX, NGO, FUK) |
| **KR** | South Korea | 2 airports (ICN, GMP) |
| **TW** | Taiwan | 1 airport (TPE) |
| **CN** | China | 4 airports (PVG, PEK, CAN, HKG) |
| **HK** | Hong Kong | 1 airport (HKG) |
| **SG** | Singapore | 1 airport (SIN) |
| **TH** | Thailand | 2 airports (BKK, HKT) |
| **IN** | India | 3 airports (DEL, BOM, BLR) |

### Europe
| Code | Country | Airports |
|------|---------|----------|
| **GB** | United Kingdom | 3 airports (LHR, LGW, MAN) |
| **FR** | France | 2 airports (CDG, ORY) |
| **DE** | Germany | 2 airports (FRA, MUC) |
| **NL** | Netherlands | 1 airport (AMS) |
| **ES** | Spain | 2 airports (MAD, BCN) |
| **IT** | Italy | 2 airports (FCO, MXP) |
| **CH** | Switzerland | 1 airport (ZRH) |

### Oceania
| Code | Country | Airports |
|------|---------|----------|
| **AU** | Australia | 3 airports (SYD, MEL, BNE) |
| **NZ** | New Zealand | 1 airport (AKL) |

### Middle East
| Code | Country | Airports |
|------|---------|----------|
| **AE** | UAE | 2 airports (DXB, AUH) |
| **QA** | Qatar | 1 airport (DOH) |

### South America
| Code | Country | Airports |
|------|---------|----------|
| **BR** | Brazil | 2 airports (GRU, GIG) |
| **AR** | Argentina | 1 airport (EZE) |

## Common Country Codes (Quick Reference)

```
US = United States       JP = Japan              GB = United Kingdom
CA = Canada              KR = South Korea        FR = France
MX = Mexico              CN = China              DE = Germany
                         TW = Taiwan             IT = Italy
                         SG = Singapore          ES = Spain
                         TH = Thailand           NL = Netherlands
                         IN = India              CH = Switzerland

AU = Australia           BR = Brazil
NZ = New Zealand         AR = Argentina

AE = UAE
QA = Qatar
```

## How to Use in Configuration

### Example 1: US → Asia
```yaml
search:
  departure_countries:
    - "US"
  arrival_countries:
    - "JP"
    - "KR"
    - "TW"
```

This searches: All US airports → All Japan/Korea/Taiwan airports

### Example 2: North America → Europe
```yaml
search:
  departure_countries:
    - "US"
    - "CA"
  arrival_countries:
    - "GB"
    - "FR"
    - "DE"
```

This searches: US + Canada airports → UK/France/Germany airports

### Example 3: Specific Region
```yaml
search:
  departure_countries:
    - "US"
  arrival_countries:
    - "SG"
    - "TH"
```

This searches: US airports → Singapore/Thailand

## Adding New Countries

If you need a country not listed, you can add it in `src/country_airports.py`:

```python
COUNTRY_AIRPORTS = {
    # ... existing countries ...

    # Add your country
    "VN": [  # Vietnam
        "SGN",  # Ho Chi Minh City
        "HAN",  # Hanoi
    ],
}
```

Country code format:
- Must be 2 letters (ISO 3166-1 alpha-2)
- Uppercase (though code accepts lowercase too)
- Standard international codes

## Find Country Codes

**Official list**: [ISO 3166-1 alpha-2 codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

**Common lookups**:
- Vietnam: VN
- Philippines: PH
- Malaysia: MY
- Indonesia: ID
- Portugal: PT
- Greece: GR
- Turkey: TR
- South Africa: ZA
- Peru: PE
- Chile: CL
- Colombia: CO

## Special Cases

### Hong Kong vs China
- **HK** = Hong Kong (separate from CN)
- **CN** = Mainland China

### United Kingdom
- **GB** = Great Britain/United Kingdom
- Not UK (though UK is sometimes used)

### Switzerland
- **CH** = Switzerland (from Latin: Confoederatio Helvetica)
- Not SW or SZ

## Airport Code Reference

If you want to see all airports for a country:

```bash
python src/test_country_search.py
```

Or in Python:
```python
from country_airports import get_airports_for_country

us_airports = get_airports_for_country("US")
print(us_airports)
# ['JFK', 'EWR', 'LGA', 'BOS', 'PHL', ...]
```

## Summary

✅ Country codes are **ISO 3166-1 alpha-2** (standard 2-letter codes)
✅ Same codes used globally (domains, shipping, Olympics)
✅ Currently **26 countries** with **80+ major airports** supported
✅ Easy to add more countries in `src/country_airports.py`
✅ Use them in `config/settings.yaml` for flexible searches

**Your current config**:
- Departure: **US** (21 airports)
- Arrival: **JP**, **KR** (7 airports)
- Total: 147 route combinations
