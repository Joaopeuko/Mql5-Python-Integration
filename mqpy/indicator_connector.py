"""Python integration module for technical indicators.

This module provides a bridge between Python and MT5 indicators through socket connections.
"""

from __future__ import annotations

import ast
import json
import socket
from typing import Any

from mqpy.logger import get_logger

# Configure logging
logger = get_logger(__name__)

# To be able to use it you need the MQL5 Service to send the data, it is possible to found it here:
# -------------------------------------------------------------------- #
# Free:
#     https://www.mql5.com/en/market/product/57574
#   - Bollinger Bands
#   - MACD
#   - Moving Average
#   - OBV On Balance Volume
#   - Stochastic
# -------------------------------------------------------------------- #
#     https://www.mql5.com/en/market/product/58056
#   - Accelerator Oscillator
#   - Accumulation/Distribution
#   - Adaptive Moving Average
#   - Alligator
#   - Average Directional Movement Index
#   - Average Directional Movement Index Wilder
#   - Average True Range
#   - Awesome Oscillator
#   - Bollinger Bands - Free
#   - Bears Power
#   - Bulls Power
#   - Chaikin Oscillator
#   - Commodity Channel Index
#   - DeMarker
#   - Double Exponential Moving Average
#   - Envelops
#   - Force Index
#   - Fractal Adaptive Moving Average
#   - Fractals
#   - Gator Oscillator
#   - Ichimoku Kinko Hyo
#   - MACD - Free
#   - Market Facilitation Index
#   - Momentum
#   - Money Flow Index
#   - Moving Average - Free
#   - Moving Average of Oscillator
#   - OBV On Balance Volume - Free
#   - Parabolic SAR
#   - Relative Strength Index
#   - Relative Vigor Index
#   - Standard Deviation
#   - Stochastic - Free
#   - Triple Exponential Average
#   - Triple Exponential Moving Average
#   - Variable Index Dynamic Average
#   - Volumes
#   - Williams' Percent Range
#
# -------------------------------------------------------------------- #


