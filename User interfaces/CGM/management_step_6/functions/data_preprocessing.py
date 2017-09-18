# coding: utf-8
import pandas as pd
from .collection_ETF import *
import numpy as np
import pyfolio as pf
from scipy.stats import norm

def get_mktcap_weight(ETF_tickers, host='155.246.104.19:27017'):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    collection = db.ETF
    cursor = collection.find({"_id":{'$in': ETF_tickers}}, {"summary.assets_under_management_B":1})
    if cursor.count() == 0:
        print("Nothing find")
        return
    else:
        mktcap = json_normalize(list(cursor))
        weight = pd.DataFrame(mktcap["summary.assets_under_management_B"] / sum(mktcap["summary.assets_under_management_B"]))
        weight.columns = ["mktcap_weight"]
        weight.index = mktcap["_id"]
        # Follow the original order
        weight['ETF_cat'] = pd.Categorical(weight.index, categories=ETF_tickers, ordered=True)
        weight = weight.sort_values(by='ETF_cat')
        weight = weight[["mktcap_weight"]]
        return weight

def get_daily_price(host, ETF=None, startdate=None, enddate=None):
        # ETF selection
        if ETF == None:
            price = get_hist_data_close_for_many(host=host)
        else:
            price = get_hist_data_close_for_many(ETF=ETF, host=host)

        # Time period selection
        if startdate == None:
            if enddate == None:
                price = price[:][:]
            else:
                price = price[:enddate][:]
        else:
            if enddate == 0:
                price = price[startdate:][:]
            else:
                price = price[startdate:enddate][:]
        return price

def get_daily_expense(host, ETF):
    expense_ratio = get_summary_data_all(host = host)["expense_ratio%"]
    daily_expens_dict = {}
    N = len(ETF)
    for e in ETF:
        daily_expens_dict[e] = expense_ratio[e]/25200
    return daily_expens_dict

def get_daily_rtn(host, ETF=object(), startdate=object(), enddate=object()):
    # ETF selection
    if ETF is object():
        price = get_hist_data_close_for_many(host=host)
    else:
        price = get_hist_data_close_for_many(ETF=ETF, host=host)
        
    # Calculate returns
    rtn = price / price.shift(1) - 1
    rtn = rtn.dropna()
    
    # Time period selection
    if startdate is object():
        if enddate is object():
            rtn = rtn[:][:]
        else:
            rtn = rtn[:enddate][:]
    else:
        if enddate is object():
            rtn = rtn[startdate:][:]
        else:
            rtn = rtn[startdate:enddate][:]
            
    return rtn


def get_daily_rtn_exclude_expense(host, ETF=None, startdate=None, enddate=None):
    # ETF selection
    if ETF == None:
        price = get_hist_data_close_for_many(host=host)
    else:
        price = get_hist_data_close_for_many(ETF=ETF, host=host)

    # Caculate returns
    rtn = price / price.shift(1) - 1
    rtn = rtn.dropna()
    daily_expense_dict = get_daily_expense(host, ETF)
    for e in ETF:
        rtn[e] = rtn[e] - daily_expense_dict[e]

    # Time period selection
    if startdate == None:
        if enddate == None:
            rtn = rtn[:][:]
        else:
            rtn = rtn[:enddate][:]
    else:
        if enddate == 0:
            rtn = rtn[startdate:][:]
        else:
            rtn = rtn[startdate:enddate][:]

    return rtn

def get_weekly_rtn(host, ETF=object(), startdate=object(), enddate=object()):
    # ETF selection
    if ETF == object():
        price = get_hist_data_close_for_many(host=host)
    else:
        price = get_hist_data_close_for_many(ETF = ETF ,host=host)
        
    # Calculate returns
    exp_w_price = price.resample("W").mean()
    rtn = exp_w_price.shift(1)/exp_w_price - 1
    rtn = rtn.dropna()
    
    # Time period selection
    if startdate == object():
        if enddate == object():
            rtn = rtn[:][:]
        else:
            rtn = rtn[:enddate][:]
    else:
        if enddate == object():
            rtn = rtn[startdate:][:]
        else:
            rtn = rtn[startdate:enddate][:]
            
    return rtn * 5



