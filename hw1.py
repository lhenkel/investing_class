import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
from itertools import product

ls_symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
dt_start = dt.datetime(2006, 1, 1)
dt_end = dt.datetime(2010, 12, 31)
dt_timeofday = dt.timedelta(hours=16)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
c_dataobj = da.DataAccess('Yahoo')
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))
na_price = d_data['close'].values

def simulate(startdate, enddate, stock_list, ratios):
	vol = daily_ret = sharpe = cum_ret  = 0.0
	
	#ls_symbols = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
	#dt_start = dt.datetime(2006, 1, 1)
	#dt_end = dt.datetime(2010, 12, 31)
	dt_timeofday = dt.timedelta(hours=16)
	ldt_timestamps = du.getNYSEdays(startdate, enddate, dt_timeofday)	
		
	c_dataobj = da.DataAccess('Yahoo')
	ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
	ldf_data = c_dataobj.get_data(ldt_timestamps, stock_list, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))	
	
	na_price = d_data['close'].values
	
	na_normalized_price = na_price / na_price[0, :]
	
	na_rets = na_normalized_price.copy()
	
	divided_prices = na_normalized_price * ratios
	
	port_val = np.sum(divided_prices, axis=1)
	#port_val
	#na_port_total = np.cumprod(na_portrets + 1)
	cum_ret = port_val[-1]
	
	daily_rets = tsu.returnize0(port_val)
	std_dev = np.std(daily_rets)
	sharpe = math.sqrt(250) * np.mean(daily_rets) / std_dev
	vol = std_dev
	
	return vol, np.mean(daily_rets), sharpe, cum_ret 

startdate = dt.datetime(2006, 1, 1)
enddate = dt.datetime(2010, 12, 31)
symbol_list = ['GOOG','AAPL','GLD','XOM']

#vol, daily_ret, sharpe, cum_ret = simulate(startdate, enddate, ['GOOG','AAPL','GLD','XOM'], [0.2,0.3,0.4,0.1])

#stock_list = ['GOOG','AAPL','GLD','XOM']

stock_list = ['BRCM', 'TXN', 'IBM', 'HNZ'] 
stock_list =  ['AAPL', 'GOOG', 'IBM', 'MSFT'] 
#ratios = [0.2,0.3,0.4,0.1]

number_of_stocks = len(stock_list)

list_of_ratios = []
for digits in product('0123456789', repeat=number_of_stocks):
	if sum(map(int, digits)) == 10:
		floats = [float(x)/10.0 for x in digits]
		list_of_ratios.append(floats)


best_sharpe_num = 0.0
best_sharpe_ratios = []
best_return = 0.0

for ratio in list_of_ratios:
	vol, daily_ret, sharpe, cum_ret = simulate(startdate, enddate, stock_list, ratio)
	if sharpe > best_sharpe_num:
		best_sharpe_num = sharpe
		best_sharpe_ratios = ratio
		best_return = cum_ret
	