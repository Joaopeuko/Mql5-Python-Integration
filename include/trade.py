from datetime import datetime, timedelta
import MetaTrader5 as Mt5


class Trade:
    def __init__(self,
                 expert_name,
                 version,
                 symbol,
                 magic_number,
                 lot: float,
                 stop_loss,  # It calls a functions that tries to close the deal, it is the stop you want.
                 emergency_stop_loss,  # It set stop on chart as a protection
                 # if something went wrong with the stop_loss.
                 take_profit,  # The same of stop_loss but for profit.
                 emergency_take_profit,  # The same of emergency_stop_loss but for gain
                 start_time='9:15',  # It is the hour and minutes that the expert advisor are able to start to run.
                 finishing_time='17:30',  # No new position can be opened after that time.
                 ending_time='17:50',  # If there is a position opened it will be closed.
                 fee=0.0,
                 ):

        self.expert_name = expert_name
        self.version = version
        self.symbol = symbol
        self.magic_number = magic_number
        self.lot = lot
        self.stop_loss = stop_loss
        self.emergency_stop_loss = emergency_stop_loss
        self.take_profit = take_profit
        self.emergency_take_profit = emergency_take_profit
        self.start_time_hour, self.start_time_minutes = start_time.split(':')
        self.finishing_time_hour, self.finishing_time_minutes = finishing_time.split(':')
        self.ending_time_hour, self.ending_time_minutes = ending_time.split(':')
        self.fee = fee

        self.loss_deals = 0
        self.profit_deals = 0
        self.total_deals = 0
        self.balance = 0.0

        self.ticket = 0

        print('\nInitializing the basics.')
        self.initialize()
        self.select_symbol()
        self.prepare_symbol()
        self.sl_tp_steps = Mt5.symbol_info(self.symbol).trade_tick_size / Mt5.symbol_info(self.symbol).point
        print('Initialization successfully completed.')

        print()
        self.summary()
        print('Running')
        print()

    def initialize(self):
        if not Mt5.initialize():
            print('Initialization failed, check internet connection. You must have Meta Trader 5 installed.')
            Mt5.shutdown()

        else:
            print(
                f'You are running the {self.expert_name} expert advisor,'
                f' version {self.version}, on symbol {self.symbol}.')

    def select_symbol(self):
        Mt5.symbol_select(self.symbol, True)

    def prepare_symbol(self):
        # Prepare the symbol to open positions
        symbol_info = Mt5.symbol_info(self.symbol)
        if symbol_info is None:
            print(f'It was not possible to find {self.symbol}')
            Mt5.shutdown()
            print('Turned off')
            quit()

        if not symbol_info.visible:
            print(f'The {self.symbol} is not visible, needed to be switched on.')
            if not Mt5.symbol_select(self.symbol, True):
                print(f'The expert advisor {self.expert_name} failed in select the symbol {self.symbol}, turning off.')
                Mt5.shutdown()
                print('Turned off')
                quit()

    def summary(self):
        print(
            f'Summary:\n'
            f'ExpertAdvisor name:              {self.expert_name}\n'
            f'ExpertAdvisor version:           {self.version}\n'
            f'Running on symbol:               {self.symbol}\n'
            f'MagicNumber:                     {self.magic_number}\n'
            f'Number of lot(s):                {self.lot}\n'
            f'StopLoss:                        {self.stop_loss}\n'
            f'TakeProfit:                      {self.take_profit}\n'
            f'Emergency StopLoss:              {self.emergency_stop_loss}\n'
            f'Emergency TakeProfit:            {self.emergency_take_profit}\n'
            f'Start trading time:              {self.start_time_hour}:{self.start_time_minutes}\n'
            f'Finishing trading time:          {self.finishing_time_hour}:{self.finishing_time_minutes}\n'
            f'Closing position after:          {self.ending_time_hour}:{self.ending_time_minutes}\n'
            f'Average fee per trading:         {self.fee}\n'
            f'StopLoss & TakeProfit Steps:     {self.sl_tp_steps}\n'
        )

    def statistics(self):
        print(f'Total of deals: {self.total_deals}, {self.profit_deals} gain, {self.loss_deals} loss.')
        print(f'Balance: {self.balance}, fee: {self.total_deals * self.fee}, final balance:'
              f' {self.balance - (self.total_deals * self.fee)}.')
        if self.total_deals != 0:
            print(f'Accuracy: {round((self.profit_deals / self.total_deals) * 100, 2)}%.\n')

    # It is to open a Buy position.
    def open_buy_position(self, comment=""):
        point = Mt5.symbol_info(self.symbol).point
        price = Mt5.symbol_info_tick(self.symbol).ask

        self.ticket = (Mt5.positions_get()[0].ticket if len(Mt5.positions_get()) == 1 else 0)

        request = {
            "action": Mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot,
            "type": Mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - self.emergency_stop_loss * point,
            "tp": price + self.emergency_take_profit * point,
            "deviation": 5,
            "magic": self.magic_number,
            "comment": str(comment),
            "type_time": Mt5.ORDER_TIME_GTC,
            "type_filling": Mt5.ORDER_FILLING_RETURN,
            "position": (Mt5.positions_get()[0].ticket if len(Mt5.positions_get()) == 1 else 0)
        }
        result = Mt5.order_send(request)
        self.request_result(price, result)

    # It is to open a Sell position.
    def open_sell_position(self, comment=""):
        point = Mt5.symbol_info(self.symbol).point
        price = Mt5.symbol_info_tick(self.symbol).bid

        self.ticket = (Mt5.positions_get()[0].ticket if len(Mt5.positions_get()) == 1 else 0)

        request = {
            "action": Mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": self.lot,
            "type": Mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": price + self.emergency_stop_loss * point,
            "tp": price - self.emergency_take_profit * point,
            "deviation": 5,
            "magic": self.magic_number,
            "comment": str(comment),
            "type_time": Mt5.ORDER_TIME_GTC,
            "type_filling": Mt5.ORDER_FILLING_RETURN,
            "position": (Mt5.positions_get()[0].ticket if len(Mt5.positions_get()) == 1 else 0)
        }
        result = Mt5.order_send(request)
        self.request_result(price, result)

    def request_result(self, price, result):
        # Send a trading request
        # Check the execution result
        print(f'Order sent: {self.symbol}, {self.lot} lot(s), at {price}.')
        if result.retcode != Mt5.TRADE_RETCODE_DONE:
            print(f'Something went wrong while retrieving ret_code, error: {result.retcode}')

        # Print the result
        if result.retcode == Mt5.TRADE_RETCODE_DONE:
            if len(Mt5.positions_get(symbol=self.symbol)) == 1:
                order_type = 'Buy' if Mt5.positions_get(symbol=self.symbol)[0].type == 0 else 'Sell'
                print(order_type, 'Position Opened:', result.price)
            else:
                print(f'Position Closed: {result.price}')

    def open_position(self, buy, sell, comment=""):
        if (len(Mt5.positions_get(symbol=self.symbol)) == 0) and self.trading_time():
            if buy and not sell:
                self.open_buy_position(comment)
                self.total_deals += 1
            if sell and not buy:
                self.open_sell_position(comment)
                self.total_deals += 1

        self.stop_and_gain(comment)

        if self.days_end():
            print('It is the end of trading the day.')
            print('Closing all positions.')
            self.close_position(comment)
            self.summary()

    def close_position(self, comment=""):
        # buy (0) and sell(1)
        if len(Mt5.positions_get(symbol=self.symbol)) == 1:

            if Mt5.positions_get(symbol=self.symbol)[0].type == 0:  # if Buy
                self.open_sell_position(comment)

            elif Mt5.positions_get(symbol=self.symbol)[0].type == 1:  # if Sell
                self.open_buy_position(comment)

    def stop_and_gain(self, comment=""):
        if len(Mt5.positions_get()) == 1:

            points = (Mt5.positions_get()[0].profit *
                      Mt5.symbol_info(self.symbol).trade_tick_size /
                      Mt5.symbol_info(self.symbol).trade_tick_value) / \
                     Mt5.positions_get()[0].volume

            if points / Mt5.symbol_info(self.symbol).point >= self.take_profit:
                self.profit_deals += 1
                self.close_position(comment)
                print(f'Take profit reached. ('
                      f'{Mt5.history_deals_get((datetime.today() - timedelta(days=1)), datetime.now())[-1].profit}'
                      f')\n')
                if Mt5.history_deals_get((datetime.today() - timedelta(days=1)), datetime.now())[-1].symbol == \
                        self.symbol:
                    self.balance += (Mt5.history_deals_get((datetime.today() - timedelta(days=1)),
                                                           datetime.now())[-1].profit)
                self.statistics()

            elif ((points / Mt5.symbol_info(self.symbol).point) * -1) >= self.stop_loss:
                self.loss_deals += 1
                self.close_position(comment)
                print(f'Stop loss reached. ('
                      f'{Mt5.history_deals_get((datetime.today() - timedelta(days=1)), datetime.now())[-1].profit}'
                      f')\n')
                if Mt5.history_deals_get((datetime.today() - timedelta(days=1)), datetime.now())[-1].symbol == \
                        self.symbol:
                    self.balance += (Mt5.history_deals_get((datetime.today() - timedelta(days=1)),
                                                           datetime.now())[-1].profit)
                self.statistics()

    def days_end(self):
        if datetime.now().hour >= int(self.ending_time_hour) and datetime.now().minute >= int(self.ending_time_minutes):
            return True

    def trading_time(self):
        if int(self.start_time_hour) < datetime.now().hour < int(self.finishing_time_hour):
            return True
        elif datetime.now().hour == int(self.start_time_hour):
            if datetime.now().minute >= int(self.start_time_minutes):
                return True
        elif datetime.now().hour == int(self.finishing_time_hour):
            if datetime.now().minute < int(self.finishing_time_minutes):
                return True
        return False
