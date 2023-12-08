import MetaTrader5 as Mt5


class Rates:
    def __init__(self, symbol, time_frame, start_pos, period):
        self.time = Mt5.copy_rates_from_pos(symbol, time_frame, start_pos, period)["time"]
        self.open = Mt5.copy_rates_from_pos(symbol, time_frame, start_pos, period)["open"]
        self.high = Mt5.copy_rates_from_pos(symbol, time_frame, start_pos, period)["high"]
        self.low = Mt5.copy_rates_from_pos(symbol, time_frame, start_pos, period)["low"]
        self.close = Mt5.copy_rates_from_pos(symbol, time_frame, start_pos, period)["close"]
        self.tick_volume = Mt5.copy_rates_from_pos(symbol, time_frame, start_pos, period)["tick_volume"]
        self.spread = Mt5.copy_rates_from_pos(symbol, time_frame, start_pos, period)["spread"]
        self.real_volume = Mt5.copy_rates_from_pos(symbol, time_frame, start_pos, period)["real_volume"]
