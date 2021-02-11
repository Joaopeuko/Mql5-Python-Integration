# Mql5-Python-Integration

## Patron who makes the difference!

1 - Joshua Greer

Help me make it possible. Be my [Patreon](https://www.patreon.com/joaopeuko).

## Introduction

I created this library because the development of an Expert Advisor in MQL5 can be complicated,while, in python, the same task flows better. 

I believe that the main advantage of using python, instead of MQL5, to develop an expert advisor is the possibility to implement machine learning, deep learning, and reinforcement learning to your code in a faster way. However, I still don´t cover these.

I find that using the “MetaTrader module for integration with Python” is straightforward; yet, there is space for improvement.

Thus, I created this library, aiming to transform the experience of Expert Advisor Creation. Python is a versatile language; it counts with a wide range of useful libraries, which, in turn, allows the implementation of diverse ideas, easily. 


## Installation


[pip](https://www.mql5.com/en/docs/integration/python_metatrader5) install MetaTrader5

```python
pip install MetaTrader5
```


## Expert Advisor

There is an expert advisor example for each different technology in the Expert Advisor folder.

### Simple Example 

[example.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/master/ExpertAdvisor/example.py)

 It uses just the MetaTrader5 library in the implementation. 

### Socket Example

[example_sockets_connection.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/master/ExpertAdvisor/example_sockets_connection.py) 


The “MetaTrader module for integration with Python” enables a wide range of possibilities; still, there is space for improvement. For instance, it lacks a connection to indicators.

That problem can be solved:
- Using Python indicators libraries that already exist through the internet.
- Re-creating all the indicators
- Creating a connection with MetaTrader5, asking for some indicators.

This example uses a socket connection to simplify the usage of indicators and it shows how easy it is to implement. You can find the indicator connection file [here](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/master/Include/indicator_connector.py).

To be able to use socket connection you need the client-side and the server-side to allow the communication.

The python code, that is used in this example, is the server-side that waits for the client-side to send the indicator result asked for.

The python code that is used in this example is the server-side that waits for the client-side to send the indicator result asked for. In order to use the client-side, it is possible to code it in MQL-language or to use the ones that I already created:

 - [here](https://www.mql5.com/en/market/product/57574) - Free - 5 Indicators
 - [here](https://www.mql5.com/en/market/product/58056) - Not Free - [38](https://www.mql5.com/en/docs/indicators) Indicators (5 from free indicators plus 33 new ones). The iCustom is not implemented.
 
To use the indicator in the expert advisor, you can call it providing the symbol name, all the other variables have pre-configured values. It always uses a time_frame for 1 minute.

[example_sockets_connection.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/master/ExpertAdvisor/example_sockets_connection.py)

```python
from include.indicator_connector import Indicator

indicator = Indicator()

moving_average = indicator.moving_average(symbol='PETR4')  # Brazilian Stock 
```

You can check [this](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/master/Include/indicator_connector.py) file to find some tips when calling an indicator, for example, on how to change the method or the applied price.

```python
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
```

When using the indicators, please use try and except; sometimes the result can return "None."

[example_sockets_connection.py](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/master/ExpertAdvisor/example_sockets_connection.py)

```python
from include.indicator_connector import Indicator

indicator = Indicator()

while True:
    try:
        moving_average = indicator.moving_average(symbol='PETR4')  # Brazilian Stock 
    except TypeError:
        pass
```

The indicator result is a dictionary.
```python
print(moving_average)
{'symbol': 'PETR4', 'time_frame': 1, 'period': 50, 'start_position': 0, 'method': 0, 'applied_price': 0, 'moving_average_result': 23.103}

print(moving_average['moving_average_result'])
23.103

```
