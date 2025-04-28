"""Module for trading operations with MetaTrader 5.

Provides a Trade class for managing trading operations.

Trade Modes:
    - 0: Disabled - Trading is completely disabled for the symbol
    - 1: Long only - Only buy positions allowed
    - 2: Short only - Only sell positions allowed
    - 3: Long and Short - Both buy and sell positions allowed (regular trading)
    - 4: Close only - Only position closing is allowed, no new positions can be opened

The Trade class automatically respects these limitations when attempting to open or close positions.
"""

import sys
from datetime import datetime, timedelta, timezone

import MetaTrader5 as Mt5

from mqpy.logger import get_logger

# Configure logging
logger = get_logger(__name__)


class Trade:
    """Represents a trading strategy for a financial instrument.

    Args:
        expert_name (str): The name of the expert advisor.
        version (str): The version of the expert advisor.
        symbol (str): The financial instrument symbol.
        magic_number (int): The magic number for identifying trades.
        lot (float): The number of lots to trade.
        stop_loss (float): The stop loss level.
        emergency_stop_loss (float): Emergency stop loss as a protection.
        take_profit (float): The take profit level.
        emergency_take_profit (float): Emergency take profit for gain.
        start_time (str): The time when the expert advisor can start trading.
        finishing_time (str): The time until new positions can be opened.
        ending_time (str): The time when any remaining position will be closed.
        fee (float): The average fee per trading.
    """

    def __init__(
        self,
        expert_name: str,
        version: str,
        symbol: str,
        magic_number: int,
        lot: float,
        stop_loss: float,
        emergency_stop_loss: float,
        take_profit: float,
        emergency_take_profit: float,
        start_time: str = "9:15",
        finishing_time: str = "17:30",
        ending_time: str = "17:50",
        fee: float = 0.0,
    ) -> None:
        """Initialize the Trade object.

        Returns:
            None
        """
        self.expert_name: str = expert_name
        self.version: str = version
        self.symbol: str = symbol
        self.magic_number: int = magic_number
        self.lot: float = lot
        self.stop_loss: float = stop_loss
        self.emergency_stop_loss: float = emergency_stop_loss
        self.take_profit: float = take_profit
        self.emergency_take_profit: float = emergency_take_profit
        self.start_time_hour, self.start_time_minutes = start_time.split(":")
        self.finishing_time_hour, self.finishing_time_minutes = finishing_time.split(":")
        self.ending_time_hour, self.ending_time_minutes = ending_time.split(":")
        self.fee: float = fee

        self.loss_deals: int = 0
        self.profit_deals: int = 0
        self.total_deals: int = 0
        self.balance: float = 0.0

        self.ticket: int = 0

        logger.info("Initializing the basics.")
        self.initialize()
        self.select_symbol()
        self.prepare_symbol()
        self.sl_tp_steps: float = Mt5.symbol_info(self.symbol).trade_tick_size / Mt5.symbol_info(self.symbol).point
        logger.info("Initialization successfully completed.")
        logger.info("")
        self.summary()
        logger.info("Running")
        logger.info("")

    def initialize(self) -> None:
        """Initialize the MetaTrader 5 instance.

        Returns:
            None
        """
        if not Mt5.initialize():
            logger.error("Initialization failed, check internet connection. You must have Meta Trader 5 installed.")
            Mt5.shutdown()
        else:
            logger.info(
                f"You are running the {self.expert_name} expert advisor,"
                f" version {self.version}, on symbol {self.symbol}."
            )

    def select_symbol(self) -> None:
        """Select the trading symbol.

        Returns:
            None
        """
        # Using positional arguments as the MetaTrader5 library doesn't support keywords
        Mt5.symbol_select(self.symbol, True)  # noqa: FBT003

    def prepare_symbol(self) -> None:
        """Prepare the trading symbol for opening positions.

        Returns:
            None
        """
        symbol_info = Mt5.symbol_info(self.symbol)
        if symbol_info is None:
            logger.error(f"It was not possible to find {self.symbol}")
            Mt5.shutdown()
            logger.error("Turned off")
            sys.exit(1)

        if not symbol_info.visible:
            logger.warning(f"The {self.symbol} is not visible, needed to be switched on.")
            # Using positional arguments as the MetaTrader5 library doesn't support keywords
            if not Mt5.symbol_select(self.symbol, True):  # noqa: FBT003
                logger.error(
                    f"The expert advisor {self.expert_name} failed in select the symbol {self.symbol}, turning off."
                )
                Mt5.shutdown()
                logger.error("Turned off")
                sys.exit(1)

        # Check the trade mode
        if symbol_info.trade_mode == 0:
            logger.warning(
                f"Trading is disabled for {self.symbol} (trade_mode = 0). No positions can be opened or closed."
            )
        elif symbol_info.trade_mode == 4:
            logger.warning(
                f"{self.symbol} is in 'Close only' mode (trade_mode = 4). Only existing positions can be closed."
            )

    def get_trade_mode_description(self) -> str:
        """Get a description of the symbol's trade mode.

        Returns:
            str: A description of the trade mode.
        """
        trade_mode = Mt5.symbol_info(self.symbol).trade_mode

        if trade_mode == 0:
            return "Disabled (trading disabled for the symbol)"
        if trade_mode == 1:
            return "Long only (only buy positions allowed)"
        if trade_mode == 2:
            return "Short only (only sell positions allowed)"
        if trade_mode == 3:
            return "Long and Short (both buy and sell positions allowed)"
        if trade_mode == 4:
            return "Close only (only position closing is allowed)"
        return f"Unknown trade mode: {trade_mode}"

    def summary(self) -> None:
        """Print a summary of the expert advisor parameters.

        Returns:
            None
        """
        trade_mode = Mt5.symbol_info(self.symbol).trade_mode
        trade_mode_desc = self.get_trade_mode_description()

        logger.info(
            f"Summary:\n"
            f"ExpertAdvisor name:              {self.expert_name}\n"
            f"ExpertAdvisor version:           {self.version}\n"
            f"Running on symbol:               {self.symbol}\n"
            f"Symbol trade mode:               {trade_mode} - {trade_mode_desc}\n"
            f"MagicNumber:                     {self.magic_number}\n"
            f"Number of lot(s):                {self.lot}\n"
            f"StopLoss:                        {self.stop_loss}\n"
            f"TakeProfit:                      {self.take_profit}\n"
            f"Emergency StopLoss:              {self.emergency_stop_loss}\n"
            f"Emergency TakeProfit:            {self.emergency_take_profit}\n"
            f"Start trading time:              {self.start_time_hour}:{self.start_time_minutes}\n"
            f"Finishing trading time:          {self.finishing_time_hour}:{self.finishing_time_minutes}\n"
            f"Closing position after:          {self.ending_time_hour}:{self.ending_time_minutes}\n"
            f"Average fee per trading:         {self.fee}\n"
            f"StopLoss & TakeProfit Steps:     {self.sl_tp_steps}\n"
        )

    def statistics(self) -> None:
        """Print statistics of the expert advisor.

        Returns:
            None
        """
        logger.info(f"Total of deals: {self.total_deals}, {self.profit_deals} gain, {self.loss_deals} loss.")
        logger.info(
            f"Balance: {self.balance}, fee: {self.total_deals * self.fee}, final balance:"
            f" {self.balance - (self.total_deals * self.fee)}."
        )
        if self.total_deals != 0:
            logger.info(f"Accuracy: {round((self.profit_deals / self.total_deals) * 100, 2)}%.\n")

    def open_buy_position(self, comment: str = "") -> None:
        """Open a Buy position.

        Args:
            comment (str): A comment for the trade.

        Returns:
            None
        """
        point = Mt5.symbol_info(self.symbol).point
        price = Mt5.symbol_info_tick(self.symbol).ask

        self.ticket = Mt5.positions_get()[0].ticket if len(Mt5.positions_get()) == 1 else 0

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
            "position": (Mt5.positions_get()[0].ticket if len(Mt5.positions_get()) == 1 else 0),
        }
        result = Mt5.order_send(request)
        self.request_result(price, result)

    def open_sell_position(self, comment: str = "") -> None:
        """Open a Sell position.

        Args:
            comment (str): A comment for the trade.

        Returns:
            None
        """
        point = Mt5.symbol_info(self.symbol).point
        price = Mt5.symbol_info_tick(self.symbol).bid

        self.ticket = Mt5.positions_get()[0].ticket if len(Mt5.positions_get()) == 1 else 0

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
            "position": (Mt5.positions_get()[0].ticket if len(Mt5.positions_get()) == 1 else 0),
        }
        result = Mt5.order_send(request)
        self.request_result(price, result)

    def request_result(self, price: float, result: int) -> None:
        """Process the result of a trading request.

        Args:
            price (float): The price of the trade.
            result (Mt5.TradeResult): The result of the trading request.

        Returns:
            None
        """
        logger.info(f"Order sent: {self.symbol}, {self.lot} lot(s), at {price}.")
        if result.retcode != Mt5.TRADE_RETCODE_DONE:
            logger.error(f"Something went wrong while retrieving ret_code, error: {result.retcode}")

        if result.retcode == Mt5.TRADE_RETCODE_DONE:
            if len(Mt5.positions_get(symbol=self.symbol)) == 1:
                order_type = "Buy" if Mt5.positions_get(symbol=self.symbol)[0].type == 0 else "Sell"
                logger.info(f"{order_type} Position Opened: {result.price}")
            else:
                logger.info(f"Position Closed: {result.price}")

    def _handle_trade_mode_restrictions(self, symbol_info: Mt5.SymbolInfo) -> bool:
        """Handle trade mode restrictions for different symbol types.

        Args:
            symbol_info (Mt5.SymbolInfo): The symbol information.

        Returns:
            bool: True if a position was opened or a restriction was handled, False otherwise.
        """
        # Check if the symbol is in "Disabled" mode (trade_mode = 0)
        if symbol_info.trade_mode == 0:
            logger.warning(f"Cannot open new positions for {self.symbol} - trading is disabled.")
            return True

        # Check if the symbol is in "Close only" mode (trade_mode = 4)
        if symbol_info.trade_mode == 4 and len(Mt5.positions_get(symbol=self.symbol)) == 0:
            logger.warning(f"Cannot open new positions for {self.symbol} - symbol is in 'Close only' mode.")
            return True

        # No restrictions that prevent all trading
        return False

    def _handle_position_by_trade_mode(
        self, symbol_info: Mt5.SymbolInfo, *, should_buy: bool, should_sell: bool, comment: str
    ) -> None:
        """Open a position based on trade mode and buy/sell conditions.

        Args:
            symbol_info (Mt5.SymbolInfo): The symbol information.
            should_buy (bool): Whether a buy position should be opened.
            should_sell (bool): Whether a sell position should be opened.
            comment (str): A comment for the trade.
        """
        # For "Long only" mode (trade_mode = 1), only allow Buy positions
        if symbol_info.trade_mode == 1:
            if should_buy:
                self.open_buy_position(comment)
                self.total_deals += 1
            elif should_sell:
                logger.warning(f"Cannot open Sell position for {self.symbol} - only Buy positions are allowed.")

        # For "Short only" mode (trade_mode = 2), only allow Sell positions
        elif symbol_info.trade_mode == 2:
            if should_sell:
                self.open_sell_position(comment)
                self.total_deals += 1
            elif should_buy:
                logger.warning(f"Cannot open Buy position for {self.symbol} - only Sell positions are allowed.")

        # For regular trading (trade_mode = 3) or other modes, allow both Buy and Sell
        else:
            if should_buy and not should_sell:
                self.open_buy_position(comment)
                self.total_deals += 1
            if should_sell and not should_buy:
                self.open_sell_position(comment)
                self.total_deals += 1

    def open_position(self, *, should_buy: bool, should_sell: bool, comment: str = "") -> None:
        """Open a position based on buy and sell conditions.

        Args:
            should_buy (bool): True if a Buy position should be opened, False otherwise.
            should_sell (bool): True if a Sell position should be opened, False otherwise.
            comment (str): A comment for the trade.

        Returns:
            None
        """
        symbol_info = Mt5.symbol_info(self.symbol)

        # Open a position if no existing positions and within trading time
        if (len(Mt5.positions_get(symbol=self.symbol)) == 0) and self.trading_time():
            if should_buy and not should_sell:
                self.open_buy_position(comment)
                self.total_deals += 1
            if should_sell and not should_buy:
                self.open_sell_position(comment)
                self.total_deals += 1

        # Check for stop loss and take profit conditions
        self.stop_and_gain(comment)

        # Check if it's the end of the trading day
        if self.days_end():
            logger.info("It is the end of trading the day.")
            logger.info("Closing all positions.")
            self.close_position(comment)
            self.summary()

    def close_position(self, comment: str = "") -> None:
        """Close an open position.

        Args:
            comment (str): A comment for the trade.

        Returns:
            None
        """
        symbol_info = Mt5.symbol_info(self.symbol)

        # If trading is completely disabled for the symbol, log a warning and return
        if symbol_info.trade_mode == 0:
            logger.warning(f"Cannot close position for {self.symbol} - trading is disabled for this symbol.")
            return

        if len(Mt5.positions_get(symbol=self.symbol)) == 1:
            if Mt5.positions_get(symbol=self.symbol)[0].type == 0:  # Buy position
                self.open_sell_position(comment)
            elif Mt5.positions_get(symbol=self.symbol)[0].type == 1:  # Sell position
                self.open_buy_position(comment)

    def stop_and_gain(self, comment: str = "") -> None:
        """Check for stop loss and take profit conditions and close positions accordingly.

        Args:
            comment (str): A comment for the trade.

        Returns:
            None
        """
        if len(Mt5.positions_get()) == 1:
            points = (
                Mt5.positions_get()[0].profit
                * Mt5.symbol_info(self.symbol).trade_tick_size
                / Mt5.symbol_info(self.symbol).trade_tick_value
            ) / Mt5.positions_get()[0].volume

            if points / Mt5.symbol_info(self.symbol).point >= self.take_profit:
                self.profit_deals += 1
                self.close_position(comment)
                start_time = datetime.now(timezone.utc) - timedelta(days=1)
                end_time = datetime.now(timezone.utc)
                profit = Mt5.history_deals_get(start_time, end_time)[-1].profit
                logger.info(f"Take profit reached. ({profit})\n")
                if Mt5.history_deals_get(start_time, end_time)[-1].symbol == self.symbol:
                    self.balance += profit
                self.statistics()

            elif ((points / Mt5.symbol_info(self.symbol).point) * -1) >= self.stop_loss:
                self.loss_deals += 1
                self.close_position(comment)
                start_time = datetime.now(timezone.utc) - timedelta(days=1)
                end_time = datetime.now(timezone.utc)
                profit = Mt5.history_deals_get(start_time, end_time)[-1].profit
                logger.info(f"Stop loss reached. ({profit})\n")
                if Mt5.history_deals_get(start_time, end_time)[-1].symbol == self.symbol:
                    self.balance += profit
                self.statistics()

    def days_end(self) -> bool:
        """Check if it is the end of trading for the day.

        Returns:
            bool: True if it is the end of trading for the day, False otherwise.
        """
        now = datetime.now(timezone.utc)
        return now.hour >= int(self.ending_time_hour) and now.minute >= int(self.ending_time_minutes)

    def trading_time(self) -> bool:
        """Check if it is within the allowed trading time.

        Returns:
            bool: True if it is within the allowed trading time, False otherwise.
        """
        now = datetime.now(timezone.utc)
        if int(self.start_time_hour) < now.hour < int(self.finishing_time_hour):
            return True
        if now.hour == int(self.start_time_hour):
            return now.minute >= int(self.start_time_minutes)
        if now.hour == int(self.finishing_time_hour):
            return now.minute < int(self.finishing_time_minutes)
        return False
