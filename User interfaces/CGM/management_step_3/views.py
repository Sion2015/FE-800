from django.shortcuts import render
from django.utils.safestring import mark_safe
from pymongo import MongoClient
from pandas.io.json import json_normalize

import urllib.request
import codecs
import pandas as pd

import json
# from datetime import datetime
import datetime
from .functions.Black_Litterman import *
from .functions.Portfolio import *
from pymongo import MongoClient
from .functions.Plotly_Charts import *



def management(request):

    host = 'localhost:27017'
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    posts = db.Test
    df = list(posts.find({'_id': "unique"}, {'_id': 0}))
    df = json_normalize(df)
    drift_threshold = df["drift_threshold"][0]
    rebalancing_frequency = df["rebalancing_frequency"][0]

    views = df["views"][0]
    risk_levels = df["risk_levels"][0]



    views = json_normalize(views)


    # Initialize Data
    ETF_tickers = df["my_tickers"][0]  # ETF_tickers = ['VTI', 'VEA', 'VWO', 'VIG', 'XLE', 'SCHP', 'MUB', 'VGSH']
    build_start_date = "2013-01-01"
    build_end_date = "2016-01-04"
    initial_data = Data(ETF_tickers, start_date=build_start_date, end_date=build_end_date, host="localhost:27017")

    # Add "Research Affiliates" views
    index = views.method[views.method == "Research Affiliates"].index.tolist()[0]
    confidence = views.get_value(index, 'confidence')
    Myblacklitterman = BlackLitterman(initial_data, confidence)

    amount = 1000000

    # return_list = []
    # vol_list = []
    # for tau in np.arange(0.0, 2.3, 0.1):
    #     initial_data = Data(ETF_tickers, start_date=build_start_date, end_date=build_end_date, host="localhost:27017")
    #     initial_blacklitterman = BlackLitterman(initial_data,
    #                                             0.8)  # parameter  confidence level of affiliate. same as input
    #     initial_portfolio = Portfolio(initial_data, Myblacklitterman, risk_tolerance=tau, host=initial_data.host,
    #                                   account_deposit=amount,frequency=rebalancing_frequency,#drift_limit=drift_threshold
    #                                   if_backtesting=False)
    #
    #     return_list.append(initial_portfolio.annual_return)
    #     vol_list.append(initial_portfolio.annual_vol)
    #
    # print(return_list)
    # print(vol_list)
    #
    # tau = np.arange(0.0, 2.3, 0.1)
    # plot_line_chart("find_tau", tau, return_list, vol_list)

    context = {

    }

    return render(request, 'management/step_3.html', context)