def get_monthly_rtn(host, ETF=object(), startdate=object(), enddate=object()):
    # ETF selection
    if ETF==object():
        price = get_hist_data_close_for_many(host=host)
    else:
        price = get_hist_data_close_for_many(ETF = ETF ,host=host)
        
    # Caculate returns
    exp_m_price = price.resample("M").mean()
    rtn = exp_m_price.shift(1)/exp_m_price - 1
    rtn = rtn.dropna()
    
    # Time period selection
    if startdate==object():
        if enddate==object():
            rtn = rtn[:][:]
        else:
            rtn = rtn[:enddate][:]
    else:
        if enddate==object():
            rtn = rtn[startdate:][:]
        else:
            rtn = rtn[startdate:enddate][:]
            
    return rtn * 21

def get_cumulative_rtn(host, startdate, enddate, ETF=object()):
    # Check dates
    if startdate >= enddate:
        print ("Input error: startdate >= enddate")
        return
    else:
        # ETF selection
        if ETF == object():
            price = get_hist_data_close_for_many(host=host)
        else:
            price = get_hist_data_close_for_many(ETF=ETF, host=host)
        price = price.dropna()
        # Caculate cumulative  returns
        price = price[startdate:enddate][:]
        df1 = price[:1]
        df2 = price[-1:]
        # index1 = df1.index
        # index2 = df2.index
        df1.index = df2.index
        cumulative_rtn = df2 / df1 - 1

        return cumulative_rtn

def get_RA_exp_rtn(asset_class, host):
    client = MongoClient(host)
    db = client.RoboAdvisor
    request = db.ResearchAffiliates
    cursor = request.find({"_id": asset_class },{ "_id":0, "views.exp_rtn%": 1})
    exp_rtn = json_normalize(list(cursor))["views.exp_rtn%"]
    return exp_rtn[0]

def get_RA_views(ETF, host):
    # Define the mapping
    asset_class_dic = {
        "US STOCKS": "US Large",
        "FOREIGN DEVELOPED STOCKS": "EAFE Equity",
        "EMERGING MARKET STOCKS": "EM Equity",
        "DIVIDEND GROWTH STOCKS": "US Small",
        "US GOVERNMENT BONDS": "ST US Treas", # SHORT TERM
        "MUNICIPAL BONDS": "LT US Treas", # Whatever
        "TREASURY INFLATION-PROTECTED SECURITIES (TIPS)": "US Tips",
        "NATURAL RESOURCES": "Commodities",# Whatever
        # todo: affiliate returns
    }
    N = len(ETF)
    RA_views = [0]*N
    for i in range(N):
        asset_class = get_asset_class(host=host, ticker=ETF[i])
        asset_class = asset_class_dic[asset_class]
        RA_views[i] = get_RA_exp_rtn(host=host, asset_class=asset_class) / 100 / 252
    return RA_views

def calculate_daily_return(price_data, if_print=False):
    # stock_returns = self.price.shift(1) / self.price - 1
    stock_returns = price_data / price_data.shift(1) - 1  # date under ascending order
    # self.stock_return = self.stock_price.apply(get_stock_return)
    stock_returns = stock_returns.dropna()
    if if_print:
        print("Return Matrix is \n", stock_returns)
    return stock_returns

def calculate_annual_return(stock_return):
    annual_return = np.mean(stock_return, axis=0) * 252
    return annual_return

def calculate_anual_vol(stock_return):
    annual_vol = np.std(stock_return, axis=0) * np.sqrt(252)
    return annual_vol

def calculate_sharpe_ratio(stock_return, risk_free_rate = 0.75/100):
    annual_return = np.mean(stock_return, axis=0) * 252
    annual_vol = np.std(stock_return, axis=0) * np.sqrt(252)
    sharpe_ratio = (annual_return - risk_free_rate) / annual_vol
    return sharpe_ratio

def calculate_VaR(vol, level = 0.99, time_period=1):
    return norm.ppf(level)* vol * np.sqrt(time_period)




def main():
    host = '155.246.104.19:27017' # use Stevens' mongoDB host
    #host = 'localhost:27017'

    ETF = ['VTI', 'ITOT', 'SCHB', 'VEA', 'IXUS']

    print(get_mktcap_weight(host=host, ETF_tickers=ETF))
    # daily_rtn = get_daily_rtn(host, ETF=["ITOT", "SCHB", "VEA", "IXUS"], startdate="2012-10-31", enddate="2017-10-31")
    # print(daily_rtn)
    # daily_rtn =get_daily_rtn(host, enddate="2012-10-31")
    # print(daily_rtn)
    # weekly_rtn = get_weekly_rtn(host, enddate="2012-12-4")
    # print(weekly_rtn)
    # monthly_rtn = get_monthly_rtn(host, enddate="2013-5-4")
    # print(monthly_rtn)


if __name__ == "__main__":
    main()
