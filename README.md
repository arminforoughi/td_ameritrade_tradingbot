# td_ameritrade_tradingbot


Here I use the td amitrade api to build a trading algorithm.

td_trade.py
are helper functions to get information from the api


macd_rsi_calc.py
gets price of a stock from price_history fucntion in td_trade.py.
Then class calculate_macd calculates macd and rsi

run.py
runs the algorithm
uses macd_rsi_calc.py then updates the data base on current market



