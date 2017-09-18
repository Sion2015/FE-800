
# coding: utf-8

# In[1]:

from .Portfolio import *
from .Black_Litterman import *

from pymongo import MongoClient
import pandas as pd
from pandas.io.json import json_normalize
ETF_tickers = ['VTI', 'SCHB', 'VEA', 'IXUS', 'IEMG', 'DVY', 'SCHD', 'VGSH',
                   'IEF', 'MUB', 'TFI', 'PZA', 'SCHP', 'DJP', 'VDE']
    # TLT is not included


# In[2]:




initial_data = Data(ETF_tickers, start_date="2013-01-01", end_date="2016-01-04")
P_matrix = np.diag(np.ones(len(ETF_tickers)))
Q_ARIMA = np.matrix([-0.004413366667244781, -0.004424015834531522, -0.005690773822704929, -0.005734796756841397, -0.005472827242047887, -0.0052321808471597914, -0.004364895249574041, -0.007686644049192283, -0.007867415841404813, -0.007274183151079553, -0.007435270639293345, -0.0074720911273814155, -0.007135610440594298, -0.007085256344163254, -0.009426469934431069]).transpose()
Q_affiliate = np.matrix([0.000449417,0.000449417,0.00342539500,0.00342539500,0.004385759898,0.000309345023,0.000309345023,0.000167661891,-0.000442237962,0.002160696, 0.0021606969, 0.0021606969, 0.0006686066, 0.0011797109, 0.0011797109]).transpose()

initial_blacklitterman = BlackLitterman(initial_data, P_matrix, Q_affiliate, 0.8).add_views(P_matrix, Q_ARIMA, 0.2)

initial_portfolio = Portfolio(initial_data, initial_blacklitterman, risk_tolerance=5)
#print(initial_portfolio.back_testing_result)


# In[5]:

host = 'localhost:27017'
backtest = initial_portfolio.back_testing_result


# In[6]:

# Initialize the collection Backtest
client = MongoClient([host])
#client.drop_database('RoboAdvisor')
db = client.RoboAdvisor
db.Backtest.drop()
posts = db.Backtest    
dates = sorted(backtest["daily_drift"].keys())
n = len(dates)
# set dates as _id
for e in range(n):
    date = dates[e]
    posts.insert_one({'_id': date})


# In[7]:

def upload_portfolio(backtest, dates, n, potfolio_name, ETF_tickers = ETF_tickers):
    # write eval(weights) code for mongodb part
    weights = [0] * len(ETF_tickers)
    for e in range(len(ETF_tickers)):
        weights[e] = '"' + ETF_tickers[e] + '": ' + ETF_tickers[e] 
    weights = ', '.join(weights)
    weights = '{' + weights + '}'
        
    for e in range(n):
        date = dates[e]
        drift =  backtest["daily_drift"][date]
        residual_cash = backtest["daily_residual_cash"][date]
        total_value =  backtest["daily_total_value"][date]   
        
        for e in range(len(ETF_tickers)):
            ETF_weights_exec = ETF_tickers[e] + ' = backtest["' + ETF_tickers[e]+  '"][date]'
            exec(ETF_weights_exec)
                
        backtest_data =  {"$set":{                    
                    potfolio_name:{
                        'drift': drift,
                        'residual_cash': residual_cash,
                        'total_value':total_value,
                        'weights':eval(weights)
                    }}}
        posts.update_one({'_id': date}, backtest_data)
    return


# In[8]:

upload_portfolio(backtest, dates, n, 'portfolio_test')


# In[ ]:



