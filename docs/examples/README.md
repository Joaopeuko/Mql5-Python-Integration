# MQPy Trading Strategy Examples

This directory contains various example trading strategies implemented using the MQPy framework for MetaTrader 5 integration.

## Getting Started

If you're new to MQPy, start with the `getting_started.py` example which demonstrates basic concepts:

- Initializing the trading environment
- Fetching market data
- Making trading decisions
- Executing trades

## Available Examples

### Basic Strategies

1. **Getting Started** (`getting_started.py`)
   - A simple introduction to the MQPy framework
   - Demonstrates basic data retrieval and trading operations
   - Perfect for beginners

2. **Moving Average Crossover** (`basic_moving_average_strategy.py`)
   - Uses crossovers between short and long moving averages
   - Implements proper crossover detection logic
   - Includes logging and exception handling

### Technical Indicator Strategies

3. **RSI Strategy** (`rsi_strategy.py`)
   - Implements the Relative Strength Index (RSI) indicator
   - Trades based on overbought and oversold conditions
   - Shows how to calculate and use technical indicators

4. **Bollinger Bands Strategy** (`bollinger_bands_strategy.py`)
   - Uses Bollinger Bands for trading range breakouts
   - Demonstrates mean reversion trading principles
   - Includes volatility-based entry and exit logic

### Advanced Strategies

5. **Fibonacci Retracement Strategy** (`fibonacci_retracement_eurusd.py`)
   - Implements the FiMathe strategy for EURUSD
   - Uses Fibonacci retracement levels for entries and exits
   - Includes dynamic stop-loss adjustment based on price action

6. **Multi-Timeframe Analysis** (`rate_converter_example.py`)
   - Demonstrates how to convert between different timeframes using the RateConverter
   - Implements multi-timeframe analysis by calculating moving averages across timeframes
   - Visualizes price data and indicators across 1-minute, 5-minute, and 1-hour charts

## Fibonacci Retracement Strategy

The Fibonacci Retracement strategy (`fibonacci_retracement_eurusd.py`) demonstrates how to implement a trading system based on Fibonacci retracement levels. This strategy:

1. **Identifies swing points**: The algorithm detects significant market swing highs and lows within a specified window.
2. **Calculates Fibonacci levels**: Standard Fibonacci ratios (0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0) are applied between swing points to generate potential support and resistance levels.
3. **Generates trading signals**: The strategy produces buy signals when price bounces off key retracement levels during uptrends and sell signals during downtrends.
4. **Visualizes analysis**: Creates charts showing price action with identified swing points and Fibonacci levels to aid in trading decisions.

This approach is popular among technical traders who believe that markets frequently retrace a predictable portion of a move before continuing in the original direction.

## Market Depth Analysis

The Market Depth Analysis tool (`market_depth_analysis.py`) provides insights into order book data (DOM - Depth of Market) to understand supply and demand dynamics. Key features include:

1. **Real-time market depth monitoring**: Captures and analyzes order book snapshots at regular intervals.
2. **Buy/sell pressure analysis**: Calculates metrics such as buy/sell volume ratio, percentage distribution, and order concentration.
3. **Support/resistance identification**: Detects potential support and resistance levels based on unusual volume concentration at specific price points.
4. **Visual representation**: Creates horizontal bar charts showing the distribution of buy (bid) and sell (ask) orders, with highlighted support/resistance zones.

This analysis helps traders understand current market sentiment and identify price levels where significant buying or selling interest exists. The tool is particularly valuable for short-term traders and those interested in order flow analysis.

## Detailed Strategy Documentation

For an in-depth explanation of advanced strategies including theoretical background, implementation details, and potential customizations, see the [detailed strategy documentation](STRATEGY_DOCUMENTATION.md).

## Running the Examples

1. Make sure you have MQPy installed:
   ```bash
   pip install mqpy
   ```

2. Ensure MetaTrader 5 is installed and running on your system

3. Run any example with Python:
   ```bash
   python getting_started.py
   ```

## Strategy Development Best Practices

When developing your own strategies with MQPy, consider the following best practices:

1. **Error Handling**: Implement proper exception handling to catch network issues, data problems, or unexpected errors

2. **Logging**: Use Python's logging module to record important events and debug information

3. **Testing**: Test your strategy on historical data before deploying with real money

4. **Risk Management**: Always implement proper stop-loss and take-profit levels

5. **Architecture**: Separate your trading logic, indicators, and execution code for better maintainability

## Contributing

If you've developed an interesting strategy using MQPy, consider contributing it to this examples collection by submitting a pull request.

## Disclaimer

These example strategies are for educational purposes only and are not financial advice. Always perform your own analysis and risk assessment before trading with real money.
