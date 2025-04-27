# MQPy Examples

!!! danger "Trading Risk Warning"
    **IMPORTANT: All examples should be tested using demo accounts only!**

    - Trading involves substantial risk of loss
    - These examples are for educational purposes only
    - Always test with fake money before using real funds
    - Past performance is not indicative of future results
    - The developers are not responsible for any financial losses

MQPy provides a variety of example trading strategies to help you understand how to implement your own algorithmic trading solutions using MetaTrader 5.

## Getting Started

If you're new to MQPy, we recommend starting with the [Getting Started Example](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/getting_started.py) which introduces you to the basics of:

- Initializing the trading environment
- Fetching market data
- Making trading decisions
- Executing trades

## Basic Strategies

### Moving Average Crossover

The [Moving Average Crossover](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/basic_moving_average_strategy.py) strategy is a classic trading approach that:

| Feature | Description |
|---------|-------------|
| Signal Generation | Uses crossovers between short and long moving averages |
| Implementation | Includes proper crossover detection logic |
| Error Handling | Comprehensive logging and exception handling |

[Read detailed explanation of the Moving Average strategy →](strategies/moving_average.md)

```python
def calculate_sma(prices, period):
    """Calculate Simple Moving Average."""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period
```

## Technical Indicator Strategies

### RSI Strategy

The [RSI Strategy](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/rsi_strategy.py) example demonstrates:

| Feature | Description |
|---------|-------------|
| Indicator | Implementation of the Relative Strength Index (RSI) |
| Trading Approach | Entry/exit based on overbought and oversold conditions |
| Technical Analysis | Practical example of calculating and using indicators |

[Read detailed explanation of the RSI strategy →](strategies/rsi_strategy.md)

### Bollinger Bands Strategy

The [Bollinger Bands Strategy](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/bollinger_bands_strategy.py) shows:

| Feature | Description |
|---------|-------------|
| Trading Approach | Using Bollinger Bands for trading range breakouts |
| Strategy Type | Mean reversion trading principles |
| Signal Generation | Volatility-based entry and exit logic |

[Read detailed explanation of the Bollinger Bands strategy →](strategies/bollinger_bands.md)

## Advanced Strategies

### Fibonacci Retracement Strategy

The [Fibonacci Retracement Strategy](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/fibonacci_retracement_eurusd.py) for EURUSD:

| Feature | Description |
|---------|-------------|
| Strategy Type | Implements the FiMathe strategy |
| Pattern Recognition | Uses Fibonacci retracement levels for entries and exits |
| Risk Management | Includes dynamic stop-loss adjustment based on price action |

[Read detailed explanation of the Fibonacci Retracement strategy →](strategies/fibonacci_retracement.md)

### Market Depth Analysis

The [Market Depth Analysis](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/market_depth_analysis.py) provides insights into order book data:

| Feature | Description |
|---------|-------------|
| Order Book Analysis | Examines buy/sell order distribution and concentration |
| Support/Resistance | Identifies potential support and resistance levels from actual orders |
| Visualization | Creates horizontal bar charts showing bid/ask distribution with key levels |

[Read detailed explanation of the Market Depth Analysis →](strategies/market_depth_analysis.md)

### Multi-Timeframe Analysis

The [Rate Converter Example](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/rate_converter_example.py) demonstrates:

| Feature | Description |
|---------|-------------|
| Timeframe Conversion | How to convert between different timeframes using the RateConverter |
| Multi-timeframe Analysis | Calculating moving averages across different timeframes |
| Visualization | Creating charts for price data across 1-minute, 5-minute, and 1-hour timeframes |

### Indicator Connector Strategy

The [Indicator Connector Strategy](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/indicator_connector_strategy.py) shows:

| Feature | Description |
|---------|-------------|
| Connectivity | How to connect to MetaTrader 5's custom indicators |
| Signal Combination | Combining multiple indicator signals (Stochastic and Moving Average) |
| Advanced Techniques | Advanced signal generation and filtering approaches |

## Running the Examples

To run any of these examples:

1. Ensure you have MQPy installed:
   ```bash
   pip install mqpy
   ```

2. Make sure MetaTrader 5 is installed and running on your system

3. Run any example with Python:
   ```bash
   python getting_started.py
   ```

## Contributing Your Own Examples

If you've developed an interesting strategy using MQPy, consider contributing it to this examples collection by submitting a pull request!

## Disclaimer

These example strategies are for educational purposes only and are not financial advice. Always perform your own analysis and risk assessment before trading with real money.

## All Example Files

You can access these examples in several ways:

1. **Clone the entire repository**:
   ```bash
   git clone https://github.com/Joaopeuko/Mql5-Python-Integration.git
   cd Mql5-Python-Integration/docs/examples
   ```

2. **Download individual files** by clicking on the links in the table below.

3. **Copy the code** from the strategy explanations page for the strategies with detailed documentation.

Here are direct links to all the example files in the MQPy repository:

| Strategy | Description | Source Code |
|----------|-------------|-------------|
| Getting Started | Basic introduction to MQPy | [getting_started.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/getting_started.py) |
| Moving Average Crossover | Simple trend-following strategy | [basic_moving_average_strategy.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/basic_moving_average_strategy.py) |
| RSI Strategy | Momentum-based overbought/oversold strategy | [rsi_strategy.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/rsi_strategy.py) |
| Bollinger Bands | Mean reversion volatility strategy | [bollinger_bands_strategy.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/bollinger_bands_strategy.py) |
| Fibonacci Retracement | Advanced Fibonacci pattern strategy | [fibonacci_retracement_eurusd.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/fibonacci_retracement_eurusd.py) |
| Market Depth Analysis | Order book and volume analysis | [market_depth_analysis.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/market_depth_analysis.py) |
| Rate Converter | Multi-timeframe analysis example | [rate_converter_example.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/rate_converter_example.py) |
| Indicator Connector | Custom indicator integration | [indicator_connector_strategy.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/indicator_connector_strategy.py) |
| Sockets Connection | Advanced MetaTrader connectivity | [example_sockets_connection.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/main/docs/examples/example_sockets_connection.py) |
