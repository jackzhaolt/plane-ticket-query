"""Logic for detecting good flight deals."""

from typing import List, Dict, Optional
from searchers.base import Flight
from distance_calculator import get_flight_distance
from award_charts import evaluate_redemption, DealQuality


class DealDetector:
    """Detects good flight deals based on configurable thresholds."""

    def __init__(self, config: Dict):
        """
        Initialize deal detector with configuration.

        Args:
            config: Deal configuration from settings.yaml
        """
        self.max_cash_price = config.get('max_cash_price', 1000)
        self.max_points = config.get('max_points', 100000)
        self.min_cpp = config.get('min_cpp', 1.0)  # cents per point
        self.min_miles_per_point = config.get('min_miles_per_point', 0.05)
        self.transfer_partners = config.get('transfer_partners', {})

        # Award chart evaluation
        self.use_award_chart = config.get('use_award_chart', True)
        self.award_chart_name = config.get('award_chart', 'standard')
        self.award_chart_min_quality = config.get('award_chart_min_quality', 'good')

    def is_good_deal(self, flight: Flight) -> bool:
        """
        Determine if a flight is a good deal based on multiple criteria.

        Evaluates:
        1. Cash price (absolute threshold)
        2. Award chart evaluation (distance-based bands) ← PRIMARY!
        3. Points value (cents per point)
        4. Distance efficiency (miles per point)

        Args:
            flight: Flight object to evaluate

        Returns:
            True if the flight meets deal criteria
        """
        # Check cash price threshold
        if flight.price_usd <= self.max_cash_price:
            return True

        # Check points-based criteria
        if not flight.points:
            return False

        # PRIMARY: Award chart evaluation
        if self.use_award_chart:
            distance = get_flight_distance(flight.departure_airport, flight.arrival_airport)
            if distance > 0:
                quality, _, _ = evaluate_redemption(
                    distance,
                    flight.points,
                    flight.cabin_class,
                    self.award_chart_name
                )

                # Define quality thresholds
                quality_order = {
                    'exceptional': 4,
                    'great': 3,
                    'good': 2,
                    'fair': 1,
                    'poor': 0
                }

                min_quality_score = quality_order.get(self.award_chart_min_quality, 2)
                flight_quality_score = quality_order.get(quality.value, 0)

                # If award chart says it's good enough, it's a deal
                if flight_quality_score >= min_quality_score:
                    return True

        # FALLBACK: Traditional metrics if award chart doesn't apply
        if flight.points <= self.max_points:
            # Calculate cents per point value
            cpp = (flight.price_usd * 100) / flight.points

            # Calculate miles per point (distance efficiency)
            distance = get_flight_distance(flight.departure_airport, flight.arrival_airport)
            miles_per_point = distance / flight.points if flight.points > 0 else 0

            # Good deal if EITHER meets threshold
            if cpp >= self.min_cpp or miles_per_point >= self.min_miles_per_point:
                return True

        return False

    def filter_deals(self, flights: List[Flight]) -> List[Flight]:
        """
        Filter a list of flights to only good deals.

        Args:
            flights: List of Flight objects

        Returns:
            List of flights that are good deals
        """
        return [flight for flight in flights if self.is_good_deal(flight)]

    def rank_deals(self, flights: List[Flight]) -> List[Flight]:
        """
        Rank flights by deal quality (best first).

        Considers:
        - Price (lower is better)
        - Cents per point value
        - Miles per point (distance efficiency) ← NEW!
        - Direct flights bonus

        Args:
            flights: List of Flight objects

        Returns:
            Sorted list of flights (best deals first)
        """
        def deal_score(flight: Flight) -> float:
            """Calculate a deal score (higher is better)."""
            score = 0

            # 1. Price score (lower price is better)
            price_score = max(0, 2000 - flight.price_usd)
            score += price_score

            # 2. Points value scores
            if flight.points:
                # Cents per point
                cpp = (flight.price_usd * 100) / flight.points
                cpp_score = cpp * 100
                score += cpp_score

                # Miles per point (distance efficiency) - NEW!
                distance = get_flight_distance(flight.departure_airport, flight.arrival_airport)
                miles_per_point = distance / flight.points if flight.points > 0 else 0
                # Weight this heavily - it's the best metric for award flights!
                mpp_score = miles_per_point * 10000
                score += mpp_score

            # 3. Direct flight bonus
            if flight.stops == 0:
                score += 500

            return score

        return sorted(flights, key=deal_score, reverse=True)

    def format_deal_summary(self, flight: Flight) -> str:
        """
        Format a flight deal as a human-readable string.

        Args:
            flight: Flight object

        Returns:
            Formatted string with deal details
        """
        # Calculate distance
        distance = get_flight_distance(flight.departure_airport, flight.arrival_airport)

        summary = f"🎉 GREAT DEAL FOUND!\n\n"
        summary += f"Route: {flight.departure_airport} → {flight.arrival_airport}"

        if distance > 0:
            summary += f" ({distance:,.0f} miles)\n"
        else:
            summary += "\n"

        summary += f"Date: {flight.departure_date}"

        if flight.return_date:
            summary += f" - {flight.return_date}"

        summary += f"\nAirline: {flight.airline}\n"
        summary += f"Class: {flight.cabin_class}\n"
        summary += f"Stops: {'Direct' if flight.stops == 0 else f'{flight.stops}'}\n"
        summary += f"\nPrice: ${flight.price_usd:.2f} USD\n"

        if flight.points:
            cpp = (flight.price_usd * 100) / flight.points
            summary += f"Points: {flight.points:,} ({cpp:.2f}¢ per point)\n"

            # Award chart evaluation (NEW!)
            if distance > 0 and self.use_award_chart:
                quality, explanation, expected = evaluate_redemption(
                    distance,
                    flight.points,
                    flight.cabin_class,
                    self.award_chart_name
                )

                # Show award chart analysis
                if expected:
                    summary += f"\nAward Chart Analysis ({self.award_chart_name}):\n"
                    summary += f"  Expected Range: {expected[0]:,}-{expected[1]:,} points\n"
                    summary += f"  This Flight: {flight.points:,} points\n"
                    summary += f"  Rating: "

                    if quality == DealQuality.EXCEPTIONAL:
                        summary += "⭐⭐⭐ EXCEPTIONAL - "
                    elif quality == DealQuality.GREAT:
                        summary += "⭐⭐ GREAT - "
                    elif quality == DealQuality.GOOD:
                        summary += "⭐ GOOD - "
                    elif quality == DealQuality.FAIR:
                        summary += "😐 FAIR - "
                    else:
                        summary += "❌ POOR - "

                    summary += f"{explanation}\n"

            # Also show miles per point for context
            if distance > 0:
                miles_per_point = distance / flight.points
                summary += f"  Distance Efficiency: {miles_per_point:.3f} miles/point\n"

        if flight.booking_url:
            summary += f"\nBook now: {flight.booking_url}\n"

        return summary
