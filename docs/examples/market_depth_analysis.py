#!/usr/bin/env python3
"""Market Depth Analysis Example.

This example demonstrates how to access and analyze market depth (DOM) data
from MetaTrader 5 using the MQPy library. It captures order book snapshots,
analyzes buy/sell pressure, and identifies potential support/resistance levels.

Analysis Components:
------------------
1. Market Depth Data Collection:
   - Connects to MetaTrader 5 to retrieve real-time order book data
   - Captures snapshots of the market depth at regular time intervals (10 seconds)
   - Maintains a rolling history of the last 10 snapshots for trend analysis

2. Order Book Analytics:
   - Calculates key metrics including buy/sell volume ratio, order count, and volume distribution
   - Tracks volume concentration at specific price levels
   - Computes buy/sell percentages to gauge market sentiment
   - Identifies imbalances between buying and selling pressure

3. Support/Resistance Detection:
   - Identifies price levels with unusually high volume concentration
   - Uses a configurable threshold (default: 1.5x average volume) to detect significant levels
   - Classifies levels as either support or resistance based on their position relative to current price
   - Calculates a "strength" metric for each level based on its volume relative to the average

4. Visualization:
   - Creates horizontal bar charts showing the distribution of buy and sell orders
   - Highlights detected support and resistance levels
   - Includes annotations with key metrics (buy/sell ratio, volume percentages)
   - Saves images at regular intervals for monitoring market structure evolution

Applications:
-----------
- Order flow analysis for short-term trading decisions
- Identifying potential price reversal zones based on order concentration
- Gauging market sentiment through buy/sell imbalances
- Confirming technical analysis levels with actual order data
- Monitoring changes in market structure over time

This tool provides valuable insights into market microstructure that are not visible on
traditional price charts, offering traders an additional dimension for analysis.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import matplotlib.pyplot as plt

from mqpy.tick import MqlBookInfo, Tick
from mqpy.trade import Trade

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def analyze_market_depth(book_info: list[MqlBookInfo]) -> tuple[dict[str, float], dict[float, int]]:
    """Analyze market depth information to extract trading insights.

    Args:
        book_info: List of MqlBookInfo objects containing the market depth data

    Returns:
        Tuple containing market metrics and volume distribution by price
    """
    if not book_info:
        logger.warning("Empty market depth data received")
        return {}, {}

    # Initialize counters
    buy_volume = 0
    sell_volume = 0
    buy_orders = 0
    sell_orders = 0

    # Dictionary to track volume at each price level
    volume_by_price: dict[float, int] = {}

    # Process each entry in the order book
    for entry in book_info:
        # Track volume by price
        volume_by_price[entry.price] = volume_by_price.get(entry.price, 0) + entry.volume

        if entry.type == 1:  # Buy orders (bids)
            buy_volume += entry.volume
            buy_orders += 1
        elif entry.type == 2:  # Sell orders (asks)
            sell_volume += entry.volume
            sell_orders += 1

    # Calculate market metrics
    total_volume = buy_volume + sell_volume
    buy_percentage = (buy_volume / total_volume) * 100 if total_volume > 0 else 0
    sell_percentage = (sell_volume / total_volume) * 100 if total_volume > 0 else 0

    # Calculate buy/sell ratio
    buy_sell_ratio = buy_volume / sell_volume if sell_volume > 0 else float("inf")

    # Package results
    metrics = {
        "buy_volume": buy_volume,
        "sell_volume": sell_volume,
        "buy_orders": buy_orders,
        "sell_orders": sell_orders,
        "buy_percentage": buy_percentage,
        "sell_percentage": sell_percentage,
        "buy_sell_ratio": buy_sell_ratio,
        "total_orders": buy_orders + sell_orders,
        "total_volume": total_volume,
    }

    return metrics, volume_by_price


def identify_support_resistance(
    volume_by_price: dict[float, int], threshold_factor: float = 1.5
) -> list[dict[str, Any]]:
    """Identify potential support and resistance levels based on volume concentration.

    Args:
        volume_by_price: Dictionary mapping price levels to their volume
        threshold_factor: Multiplier for the average volume to identify significant levels

    Returns:
        List of dictionaries containing identified support/resistance levels
    """
    if not volume_by_price:
        return []

    # Calculate average volume
    volumes = list(volume_by_price.values())
    avg_volume = sum(volumes) / len(volumes)
    threshold = avg_volume * threshold_factor

    # Find price levels with volume above threshold
    significant_levels = []

    # Sort price levels for easier analysis
    sorted_prices = sorted(volume_by_price.keys())

    for price in sorted_prices:
        volume = volume_by_price[price]
        if volume > threshold:
            # Determine if this is likely support or resistance
            # This is a simplistic approach - in reality, you'd need more context
            # We'll use a simple heuristic based on position in the order book
            median_price = sorted_prices[len(sorted_prices) // 2]
            level_type = "support" if price < median_price else "resistance"

            significant_levels.append(
                {
                    "price": price,
                    "volume": volume,
                    "type": level_type,
                    "strength": volume / avg_volume,  # Relative strength factor
                }
            )

    return significant_levels


def plot_market_depth(book_info: list[MqlBookInfo], metrics: dict[str, float], levels: list[dict[str, Any]]) -> None:
    """Visualize market depth data and identified support/resistance levels.

    Args:
        book_info: List of MqlBookInfo objects containing the market depth data
        metrics: Dictionary of market metrics from analyze_market_depth
        levels: List of identified support/resistance levels
    """
    try:
        # Extract data for plotting
        buy_prices = []
        buy_volumes = []
        sell_prices = []
        sell_volumes = []

        for entry in book_info:
            if entry.type == 1:  # Buy orders
                buy_prices.append(entry.price)
                buy_volumes.append(entry.volume)
            elif entry.type == 2:  # Sell orders
                sell_prices.append(entry.price)
                sell_volumes.append(entry.volume)

        # Create the plot
        plt.figure(figsize=(12, 8))

        # Plot buy orders (bids) in green
        plt.barh(buy_prices, buy_volumes, color="green", alpha=0.6, label="Bids (Buy Orders)")

        # Plot sell orders (asks) in red
        plt.barh(sell_prices, sell_volumes, color="red", alpha=0.6, label="Asks (Sell Orders)")

        # Highlight support/resistance levels
        for level in levels:
            plt.axhline(
                y=level["price"],
                color="purple",
                linestyle="--",
                alpha=0.7,
                label=f"{level['type'].capitalize()} ({level['price']})",
            )

        # Add labels and title
        plt.title(f"Market Depth Analysis\nBuy/Sell Ratio: {metrics['buy_sell_ratio']:.2f}", fontsize=14)
        plt.xlabel("Volume", fontsize=12)
        plt.ylabel("Price", fontsize=12)
        plt.grid(visible=True, alpha=0.3)

        # Add buy/sell percentage annotation
        annotation_text = (
            f"Buy Volume: {metrics['buy_volume']} ({metrics['buy_percentage']:.1f}%)\n"
            f"Sell Volume: {metrics['sell_volume']} ({metrics['sell_percentage']:.1f}%)\n"
            f"Total Orders: {metrics['total_orders']}"
        )
        plt.annotate(
            annotation_text,
            xy=(0.02, 0.02),
            xycoords="axes fraction",
            bbox={"boxstyle": "round,pad=0.5", "fc": "white", "alpha": 0.8},
        )

        # Clean up the legend (limit to unique entries)
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc="best")

        # Save the plot
        plt.tight_layout()
        plt.savefig("market_depth_analysis.png")
        logger.info("Market depth visualization saved as 'market_depth_analysis.png'")
        plt.close()
    except Exception:
        logger.exception("Error creating market depth visualization")


def main() -> None:
    """Main execution function for the market depth analysis."""
    # Initialize the trade object
    trade = Trade(
        expert_name="Market Depth Analyzer",
        version="1.0",
        symbol="EURUSD",
        magic_number=573,
        lot=0.1,
        stop_loss=30,
        emergency_stop_loss=90,
        take_profit=60,
        emergency_take_profit=180,
        start_time="9:15",
        finishing_time="17:30",
        ending_time="17:50",
        fee=0.5,
    )

    logger.info(f"Starting Market Depth Analysis for {trade.symbol}")

    # Previous tick time to track new ticks
    prev_tick_time = 0

    # Track depth changes
    depth_snapshots: list[list[MqlBookInfo]] = []
    snapshot_timestamps: list[int] = []
    last_snapshot_time = 0

    try:
        # Main loop
        while True:
            # Prepare the symbol for trading
            trade.prepare_symbol()

            # Fetch current tick data
            current_tick = Tick(trade.symbol)

            # Only process if we have a new tick
            if current_tick.time_msc != prev_tick_time:
                try:
                    # Get market depth data
                    book_info = current_tick.get_book()

                    # Check if we have valid market depth data
                    if book_info and len(book_info) > 0:
                        # Take snapshots at regular intervals (every 10 seconds)
                        current_time = int(time.time())
                        if current_time - last_snapshot_time >= 10:
                            # Store the snapshot
                            depth_snapshots.append(book_info)
                            snapshot_timestamps.append(current_time)
                            last_snapshot_time = current_time

                            # Keep only the last 10 snapshots
                            if len(depth_snapshots) > 10:
                                depth_snapshots.pop(0)
                                snapshot_timestamps.pop(0)

                            # Analyze the current market depth
                            metrics, volume_by_price = analyze_market_depth(book_info)

                            # Log key metrics
                            logger.info(
                                f"Market depth snapshot at {time.strftime('%H:%M:%S', time.localtime(current_time))}"
                            )
                            logger.info(f"Buy/Sell Ratio: {metrics['buy_sell_ratio']:.2f}")
                            logger.info(f"Buy Volume: {metrics['buy_volume']} ({metrics['buy_percentage']:.1f}%)")
                            logger.info(f"Sell Volume: {metrics['sell_volume']} ({metrics['sell_percentage']:.1f}%)")

                            # Identify potential support and resistance levels
                            levels = identify_support_resistance(volume_by_price)

                            if levels:
                                logger.info("Potential support/resistance levels:")
                                for level in levels:
                                    logger.info(
                                        f"{level['type'].capitalize()} at {level['price']} "
                                        f"(strength: {level['strength']:.1f}x average)"
                                    )

                            # Create a visualization every 30 seconds
                            if len(depth_snapshots) % 3 == 0:
                                plot_market_depth(book_info, metrics, levels)

                except Exception:
                    logger.exception("Error processing market depth data")

                # Update previous tick time
                prev_tick_time = current_tick.time_msc

            # Check if it's the end of the trading day
            if trade.days_end():
                logger.info("End of trading day reached.")
                break

            # Add a short delay to avoid excessive CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
    except Exception:
        logger.exception("Error in market depth analysis")
    finally:
        logger.info("Finishing market depth analysis")

        # Create a final visualization if we have data
        if depth_snapshots:
            try:
                # Analyze the most recent snapshot
                metrics, volume_by_price = analyze_market_depth(depth_snapshots[-1])
                levels = identify_support_resistance(volume_by_price)
                plot_market_depth(depth_snapshots[-1], metrics, levels)
                logger.info("Final market depth visualization saved")
            except Exception:
                logger.exception("Error creating final visualization")


if __name__ == "__main__":
    main()