class Indicator:
    """A class for connecting to and retrieving data from MetaTrader 5 technical indicators.

    This class provides methods to connect to various technical indicators in MetaTrader 5
    through a socket connection. Each method corresponds to a specific technical indicator
    and returns its calculated values.
    """

    def __init__(self, address: str = "localhost", port: int = 9090, listen: int = 1) -> None:
        """Initialize the Indicator connector.

        Args:
            address (str): The address to bind to. Defaults to "localhost".
            port (int): The port to bind to. Defaults to 9090.
            listen (int): The number of connections to accept. Defaults to 1.

        Returns:
            None
        """
        self.address = address
        self.port = port
        self.listen = listen
        self.location = (address, port)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.address, self.port))
        self.s.listen(self.listen)

    # -------------------------------------------------------------------- #

    def accelerator_oscillator(
        self, symbol: str, time_frame: int = 1, start_position: int = 0
    ) -> dict[str, Any] | None:  # Change it if you want past values, zero is the most recent.
        """Calculate the Accelerator Oscillator.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"accelerator_oscillator,{symbol},{time_frame},{start_position}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def accumulation_distribution(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        # applied_volume:
        # 0 - VOLUME_TICK
        # 1 - VOLUME_REAL
        applied_volume: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Accumulation/Distribution.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            applied_volume (int): The volume type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"accumulation_distribution," f"{symbol}," f"{time_frame}," f"{start_position}," f"{applied_volume}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def adaptive_moving_average(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ama_period: int = 9,
        fast_ma_period: int = 2,
        slow_ma_period: int = 30,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 4,
    ) -> dict[str, Any] | None:
        """Calculate the Adaptive Moving Average.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ama_period (int): The period for the Adaptive Moving Average. Defaults to 9.
            fast_ma_period (int): The fast moving average period. Defaults to 2.
            slow_ma_period (int): The slow moving average period. Defaults to 30.
            applied_price (int): The price type for calculations. Defaults to 4.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"adaptive_moving_average,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{ama_period},"
                f"{fast_ma_period},"
                f"{slow_ma_period},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def alligator(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        jaw_period: int = 13,
        teeth_period: int = 8,
        lips_period: int = 5,
        # method:
        # 0 - MODE_SMA
        # 1 - MODE_EMA
        # 2 - MODE_SMMA
        # 3 - MODE_LWMA
        ma_method: int = 2,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 4,
    ) -> dict[str, Any] | None:
        """Calculate the Alligator.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            jaw_period (int): The period for the Alligator's jaw. Defaults to 13.
            teeth_period (int): The period for the Alligator's teeth. Defaults to 8.
            lips_period (int): The period for the Alligator's lips. Defaults to 5.
            ma_method (int): The method for the Alligator's moving average. Defaults to 2.
            applied_price (int): The price type for calculations. Defaults to 4.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"alligator,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{jaw_period},"
                f"{teeth_period},"
                f"{lips_period},"
                f"{ma_method},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def average_directional_index(
        self,
        symbol: str,
        time_frame: int = 1,
        period: int = 14,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
    ) -> dict[str, Any] | None:
        """Calculate the Average Directional Index.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            period (int): The period for the Average Directional Index. Defaults to 14.
            start_position (int): Starting position for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"average_directional_index," f"{symbol}," f"{time_frame}," f"{period}," f"{start_position}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def average_directional_index_wilder(
        self,
        symbol: str,
        time_frame: int = 1,
        period: int = 14,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
    ) -> dict[str, Any] | None:
        """Calculate the Average Directional Index Wilder.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            period (int): The period for the Average Directional Index Wilder. Defaults to 14.
            start_position (int): Starting position for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"average_directional_index_wilder," f"{symbol}," f"{time_frame}," f"{period}," f"{start_position}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def average_true_range(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 14,
    ) -> dict[str, Any] | None:
        """Calculate the Average True Range.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Average True Range. Defaults to 14.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"average_true_range," f"{symbol}," f"{time_frame}," f"{start_position}," f"{ma_period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def awesome_oscillator(
        self, symbol: str, time_frame: int = 1, start_position: int = 0
    ) -> dict[str, Any] | None:  # Change it if you want past values, zero is the most recent.
        """Calculate the Awesome Oscillator.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"awesome_oscillator," f"{symbol}," f"{time_frame}," f"{start_position}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #
    # Free
    def bollinger_bands(
        self,
        symbol: str,
        time_frame: int = 1,
        period: int = 20,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_shift: int = 0,
        deviation: float = 2.000,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Bollinger Bands.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            period (int): The period for the Bollinger Bands. Defaults to 20.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_shift (int): The shift for the moving average. Defaults to 0.
            deviation (float): The deviation for the Bollinger Bands. Defaults to 2.000.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"bollinger_bands,"
                f"{symbol},"
                f"{time_frame},"
                f"{period},"
                f"{start_position},"
                f"{ma_shift},"
                f"{deviation},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def bears_power(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 13,
    ) -> dict[str, Any] | None:
        """Calculate the Bears Power.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Bears Power. Defaults to 13.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"bears_power," f"{symbol}," f"{time_frame}," f"{start_position}," f"{ma_period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def bulls_power(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 13,
    ) -> dict[str, Any] | None:
        """Calculate the Bulls Power.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Bulls Power. Defaults to 13.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"bulls_power," f"{symbol}," f"{time_frame}," f"{start_position}," f"{ma_period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def chaikin_oscillator(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        fast_ma_period: int = 3,
        slow_ma_period: int = 10,
        # method:
        # 0 - MODE_SMA
        # 1 - MODE_EMA
        # 2 - MODE_SMMA
        # 3 - MODE_LWMA
        ma_method: int = 1,
        # applied_volume:
        # 0 - VOLUME_TICK
        # 1 - VOLUME_REAL
        applied_volume: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Chaikin Oscillator.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            fast_ma_period (int): The period for the fast moving average. Defaults to 3.
            slow_ma_period (int): The period for the slow moving average. Defaults to 10.
            ma_method (int): The method for the moving average. Defaults to 1.
            applied_volume (int): The volume type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"chaikin_oscillator,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{fast_ma_period},"
                f"{slow_ma_period},"
                f"{ma_method},"
                f"{applied_volume}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def commodity_channel_index(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 1,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 14,
        # For this Indicator, the applied price is shifted.
        # applied_price:
        # 1 - PRICE_CLOSE
        # 2 - PRICE_OPEN
        # 3 - PRICE_HIGH
        # 4 - PRICE_LOW
        # 5 - PRICE_MEDIAN
        # 6 - PRICE_TYPICAL
        # 7 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Commodity Channel Index.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 1.
            ma_period (int): The period for the Commodity Channel Index. Defaults to 14.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"commodity_channel_index,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{ma_period},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def demarker(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        period: int = 14,
    ) -> dict[str, Any] | None:
        """Calculate the DeMarker.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            period (int): The period for the DeMarker. Defaults to 14.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"demarker," f"{symbol}," f"{time_frame}," f"{start_position}," f"{period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        except ConnectionAbortedError:
            logger.exception("Connection aborted by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def double_exponential_moving_average(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 14,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Double Exponential Moving Average.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Double Exponential Moving Average. Defaults to 14.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"double_exponential_moving_average,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{ma_period},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

        # -------------------------------------------------------------------- #

    def envelopes(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 14,
        # method:
        # 0 - MODE_SMA
        # 1 - MODE_EMA
        # 2 - MODE_SMMA
        # 3 - MODE_LWMA
        ma_method: int = 0,
        # For this Indicator, the applied price is shifted.
        # applied_price:
        # 1 - PRICE_CLOSE
        # 2 - PRICE_OPEN
        # 3 - PRICE_HIGH
        # 4 - PRICE_LOW
        # 5 - PRICE_MEDIAN
        # 6 - PRICE_TYPICAL
        # 7 - PRICE_WEIGHTED
        applied_price: int = 1,
        deviation: float = 0.100,
    ) -> dict[str, Any] | None:
        """Calculate the Envelopes.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Envelopes. Defaults to 14.
            ma_method (int): The method for the Envelopes. Defaults to 0.
            applied_price (int): The price type for calculations. Defaults to 1.
            deviation (float): The deviation for the Envelopes. Defaults to 0.100.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"envelopes,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{ma_period},"
                f"{ma_method},"
                f"{applied_price},"
                f"{deviation}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    def force_index(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 13,
        # method:
        # 0 - MODE_SMA
        # 1 - MODE_EMA
        # 2 - MODE_SMMA
        # 3 - MODE_LWMA
        ma_method: int = 0,
        # applied_volume:
        # 0 - VOLUME_TICK
        # 1 - VOLUME_REAL
        applied_volume: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Force Index.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Force Index. Defaults to 13.
            ma_method (int): The method for the Force Index. Defaults to 0.
            applied_volume (int): The volume type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"force_index,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{ma_period},"
                f"{ma_method},"
                f"{applied_volume}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

        # -------------------------------------------------------------------- #

    def fractal_adaptive_moving_average(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 14,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Fractal Adaptive Moving Average.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Fractal Adaptive Moving Average. Defaults to 14.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"fractal_adaptive_moving_average,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{ma_period},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def fractals(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
    ) -> dict[str, Any] | None:
        """Calculate the Fractals.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"fractals," f"{symbol}," f"{time_frame}," f"{start_position}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #
    # https://www.mql5.com/en/forum/41357
    def gator_oscillator(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        jaw_period: int = 13,
        jaw_shift: int = 8,
        teeth_period: int = 8,
        teeth_shift: int = 5,
        lips_period: int = 5,
        lips_shift: int = 3,
        # method:
        # 0 - MODE_SMA
        # 1 - MODE_EMA
        # 2 - MODE_SMMA
        # 3 - MODE_LWMA
        ma_method: int = 2,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 4,
    ) -> dict[str, Any] | None:
        """Calculate the Gator Oscillator.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            jaw_period (int): The period for the jaw. Defaults to 13.
            jaw_shift (int): The shift for the jaw. Defaults to 8.
            teeth_period (int): The period for the teeth. Defaults to 8.
            teeth_shift (int): The shift for the teeth. Defaults to 5.
            lips_period (int): The period for the lips. Defaults to 5.
            lips_shift (int): The shift for the lips. Defaults to 3.
            ma_method (int): The method for the moving average. Defaults to 2.
            applied_price (int): The price type for calculations. Defaults to 4.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"gator_oscillator,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{jaw_period},"
                f"{jaw_shift},"
                f"{teeth_period},"
                f"{teeth_shift},"
                f"{lips_period},"
                f"{lips_shift},"
                f"{ma_method},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def ichimoku_kinko_hyo(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        tenkan_sen: int = 9,
        kijun_sen: int = 26,
        senkou_span_b: int = 52,
    ) -> dict[str, Any] | None:
        """Calculate the Ichimoku Kinko Hyo.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            tenkan_sen (int): The period for the Tenkan-sen. Defaults to 9.
            kijun_sen (int): The period for the Kijun-sen. Defaults to 26.
            senkou_span_b (int): The period for the Senkou Span B. Defaults to 52.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"ichimoku_kinko_hyo,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{tenkan_sen},"
                f"{kijun_sen},"
                f"{senkou_span_b}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #
    # Free
    def macd(
        self,
        symbol: str,
        time_frame: int = 1,
        fast_ema_period: int = 12,
        slow_ema_period: int = 26,
        signal_period: int = 9,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Moving Average Convergence Divergence.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            fast_ema_period (int): The period for the fast EMA. Defaults to 12.
            slow_ema_period (int): The period for the slow EMA. Defaults to 26.
            signal_period (int): The period for the signal line. Defaults to 9.
            start_position (int): Starting position for calculations. Defaults to 0.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"macd,"
                f"{symbol},"
                f"{time_frame},"
                f"{fast_ema_period},"
                f"{slow_ema_period},"
                f"{signal_period},"
                f"{start_position},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def market_facilitation_index(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        # applied_volume:
        # 0 - VOLUME_TICK
        # 1 - VOLUME_REAL
        applied_volume: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Market Facilitation Index.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            applied_volume (int): Volume type to use in calculations. Defaults to 0 (VOLUME_TICK).

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"market_facilitation_index," f"{symbol}," f"{time_frame}," f"{start_position}," f"{applied_volume}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def momentum(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        mom_period: int = 14,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Momentum.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            mom_period (int): The period for the Momentum. Defaults to 14.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"momentum," f"{symbol}," f"{time_frame}," f"{start_position}," f"{mom_period}," f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def money_flow_index(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 14,
        # applied_volume:
        # 0 - VOLUME_TICK
        # 1 - VOLUME_REAL
        applied_volume: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Money Flow Index.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Money Flow Index. Defaults to 14.
            applied_volume (int): The volume type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"money_flow_index,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{ma_period},"
                f"{applied_volume}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        finally:
            if "client_socket" in locals():
                client_socket.close()

        return None

    # -------------------------------------------------------------------- #

    def moving_average(
        self,
        symbol: str,
        time_frame: int = 1,
        period: int = 20,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        # method:
        # 0 - MODE_SMA
        # 1 - MODE_EMA
        # 2 - MODE_SMMA
        # 3 - MODE_LWMA
        method: int = 0,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Moving Average.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            period (int): The period for the Moving Average. Defaults to 20.
            start_position (int): Starting position for calculations. Defaults to 0.
            method (int): The method for the Moving Average. Defaults to 0.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"moving_average,"
                f"{symbol},"
                f"{time_frame},"
                f"{period},"
                f"{start_position},"
                f"{method},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def moving_average_of_oscillator(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        fast_ema_period: int = 12,
        slow_ema_period: int = 26,
        macd_sma_period: int = 9,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Moving Average of Oscillator.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            fast_ema_period (int): The period for the fast EMA. Defaults to 12.
            slow_ema_period (int): The period for the slow EMA. Defaults to 26.
            macd_sma_period (int): The period for the MACD SMA. Defaults to 9.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"moving_average_of_oscillator,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{fast_ema_period},"
                f"{slow_ema_period},"
                f"{macd_sma_period},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #
    # Free
    def obv(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        # applied_volume:
        # 0 - VOLUME_TICK
        # 1 - VOLUME_REAL
        applied_volume: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the On Balance Volume.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            applied_volume (int): The volume type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"obv," f"{symbol}," f"{time_frame}," f"{start_position}," f"{applied_volume}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def parabolic_sar(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        step: float = 0.02,
        maximum: float = 0.2,
    ) -> dict[str, Any] | None:
        """Calculate the Parabolic SAR.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            step (float): The step for the Parabolic SAR. Defaults to 0.02.
            maximum (float): The maximum for the Parabolic SAR. Defaults to 0.2.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"parabolic_sar," f"{symbol}," f"{time_frame}," f"{start_position}," f"{step}," f"{maximum}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def relative_strength_index(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 14,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Relative Strength Index.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Relative Strength Index. Defaults to 14.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"relative_strength_index,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{ma_period},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def relative_vigor_index(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 10,
    ) -> dict[str, Any] | None:
        """Calculate the Relative Vigor Index.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Relative Vigor Index. Defaults to 10.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"relative_vigor_index," f"{symbol}," f"{time_frame}," f"{start_position}," f"{ma_period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def standard_deviation(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 20,
        # method:
        # 0 - MODE_SMA
        # 1 - MODE_EMA
        # 2 - MODE_SMMA
        # 3 - MODE_LWMA
        ma_method: int = 0,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Standard Deviation.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Standard Deviation. Defaults to 20.
            ma_method (int): The method for the Standard Deviation. Defaults to 0.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"standard_deviation,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{ma_period},"
                f"{ma_method},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #
    # Free
    def stochastic(
        self,
        symbol: str,
        time_frame: int = 1,
        k_period: int = 5,
        d_period: int = 3,
        slowing: int = 3,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        # method:
        # 0 - MODE_SMA
        # 1 - MODE_EMA
        # 2 - MODE_SMMA
        # 3 - MODE_LWMA
        method: int = 0,
        # applied_price
        # 0 - STO_LOWHIGH
        # 1 - STO_CLOSECLOSE
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Stochastic.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            k_period (int): The period for the Stochastic. Defaults to 5.
            d_period (int): The period for the Stochastic. Defaults to 3.
            slowing (int): The slowing for the Stochastic. Defaults to 3.
            start_position (int): Starting position for calculations. Defaults to 0.
            method (int): The method for the Stochastic. Defaults to 0.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"stochastic,"
                f"{symbol},"
                f"{time_frame},"
                f"{k_period},"
                f"{d_period},"
                f"{slowing},"
                f"{start_position},"
                f"{method},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def triple_exponential_ma_oscillator(
        self,
        symbol: str,
        time_frame: int,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        count: int = 100,  # Number of elements to be calculated.
        ma_period: int = 14,
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Triple Exponential Moving Average Oscillator.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations.
            start_position (int): Starting position for calculations. Defaults to 0.
            count (int): Number of elements to calculate. Defaults to 100.
            ma_period (int): Moving average period. Defaults to 14.
            applied_price (int): Price type to use in calculations. Defaults to 0 (PRICE_CLOSE).

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            try:
                data = f"TEMA_OSC,{symbol},{time_frame},{start_position},{count},{ma_period},{applied_price}"
                client_socket.send(data.encode())
                response = client_socket.recv(1024).decode()
                return ast.literal_eval(response)
            except ValueError:
                logger.exception("Connection lost to MQL5 Service")
        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")
        finally:
            client_socket.close()
        return None

    # -------------------------------------------------------------------- #

    def triple_exponential_moving_average(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values,
        # zero is the most recent.
        ma_period: int = 14,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Triple Exponential Moving Average.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            ma_period (int): The period for the Triple Exponential Moving Average. Defaults to 14.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"triple_exponential_moving_average,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{ma_period},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def variable_index_dynamic_average(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        cmo_period: int = 9,
        ema_period: int = 12,
        # applied_price:
        # 0 - PRICE_CLOSE
        # 1 - PRICE_OPEN
        # 2 - PRICE_HIGH
        # 3 - PRICE_LOW
        # 4 - PRICE_MEDIAN
        # 5 - PRICE_TYPICAL
        # 6 - PRICE_WEIGHTED
        applied_price: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Variable Index Dynamic Average.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            cmo_period (int): The period for the CMO. Defaults to 9.
            ema_period (int): The period for the EMA. Defaults to 12.
            applied_price (int): The price type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = (
                f"variable_index_dynamic_average,"
                f"{symbol},"
                f"{time_frame},"
                f"{start_position},"
                f"{cmo_period},"
                f"{ema_period},"
                f"{applied_price}"
            )

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def volumes(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        # applied_volume:
        # 0 - VOLUME_TICK
        # 1 - VOLUME_REAL
        applied_volume: int = 0,
    ) -> dict[str, Any] | None:
        """Calculate the Volumes.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            applied_volume (int): The volume type for calculations. Defaults to 0.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"volumes," f"{symbol}," f"{time_frame}," f"{start_position}," f"{applied_volume}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")

    # -------------------------------------------------------------------- #

    def williams_percent_range(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        calc_period: int = 14,
    ) -> dict[str, Any] | None:
        """Calculate the Williams Percent Range.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for calculations. Defaults to 1.
            start_position (int): Starting position for calculations. Defaults to 0.
            calc_period (int): The period for the Williams Percent Range. Defaults to 14.

        Returns:
            dict[str, Any] | None: The calculated values if successful, None otherwise.
        """
        try:
            client_socket, address = self.s.accept()
            message = f"williams_percent_range," f"{symbol}," f"{time_frame}," f"{start_position}," f"{calc_period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                logger.exception("Connection lost to MQL5 Service")

        except ConnectionResetError:
            logger.exception("Connection reset by MQL5 Service")

        except ConnectionAbortedError:
            logger.exception("Connection reset by MQL5 Service")
