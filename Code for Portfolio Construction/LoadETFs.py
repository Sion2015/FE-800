# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
import quandl as qd
from pymongo import MongoClient

def LoadETFs():
    client = MongoClient()
    db = client.robo_advisor
    
    
    qd.ApiConfig.api_key = 'e9mjr1zRrH1o_5zBfEEy' # Yun's key = yJRsZwcETsegkLY-PThM
    
    ETFs = {'VTI':"US STOCKS",'ITOT':"US STOCKS",'SCHB':"US STOCKS",'VEA':"FOREIGN \
    DEVELOPED STOCKS",'IXUS':"FOREIGN DEVELOPED STOCKS",'SCHF':"FOREIGN DEVELOPED STOCKS",
    'VWO':"EMERGING MARKET STOCKS",'IEMG':"EMERGING MARKET STOCKS",'SCHE':"EMERGING MARKET\
    STOCKS",'VIG':"DIVIDEND GROWTH STOCKS",'DVY':"DIVIDEND GROWTH STOCKS",'SCHD':"DIVIDEND\
    GROWTH STOCKS",'VGSH':"US GOVERNMENT BONDS",'IEF':"US GOVERNMENT BONDS",'TLT':"US\
    GOVERNMENT BONDS",'MUB':"MUNICIPAL BONDS",'TFI':"MUNICIPAL BONDS",'PZA':"MUNICIPAL \
    BONDS",'SCHP':"TREASURY INFLATION-PROTECTED SECURITIES (TIPS)",'TIP':"TREASURY \
    INFLATION-PROTECTED SECURITIES (TIPS)",'IPE':"TREASURY INFLATION-PROTECTED SECUR\
    ITIES (TIPS)",'XLE':"NATURAL RESOURCES",'DJP':"NATURAL RESOURCES",
    'VDE':"NATURAL RESOURCES"}

    capital = {'VTI':"US STOCKS",'ITOT':"US STOCKS",'SCHB':"US STOCKS",'VEA':"FOREIGN \
    DEVELOPED STOCKS",'IXUS':"FOREIGN DEVELOPED STOCKS",'SCHF':"FOREIGN DEVELOPED STOCKS",
    'VWO':"EMERGING MARKET STOCKS",'IEMG':"EMERGING MARKET STOCKS",'SCHE':"EMERGING MARKET\
    STOCKS",'VIG':"DIVIDEND GROWTH STOCKS",'DVY':"DIVIDEND GROWTH STOCKS",'SCHD':"DIVIDEND\
    GROWTH STOCKS",'VGSH':"US GOVERNMENT BONDS",'IEF':"US GOVERNMENT BONDS",'TLT':"US\
    GOVERNMENT BONDS",'MUB':"MUNICIPAL BONDS",'TFI':"MUNICIPAL BONDS",'PZA':"MUNICIPAL \
    BONDS",'SCHP':"TREASURY INFLATION-PROTECTED SECURITIES (TIPS)",'TIP':"TREASURY \
    INFLATION-PROTECTED SECURITIES (TIPS)",'IPE':"TREASURY INFLATION-PROTECTED SECUR\
    ITIES (TIPS)",'XLE':"NATURAL RESOURCES",'DJP':"NATURAL RESOURCES",
    'VDE':"NATURAL RESOURCES"}


    db.ETF.delete_many({})
    db.histricaldata.delete_many({})
    
    apiCall = 1
    for k in ETFs.keys(): # dictionary
        print(ETFs[k])

        if apiCall % 20 == 0:
            print("Sleeping for 10 min every 20 calls")
            time.sleep(11*60) #sleep 10 min if 20 calls have been made

        # qd.ApiConfig.api_key = 'e9mjr1zRrH1o_5zBfEEy'

        apiCall = apiCall+1
        print(k + " is start!")
        ETFs_data = None
        if k is not 'VGSH': # VGSH is in NASDAQ
            ETFs_data = qd.get('GOOG/NYSEARCA_' + k, start_date="2010-01-01").to_dict()
        else:
            ETFs_data = qd.get('GOOG/NASDAQ_' + k, start_date="2010-01-01").to_dict()
        ETFs_ticker = {"ticker" : k, "asset class" : ETFs[k]}

       # print("ETF data " + ETFs_ticker['name'])
        ETF = db.ETF
        ETF.insert_one(ETFs_ticker).inserted_id
        #print('id' + (ETF_id))
        a = sorted(ETFs_data["Close"].keys())
        for x in a:
            b = x.to_datetime().strftime('%Y-%m-%d')
            post = {
                "ticker":db.ETF.find_one({"ticker":k})["_id"],
                "Date":b,
                "Close":("%.2f" % ETFs_data["Close"][x]),
                "Volume":ETFs_data["Volume"][x]}
            historical_data = db.histrical_data
            historical_data.insert_one(post).inserted_id
        print(k + "is end")

LoadETFs()