"""MetaQuotes Language 5 Python integration module for technical indicators.
This module provides a bridge between Python and MT5 indicators through socket connections.
"""

import json
import socket
from typing import Any, Dict, Optional

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
    def __init__(self, address: str = "localhost", port: int = 9090, listen: int = 1) -> None:
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
    ) -> Optional[Dict[str, Any]]:  # Change it if you want past values, zero is the most recent.
        try:
            client_socket, address = self.s.accept()
            message = f"accelerator_oscillator," f"{symbol}," f"{time_frame}," f"{start_position}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")
                return None

        except ConnectionResetError:
            pass
        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def average_directional_index(
        self,
        symbol: str,
        time_frame: int = 1,
        period: int = 14,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"average_directional_index," f"{symbol}," f"{time_frame}," f"{period}," f"{start_position}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def average_directional_index_wilder(
        self,
        symbol: str,
        time_frame: int = 1,
        period: int = 14,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def average_true_range(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 14,
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"average_true_range," f"{symbol}," f"{time_frame}," f"{start_position}," f"{ma_period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def awesome_oscillator(
        self, symbol: str, time_frame: int = 1, start_position: int = 0
    ) -> Optional[Dict[str, Any]]:  # Change it if you want past values, zero is the most recent.
        try:
            client_socket, address = self.s.accept()
            message = f"awesome_oscillator," f"{symbol}," f"{time_frame}," f"{start_position}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def bears_power(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 13,
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"bears_power," f"{symbol}," f"{time_frame}," f"{start_position}," f"{ma_period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def bulls_power(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 13,
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"bulls_power," f"{symbol}," f"{time_frame}," f"{start_position}," f"{ma_period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

        # -------------------------------------------------------------------- #

    def demarker(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        period: int = 14,
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"demarker," f"{symbol}," f"{time_frame}," f"{start_position}," f"{period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def fractals(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"fractals," f"{symbol}," f"{time_frame}," f"{start_position}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def ichimoku_kinko_hyo(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        tenkan_sen: int = 9,
        kijun_sen: int = 26,
        senkou_span_b: int = 52,
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #
    # Free
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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"obv," f"{symbol}," f"{time_frame}," f"{start_position}," f"{applied_volume}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def parabolic_sar(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        step: float = 0.02,
        maximum: float = 0.2,
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"parabolic_sar," f"{symbol}," f"{time_frame}," f"{start_position}," f"{step}," f"{maximum}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def relative_vigor_index(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        ma_period: int = 10,
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"relative_vigor_index," f"{symbol}," f"{time_frame}," f"{start_position}," f"{ma_period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def triple_exponential_ma_oscillator(
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
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = (
                f"triple_exponential_ma_oscillator,"
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
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
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

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
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"volumes," f"{symbol}," f"{time_frame}," f"{start_position}," f"{applied_volume}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #

    def williams_percent_range(
        self,
        symbol: str,
        time_frame: int = 1,
        start_position: int = 0,  # Change it if you want past values, zero is the most recent.
        calc_period: int = 14,
    ) -> Optional[Dict[str, Any]]:
        try:
            client_socket, address = self.s.accept()
            message = f"williams_percent_range," f"{symbol}," f"{time_frame}," f"{start_position}," f"{calc_period}"

            client_socket.send(bytes(message, "utf-8"))
            data = client_socket.recv(1024)

            result = data.decode("utf-8")
            try:
                return json.loads(result)

            except ValueError:
                print("Connection lost to MQL5 Service")

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass
