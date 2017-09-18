from yahoo_finance import Share
import time
import quandl as qd
from pymongo import MongoClient
import urllib.request
from bs4 import BeautifulSoup
import datetime
import pprint
import pandas as pd
from pandas.io.json import json_normalize

host = 'localhost:27017'
ETF_tickers = ['VTI', 'VEA', 'VWO', 'VIG', 'XLE', 'SCHP', 'MUB']
csv_name = "core_asset_class_expected_returns.csv"

def build_collection_ResearchAffiliates(host=host, ETF=ETF_tickers, csv_name=csv_name):
    core_asset_class = pd.read_csv(csv_name)
    client = MongoClient(host)
    db = client.RoboAdvisor
    db.ResearchAffiliates.drop()
    posts = db.ResearchAffiliates
    N = len(core_asset_class)
    for i in range(N):
        posts.insert_one({
        "_id": core_asset_class["Asset class"][i],
        "views": {
                    "exp_rtn%": core_asset_class["Expected Return %"][i],
                    "volatility%": core_asset_class["Volatility %"][i]
                }
    })
    return

def build_ETF(ETF, asset_class,quandlKey = 'e9mjr1zRrH1o_5zBfEEy',
              start_date="2010-01-01", host = 'localhost:27017'):
    qd.ApiConfig.api_key = quandlKey
    N = len(ETF)
    address = "http://www.etf.com/"
    inception_date = [0]*N
    legal_structure = [0]*N
    expense_ratio = [0]*N
    assets_under_management = [0]*N
    average_daily_volume = [0]*N
    average_spread = [0]*N
    Max_LT_Capital_Gains_Rate = [0]*N
    Max_ST_Capital_Gains_Rate = [0]*N
    median_tracking_diff_12m = [0]*N
    ETF_dic = dict(zip(ETF, asset_class))

    # Initialize the collection ETF
    client = MongoClient()
    #client.drop_database('RoboAdvisor')
    db = client.RoboAdvisor
    db.ETF.drop()
    posts = db.ETF

    # Add ticker as _id
    for e in range(N):
        posts.insert_one({'_id': ETF[e]})

    # Add Asset class
    for e in range(N):
        asset = ETF[e]
        assetClass = ETF_dic[asset]
        posts.update_one({'_id': asset}, {'$set': {"asset_class": assetClass}})

    # Get summary
    for e in range(N):
        url = address + ETF[e]
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        bsObj = BeautifulSoup(html, "html.parser")

        inception_date[e] = bsObj.find("span", {"class":"field-r-inception-date"}).get_text()
        d = datetime.datetime.strptime(inception_date[e], '%m/%d/%y')
        inception_date[e] =  d.strftime('%Y-%m-%d')

        legal_structure[e] = bsObj.find("span", {"class":"field-r-legal-structure"}).get_text()


        expense_ratio[e] = bsObj.find("span", {"class":"field-r-expense-ratio"}).get_text()
        # convert ['0.05%'] to [0.05]
        temp = expense_ratio[e]
        expense_ratio[e] = float(temp[:-1])

        assets_under_management[e] = bsObj.find("span", {"class":"field-r-assets-under-management"}).get_text()
        # start: every element is in format ['$75.04 B'] or ['$866.61 M']
        # end: every element is in format [75.04] in billion
        temp1 = assets_under_management[e].split(' ')
        temp2 = temp1[0]
        temp1[0] = float(temp2[1:]) # get rid of the first element '$'
        if temp1[1] == 'M':
            temp1[0] = temp1[0]/1000 # convert million into billion
        assets_under_management[e] = temp1[0]

        average_daily_volume[e] = bsObj.find("span", {"class":"field-r-average-daily--volume"}).get_text()
        # start: every element is in format ['$274.26 M']
        # end: every element is in format [274.26]
        temp1 = average_daily_volume[e].split(' ')
        temp2 = temp1[0]
        temp1[0] = float(temp2[1:]) # get rid of the first element '$'
        if temp1[1] == 'B':
            temp1[0] = temp1[0]*1000 # convert billion into million
        average_daily_volume[e] = temp1[0]

        average_spread[e] = bsObj.find("span", {"class":"field-r-average-spread-"}).get_text()
        # convert ['0.05%'] to [0.05]
        temp = average_spread[e]
        average_spread[e] = float(temp[:-1])


        temp = bsObj.find("span", {"class":"field-r-max-lt-st-cap-gains-rate"}).get_text()
        # convert ["20.00% / 39.60%"] into [20.00] and [39.60] in different vectors
        temp = temp.split(' / ')
        temp1 = temp[0]
        temp2 = temp[1]
        Max_LT_Capital_Gains_Rate[e] = float(temp1[:-1])
        Max_ST_Capital_Gains_Rate[e] = float(temp2[:-1])


        median_tracking_diff_12m[e] = bsObj.find("span", {"class":"field-r-median-tracking-diff-12m"}).get_text()
        # convert ['0.05%'] to [0.05]
        temp = median_tracking_diff_12m[e]
        median_tracking_diff_12m[e] = float(temp[:-1])

    # Add summary data
    for e in range(N):
        asset = ETF[e]
        posts.update_one(
           { '_id': asset },
           { '$set':
            {'summary':
             {
              'date_of_summary': datetime.date.today().strftime('%Y-%m-%d'),
              'inception_date':inception_date[e],
              'legal_structure':legal_structure[e],
              'expense_ratio%':expense_ratio[e],
              'assets_under_management_B': assets_under_management[e],
              'average_daily_volume_M': assets_under_management[e],
              'average_spread%': average_spread[e],
              'Max_LT_Capital_Gains_Rate%': Max_LT_Capital_Gains_Rate[e],
              'Max_ST_Capital_Gains_Rate%': Max_ST_Capital_Gains_Rate[e],
              'median_tracking_diff_12m%': median_tracking_diff_12m[e]
             }
            }
           },
           upsert = True
        )

    # Add historical data
    #apiCall = 1
    for e in range(N):
        asset = ETF[e]
        #if apiCall%20 == 0:
        #    print("Sleeping for 10 min every 20 calls")
        #    time.sleep(11*60)
        #apiCall = apiCall+1
        print(asset + " is start!")
        #ETFs_data = None
        if asset is 'VGSH': # VGSH is in NASDAQ
            ETFs_data = qd.get('GOOG/NASDAQ_' + ETF[e], start_date=start_date).to_dict()
        elif asset is 'TLT':
            ETFs_data = qd.get("GOOG/AMEX_" + ETF[e], start_date=start_date).to_dict()
        else:
            ETFs_data = qd.get('GOOG/NYSEARCA_' + ETF[e], start_date=start_date).to_dict()

        dates = sorted(ETFs_data["Close"].keys())
        n = len(dates)
        #date = dates[0].to_datetime().strftime('%Y-%m-%d')
        date = dates[0].to_datetime()
        close =  ETFs_data["Close"][dates[0]]
        volume = ETFs_data["Volume"][dates[0]]
        posts.update_one(
           { '_id': asset },
           { '$set':{'hist_data':[{'date': date,'quotes':{'close': close,'volume': volume} }]}}

        )
        for x in range(1,n):
            #date = dates[x].to_datetime().strftime('%Y-%m-%d')
            date = dates[x].to_datetime()
            close =  ETFs_data["Close"][dates[x]]  # "%.2f" %
            volume = ETFs_data["Volume"][dates[x]]
            histData =  {'$push':{'hist_data':{'date': date,'quotes':{'close': close,'volume': volume} }}}
            posts.update_one({'_id': asset},histData)
    return

def get_hist_data(ticker, host = 'localhost:27017'):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    collection = db.ETF
    cursor = collection.find({"_id": ticker},{"hist_data": 1})
    if cursor.count() == 0:
        print("No "+ ticker + " find")
        return
    else:
        df = json_normalize(list(cursor))
        json_normalize(df.hist_data[0])
        return json_normalize(df.hist_data[0])

def get_hist_data_close(ticker, host):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    collection = db.ETF
    cursor = collection.find({"_id": ticker},{"hist_data.date":1,"hist_data.quotes.close": 1})
    if cursor.count() == 0:
        print("No " + ticker + " find")
        return
    else:
        df = json_normalize(list(cursor))
        df = json_normalize(df.hist_data[0])
        close = list(df['quotes.close'])
        close = pd.DataFrame({ticker: close}, index=df['date'])
        return close


def get_hist_data_close_for_many(ETF, host='155.246.104.19:27017'):
    N = len(ETF)
    df1 = get_hist_data_close(ETF[0], host)
    for e in range(1,N):
        df2 = get_hist_data_close(ETF[e], host)
        df1 = pd.concat([df1, df2], axis=1, join='inner')
    return df1


def get_summary_data(ticker, host='localhost:27017'):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    collection = db.ETF
    cursor = collection.find({"_id": ticker}, {"summary":1})
    if cursor.count() == 0:
        print("No " + ticker + " find")
        return
    else:
        df = json_normalize(list(cursor))
        return df


