import ccxt
import os
import numpy as np
import pandas as pd
import datetime
import plotly.graph_objs as go
from dotenv import load_dotenv
load_dotenv()

try:
    # Initialize exchange client
    ccxtBinance = ccxt.binance({
        'apiKey': os.getenv('apiKey'),
        'secret': os.getenv('secret')
    })

    # print(exchange.fetch_balance())
    # print(exchange.markets)

except Exception as e:
    print("Error:", e)

symbol='ETH/USDT'
granularity = '1d'
start_date = "19 June, 2022"
utc_start_s = datetime.datetime.strptime(start_date, '%d %B, %Y').replace(tzinfo=datetime.timezone.utc).timestamp()
end_date =  "19 March, 2023"
utc_stop_s = datetime.datetime.strptime(end_date, '%d %B, %Y').replace(tzinfo=datetime.timezone.utc).timestamp()
delta_time_s = (utc_stop_s-utc_start_s)
span = delta_time_s/60./30 # number of 30m intervals from start to end

ohlcv_btceur_binance = np.array(ccxtBinance.fetchOHLCV (symbol, timeframe = granularity, since = int(utc_start_s*1000), limit=int(span)))

df_ohlcv_btceur_binance = pd.DataFrame(ohlcv_btceur_binance.reshape(-1, 6), dtype=float, columns=('Open Time','Open','High','Low','Close','Volume'))
df_ohlcv_btceur_binance['Open Time'] = pd.to_datetime(df_ohlcv_btceur_binance['Open Time'], unit='ms')

# plot candlesticks using plotly
fig = go.Figure(data=[go.Candlestick(x=df_ohlcv_btceur_binance['Open Time'],
                open=df_ohlcv_btceur_binance['Open'],
                high=df_ohlcv_btceur_binance['High'],
                low=df_ohlcv_btceur_binance['Low'],
                close=df_ohlcv_btceur_binance['Close'])])
fig.update_yaxes(title_text=symbol)
fig.update_layout(title = "OHLCV from  Binance")
fig.show()


# Define trading parameters
# symbol = 'BTC/USDT'
# amount = 0.01
# buy_level = 0.618
# sell_level = -0.236
# stop_loss = 0.71

# # Retrieve current price data
# ticker = exchange.fetch_ticker(symbol)
# price = ticker['close']

# # Calculate Fibonacci levels
# high = ticker['high']
# low = ticker['low']
# diff = high - low
# fib_618 = high - (diff * buy_level)
# fib_neg_236 = high - (diff * abs(sell_level))

# # Check if current price is below 61.8% level
# if price < fib_618:
#     # Calculate buy order parameters
#     buy_price = price
#     sell_price = fib_neg_236
#     stop_price = high * stop_loss
    
#     # Place buy order
#     order = exchange.create_limit_buy_order(symbol, amount, buy_price)
    
#     # Wait for order to fill
#     order_id = order['id']
#     while True:
#         order_status = exchange.fetch_order(order_id)['status']
#         if order_status == 'closed':
#             break
    
#     # Place sell order and stop loss order
#     exchange.create_limit_sell_order(symbol, amount, sell_price)
#     exchange.create_stop_loss_order(symbol, amount, stop_price, {'stopPrice': stop_price})