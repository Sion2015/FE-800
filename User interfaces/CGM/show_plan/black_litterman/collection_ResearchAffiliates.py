
# coding: utf-8

# In[10]:

import pandas as pd
from pymongo import MongoClient
from .data_preprocessing import *

# In[12]:
host = 'localhost:27017'
ETF_tickers = ['VTI', 'VEA', 'VWO', 'VIG', 'XLE', 'SCHP', 'MUB']
csv_name = "core_asset_class_expected_returns.csv"


# In[73]:

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



# In[74]:

def get_RA_exp_rtn(host=host, asset_class=asset_class):
    client = MongoClient(host)
    db = client.RoboAdvisor
    request = db.ResearchAffiliates
    cursor = request.find({"_id": asset_class },{ "_id":0, "views.exp_rtn%": 1})
    exp_rtn = json_normalize(list(cursor))["views.exp_rtn%"]
    return exp_rtn[0]


# In[75]:

def get_RA_views(host=host, ETF=ETF_tickers):
    # Define the mapping
    asset_class_dic = {
        "US STOCKS": "US Large",
        "FOREIGN DEVELOPED STOCKS": "Global Core", # Not sure
        "EMERGING MARKET STOCKS": "EM Equity",
        "DIVIDEND GROWTH STOCKS": "US Large", # Whatever
        "US GOVERNMENT BONDS": "US Large", # Whatever
        "MUNICIPAL BONDS": "US Large", # Whatever
        "TREASURY INFLATION-PROTECTED SECURITIES (TIPS)": "US Tips",  
        "NATURAL RESOURCES": "US Large",# Whatever
    }
    N = len(ETF)
    RA_views = [0]*N
    for i in range(N):
        asset_class = get_asset_class(host=host, ticker=ETF[i])
        asset_class = asset_class_dic[asset_class]
        RA_views[i] = get_RA_exp_rtn(host=host, asset_class=asset_class)
    return RA_views


def main():
    # build_collection_ResearchAffiliates(host=host, ETF=ETF_tickers, csv_name=csv_name)
    print(get_RA_views(host=host, ETF=ETF_tickers))

if __name__ == "__main__":
    main()
    pass
