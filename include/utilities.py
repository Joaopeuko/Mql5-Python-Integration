from datetime import datetime
import MetaTrader5 as Mt5


class Utilities:
    def __init__(self):

        # Variables for minutes_counter
        self.__minutes_counter = 0
        self.__counter_flag = True
        self.__allowed_to_trade = True
        self.__allow_to_count = False
        self.__recent_trade = False

    # This function will count the amount of minutes after some trade end.
    # You can use it as a condition to allow trades to happen.
    def minutes_counter_after_trade(self, symbol, count_until):
        if len(Mt5.positions_get(symbol=symbol)) == 1:
            self.__recent_trade = True

        if len(Mt5.positions_get(symbol=symbol)) != 1 and self.__recent_trade:
            if not self.__allow_to_count:
                self.__allow_to_count = True
                self.__allowed_to_trade = False
                self.__recent_trade = False

        if datetime.now().second == 0 and self.__counter_flag and self.__allow_to_count:
            print(f"Your Expert Advisor will be allowed to trade in {count_until-self.__minutes_counter} minutes.")
            self.__minutes_counter += 1
            self.__counter_flag = False

        if datetime.now().second == 59:
            self.__counter_flag = True

        if self.__minutes_counter == count_until:
            print(f"Your Expert Advisor is allowed to trade.\n")
            self.__minutes_counter = 0
            self.__counter_flag = True
            self.__allow_to_count = False
            self.__allowed_to_trade = True

        return self.__allowed_to_trade