def get_summary_data_all(host = 'localhost:27017'):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    collection = db.ETF
    cursor = collection.find({},{"summary":1})
    if cursor.count() == 0:
        print("Nothing find")
        return
    else:
        df = json_normalize(list(cursor))
        SUMMARY_DATA = pd.DataFrame({
            'inception_date': list(df["summary.inception_date"]),
            'legal_structure': list(df["summary.legal_structure"]),
            'expense_ratio%': list(df["summary.expense_ratio%"]),
            'assets_under_management_B': list(df["summary.assets_under_management_B"]),
            'average_daily_volume_M': list(df["summary.average_daily_volume_M"]),
            'average_spread%': list(df["summary.average_spread%"]),
            'Max_LT_Capital_Gains_Rate%': list(df["summary.Max_LT_Capital_Gains_Rate%"]),
            'Max_ST_Capital_Gains_Rate%': list(df["summary.Max_ST_Capital_Gains_Rate%"]),
            'date_of_summary': list(df["summary.date_of_summary"]),
            'summary.median_tracking_diff_12m%': list(df["summary.median_tracking_diff_12m%"])

        }, index=df["_id"])
        return SUMMARY_DATA

def get_asset_class(host, ticker=None):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    collection = db.ETF
    cursor = collection.find({}, {"asset_class": 1})
    df = json_normalize(list(cursor))
    df2 = list(df['asset_class'])
    asset_class = pd.DataFrame({"asset_class": df2}, index=df['_id'])
    if ticker == 0:
        return asset_class
    else:
        return asset_class["asset_class"][ticker]





def main():
    ETF24 = ['VTI', 'ITOT', 'SCHB', 'VEA', 'IXUS', 'SCHF', 'VWO', 'IEMG', 'SCHE', 'VIG', 'DVY', 'SCHD', 'VGSH', 'IEF',
             'TLT', 'MUB', 'TFI', 'PZA', 'SCHP', 'TIP', 'IPE', 'XLE', 'DJP', 'VDE']

    asset_class = ["US STOCKS", "US STOCKS", "US STOCKS", "FOREIGN DEVELOPED STOCKS",
                   "FOREIGN DEVELOPED STOCKS", "FOREIGN DEVELOPED STOCKS", "EMERGING MARKET STOCKS",
                   "EMERGING MARKET STOCKS", "EMERGING MARKET STOCKS", "DIVIDEND GROWTH STOCKS",
                   "DIVIDEND GROWTH STOCKS", "DIVIDEND GROWTH STOCKS", "US GOVERNMENT BONDS", "US GOVERNMENT BONDS",
                   "US GOVERNMENT BONDS", "MUNICIPAL BONDS", "MUNICIPAL BONDS", "MUNICIPAL BONDS",
                   "TREASURY INFLATION-PROTECTED SECURITIES (TIPS)", "TREASURY INFLATION-PROTECTED SECURITIES (TIPS)",
                   "TREASURY INFLATION-PROTECTED SECURITIES (TIPS)", "NATURAL RESOURCES", "NATURAL RESOURCES",
                   "NATURAL RESOURCES"]

    host = '155.246.104.19:27017' # use Stevens' mongoDB host
    #host = 'localhost:27017'
    build_ETF(quandlKey = 'e9mjr1zRrH1o_5zBfEEy', host=host) #download the data into database, only use once

    print(get_hist_data("ITOT", host).head())
    print(get_hist_data_close_for_many(ETF =["VTI", "233333", "ITOT"], host = host).head())
    print(get_hist_data_close_for_many(host = host).head())
    print(get_summary_data("VTI", host))
    print(get_asset_class(host=host).head())
    print(get_asset_class(host, "XLE"))

if __name__ == "__main__":
    main()
    print("success!")
