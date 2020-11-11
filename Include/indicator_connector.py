import socket
import json


# To be able to use it you need the MQL5 Service to send the data, it is possible to found it here:
# Free:
#   https://www.mql5.com/en/market/product/57574

class Indicator:
    def __init__(self,
                 address='localhost',
                 port=9090,
                 listen=1):

        self.address = address
        self.port = port
        self.listen = listen
        self.location = (address, port)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.address, self.port))
        self.s.listen(self.listen)

    # -------------------------------------------------------------------- #
    def bollinger_bands(self,
                        symbol,
                        time_frame=1,
                        period=20,
                        start_position=0,  # Change it if you want past values, zero is the most recent.
                        ma_shift=0,
                        deviation=2.000,
                        # applied_price:
                        # 0 - PRICE_CLOSE
                        # 1 - PRICE_OPEN
                        # 2 - PRICE_HIGH
                        # 3 - PRICE_LOW
                        # 4 - PRICE_MEDIAN
                        # 5 - PRICE_TYPICAL
                        # 6 - PRICE_WEIGHTED
                        applied_price=0):

        try:
            client_socket, address = self.s.accept()
            message = (f"bollinger_bands,"
                       f"{symbol},"
                       f"{time_frame},"
                       f"{period},"
                       f"{start_position},"
                       f"{ma_shift},"
                       f"{deviation},"
                       f"{applied_price}")

            client_socket.send(bytes(message, 'utf-8'))
            data = client_socket.recv(1024)

            result = data.decode('utf-8')
            try:
                return json.loads(result)

            except ValueError:
                print('Connection lost to MQL5 Service')
                pass

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #
    def macd(self,
             symbol,
             time_frame=1,
             fast_ema_period=12,
             slow_ema_period=26,
             signal_period=9,
             start_position=0,  # Change it if you want past values, zero is the most recent.
             # applied_price:
             # 0 - PRICE_CLOSE
             # 1 - PRICE_OPEN
             # 2 - PRICE_HIGH
             # 3 - PRICE_LOW
             # 4 - PRICE_MEDIAN
             # 5 - PRICE_TYPICAL
             # 6 - PRICE_WEIGHTED
             applied_price=0):

        try:
            client_socket, address = self.s.accept()
            message = (f"macd,"
                       f"{symbol},"
                       f"{time_frame},"
                       f"{fast_ema_period},"
                       f"{slow_ema_period},"
                       f"{signal_period},"
                       f"{start_position},"
                       f"{applied_price}")

            client_socket.send(bytes(message, 'utf-8'))
            data = client_socket.recv(1024)

            result = data.decode('utf-8')
            try:
                return json.loads(result)

            except ValueError:
                print('Connection lost to MQL5 Service')
                pass

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #
    def moving_average(self,
                       symbol,
                       time_frame=1,
                       period=20,
                       start_position=0,  # Change it if you want past values, zero is the most recent.
                       # method:
                       # 0 - MODE_SMA
                       # 1 - MODE_EMA
                       # 2 - MODE_SMMA
                       # 3 - MODE_LWMA
                       method=0,
                       # applied_price:
                       # 0 - PRICE_CLOSE
                       # 1 - PRICE_OPEN
                       # 2 - PRICE_HIGH
                       # 3 - PRICE_LOW
                       # 4 - PRICE_MEDIAN
                       # 5 - PRICE_TYPICAL
                       # 6 - PRICE_WEIGHTED
                       applied_price=0):

        try:
            client_socket, address = self.s.accept()
            message = (f"moving_average,"
                       f"{symbol},"
                       f"{time_frame},"
                       f"{period},"
                       f"{start_position}," 
                       f"{method},"
                       f"{applied_price}")

            client_socket.send(bytes(message, 'utf-8'))
            data = client_socket.recv(1024)

            result = data.decode('utf-8')
            try:
                return json.loads(result)

            except ValueError:
                print('Connection lost to MQL5 Service')
                pass

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

        # -------------------------------------------------------------------- #

    def obv(self,
            symbol,
            time_frame=1,
            start_position=0,  # Change it if you want past values, zero is the most recent.
            # applied_volume:
            # 0 - VOLUME_TICK
            # 1 - VOLUME_REAL
            applied_volume=0):

        try:
            client_socket, address = self.s.accept()
            message = (f"obv,"
                       f"{symbol},"
                       f"{time_frame},"
                       f"{start_position},"
                       f"{applied_volume}")

            client_socket.send(bytes(message, 'utf-8'))
            data = client_socket.recv(1024)

            result = data.decode('utf-8')
            try:
                return json.loads(result)

            except ValueError:
                print('Connection lost to MQL5 Service')
                pass

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass

    # -------------------------------------------------------------------- #
    def stochastic(self,
                   symbol,
                   time_frame=1,
                   k_period=5,
                   d_period=3,
                   slowing=3,
                   start_position=0,  # Change it if you want past values, zero is the most recent.
                   # method:
                   # 0 - MODE_SMA
                   # 1 - MODE_EMA
                   # 2 - MODE_SMMA
                   # 3 - MODE_LWMA
                   method=0,
                   # applied_price
                   # 0 - STO_LOWHIGH
                   # 1 - STO_CLOSECLOSE
                   applied_price=0):

        try:
            client_socket, address = self.s.accept()
            message = (f"stochastic,"
                       f"{symbol},"
                       f"{time_frame},"
                       f"{k_period},"
                       f"{d_period},"
                       f"{slowing},"
                       f"{start_position},"
                       f"{method},"
                       f"{applied_price}")

            client_socket.send(bytes(message, 'utf-8'))
            data = client_socket.recv(1024)

            result = data.decode('utf-8')
            try:
                return json.loads(result)

            except ValueError:
                print('Connection lost to MQL5 Service')
                pass

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            pass
