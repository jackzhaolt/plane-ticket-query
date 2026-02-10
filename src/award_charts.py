"""Award chart definitions for different airlines and loyalty programs."""

from typing import Dict, List, Optional, Tuple
from enum import Enum


class CabinClass(Enum):
    """Cabin class categories."""
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium_economy"
    BUSINESS = "business"
    FIRST = "first"


class DealQuality(Enum):
    """Deal quality ratings."""
    EXCEPTIONAL = "exceptional"  # Bottom of range or below
    GREAT = "great"              # Lower third of range
    GOOD = "good"                # Middle of range
    FAIR = "fair"                # Upper third of range
    POOR = "poor"                # Above range


class AwardChart:
    """Represents an airline award chart with distance-based pricing."""

    def __init__(self, name: str, distance_bands: List[Dict]):
        """
        Initialize award chart.

        Args:
            name: Chart name (e.g., "ANA", "Delta", "United")
            distance_bands: List of distance band definitions
        """
        self.name = name
        self.distance_bands = sorted(distance_bands, key=lambda x: x['min_miles'])

    def get_expected_points(
        self,
        distance: float,
        cabin_class: str = "ECONOMY"
    ) -> Optional[Tuple[int, int]]:
        """
        Get expected point range for a flight distance.

        Args:
            distance: Flight distance in miles
            cabin_class: Cabin class

        Returns:
            Tuple of (min_points, max_points) or None if not found
        """
        cabin_key = cabin_class.lower()

        for band in self.distance_bands:
            if band['min_miles'] <= distance <= band['max_miles']:
                points = band.get(cabin_key, band.get('economy'))
                return (points['min'], points['max'])

        return None

    def evaluate_deal(
        self,
        distance: float,
        points: int,
        cabin_class: str = "ECONOMY"
    ) -> Tuple[DealQuality, str]:
        """
        Evaluate if a redemption is a good deal based on award chart.

        Args:
            distance: Flight distance in miles
            points: Points required
            cabin_class: Cabin class

        Returns:
            Tuple of (DealQuality, explanation)
        """
        expected = self.get_expected_points(distance, cabin_class)

        if not expected:
            return DealQuality.FAIR, "Distance not in award chart range"

        min_points, max_points = expected
        range_size = max_points - min_points

        # Calculate position in range (0 = min, 1 = max)
        if points < min_points:
            # Below minimum - exceptional!
            percent_below = ((min_points - points) / min_points) * 100
            return (
                DealQuality.EXCEPTIONAL,
                f"{percent_below:.0f}% below standard minimum ({min_points:,} pts)"
            )
        elif points <= min_points + (range_size * 0.33):
            # Lower third - great deal
            return (
                DealQuality.GREAT,
                f"Low end of range ({min_points:,}-{max_points:,} pts)"
            )
        elif points <= min_points + (range_size * 0.66):
            # Middle third - good deal
            return (
                DealQuality.GOOD,
                f"Mid-range pricing ({min_points:,}-{max_points:,} pts)"
            )
        elif points <= max_points:
            # Upper third - fair
            return (
                DealQuality.FAIR,
                f"High end of range ({min_points:,}-{max_points:,} pts)"
            )
        else:
            # Above maximum - poor deal
            percent_above = ((points - max_points) / max_points) * 100
            return (
                DealQuality.POOR,
                f"{percent_above:.0f}% above standard maximum ({max_points:,} pts)"
            )


# Standard Award Chart (based on common airline charts)
STANDARD_AWARD_CHART = AwardChart(
    name="Standard",
    distance_bands=[
        {
            'min_miles': 0,
            'max_miles': 5000,
            'economy': {'min': 55000, 'max': 69000},
            'premium_economy': {'min': 75000, 'max': 95000},
            'business': {'min': 110000, 'max': 140000},
            'first': {'min': 165000, 'max': 210000},
        },
        {
            'min_miles': 5001,
            'max_miles': 7500,
            'economy': {'min': 75000, 'max': 90000},
            'premium_economy': {'min': 100000, 'max': 120000},
            'business': {'min': 150000, 'max': 180000},
            'first': {'min': 225000, 'max': 270000},
        },
        {
            'min_miles': 7501,
            'max_miles': 11000,
            'economy': {'min': 87500, 'max': 103500},
            'premium_economy': {'min': 120000, 'max': 145000},
            'business': {'min': 175000, 'max': 210000},
            'first': {'min': 262500, 'max': 315000},
        },
        {
            'min_miles': 11001,
            'max_miles': 15000,
            'economy': {'min': 110000, 'max': 132000},
            'premium_economy': {'min': 150000, 'max': 180000},
            'business': {'min': 220000, 'max': 264000},
            'first': {'min': 330000, 'max': 396000},
        },
    ]
)


# ANA Award Chart (example of a real airline)
ANA_AWARD_CHART = AwardChart(
    name="ANA Mileage Club",
    distance_bands=[
        {
            'min_miles': 0,
            'max_miles': 2000,
            'economy': {'min': 12000, 'max': 15000},
            'business': {'min': 25000, 'max': 30000},
        },
        {
            'min_miles': 2001,
            'max_miles': 4000,
            'economy': {'min': 20000, 'max': 25000},
            'business': {'min': 40000, 'max': 50000},
        },
        {
            'min_miles': 4001,
            'max_miles': 6500,
            'economy': {'min': 35000, 'max': 43000},
            'business': {'min': 60000, 'max': 75000},
        },
        {
            'min_miles': 6501,
            'max_miles': 9500,
            'economy': {'min': 50000, 'max': 60000},
            'business': {'min': 85000, 'max': 105000},
        },
    ]
)


# Delta SkyMiles is dynamic, but we can define typical ranges
DELTA_AWARD_CHART = AwardChart(
    name="Delta SkyMiles (Typical)",
    distance_bands=[
        {
            'min_miles': 0,
            'max_miles': 5000,
            'economy': {'min': 45000, 'max': 80000},
            'business': {'min': 100000, 'max': 180000},
        },
        {
            'min_miles': 5001,
            'max_miles': 10000,
            'economy': {'min': 70000, 'max': 120000},
            'business': {'min': 140000, 'max': 250000},
        },
    ]
)


# Chart registry
AWARD_CHARTS: Dict[str, AwardChart] = {
    'standard': STANDARD_AWARD_CHART,
    'ana': ANA_AWARD_CHART,
    'delta': DELTA_AWARD_CHART,
}


def get_award_chart(chart_name: str) -> Optional[AwardChart]:
    """
    Get an award chart by name.

    Args:
        chart_name: Name of the chart (standard, ana, delta, etc.)

    Returns:
        AwardChart or None if not found
    """
    return AWARD_CHARTS.get(chart_name.lower())


def evaluate_redemption(
    distance: float,
    points: int,
    cabin_class: str = "ECONOMY",
    chart_name: str = "standard"
) -> Tuple[DealQuality, str, Optional[Tuple[int, int]]]:
    """
    Evaluate a redemption against an award chart.

    Args:
        distance: Flight distance in miles
        points: Points required
        cabin_class: Cabin class
        chart_name: Award chart to use

    Returns:
        Tuple of (DealQuality, explanation, expected_range)
    """
    chart = get_award_chart(chart_name)

    if not chart:
        return DealQuality.FAIR, "Unknown award chart", None

    quality, explanation = chart.evaluate_deal(distance, points, cabin_class)
    expected = chart.get_expected_points(distance, cabin_class)

    return quality, explanation, expected


# Example usage
if __name__ == "__main__":
    print("Award Chart Evaluation Examples")
    print("="*60)

    test_cases = [
        # (distance, points, cabin, expected_quality)
        (6730, 45000, "ECONOMY", "JFK→NRT"),  # Should be EXCEPTIONAL (below 55k)
        (6730, 60000, "ECONOMY", "JFK→NRT"),  # Should be GOOD (mid-range 55k-69k)
        (6730, 69000, "ECONOMY", "JFK→NRT"),  # Should be FAIR (high end)
        (6730, 80000, "ECONOMY", "JFK→NRT"),  # Should be POOR (above 69k)
        (8500, 90000, "ECONOMY", "SFO→SIN"),  # Should be GREAT (low end 87.5k-103.5k)
        (2470, 50000, "ECONOMY", "JFK→LAX"),  # Should be GOOD
    ]

    for distance, points, cabin, route in test_cases:
        quality, explanation, expected = evaluate_redemption(
            distance, points, cabin, "standard"
        )

        print(f"\n{route} ({distance:,} miles)")
        print(f"  Points: {points:,} {cabin.lower()}")
        if expected:
            print(f"  Expected: {expected[0]:,}-{expected[1]:,} points")
        print(f"  Rating: {quality.value.upper()}")
        print(f"  {explanation}")
