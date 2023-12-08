from mqpy.src.rates import Rates
from mqpy.src.tick import Tick
from mqpy.src.trade import Trade

# Initialize the trading strategy
trade = Trade(
    expert_name="Example",
    version=0.1,
    symbol="EURUSD",
    magic_number=567,
    lot=1.0,
    stop_loss=25,
    emergency_stop_loss=300,
    take_profit=25,
    emergency_take_profit=300,
    start_time="9:15",
    finishing_time="17:30",
    ending_time="17:50",
    fee=0.5,
)

# Main trading loop
time = 0
while True:
    # Fetch tick and rates data
    tick = Tick(trade.symbol)
    rates = Rates(trade.symbol, 1, 0, 1)

    # Check for new tick
    if tick.time_msc != time:
        buy_signal = tick.last > rates.open
        sell_signal = tick.last < rates.open

        # Execute trading positions based on signals
        trade.open_position(buy_signal, sell_signal, "Example Advisor")

    time = tick.time_msc

    # Check if it's the end of the trading day
    if trade.days_end():
        trade.close_position("End of the trading day reached.")
        break

print("Finishing the program.")
print("Program finished.")
