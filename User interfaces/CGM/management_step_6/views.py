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
from .functions.Plotly_Charts_1 import *




def management(request):

    # --Connect to MongoDB to get all stock tickers
    # host = '155.246.104.19:27017'
    host = 'localhost:27017'
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    requests = db.Test
    df = list(requests.find({'_id': "unique"}, {'_id': 0}))
    df = json_normalize(df)
    drift_threshold = df["drift_threshold"][0]
    rebalancing_frequency = df["rebalancing_frequency"][0]
    my_tickers = df["my_tickers"][0]
    views = df["views"][0]
    risk_levels = df["risk_levels"][0]



    #db.Parameter.drop()
    posts = db.Parameters




    posts.update(
        {'_id': "unique"},
        {'$set': {
            'my_tickers': my_tickers,
            'views':  views,
            'drift_threshold': drift_threshold,
            'rebalancing_frequency': rebalancing_frequency,
            'risk_levels': risk_levels,
        }

        },
        upsert=True
    )

    requests = db.Parameters
    df = list(requests.find({'_id': "unique"}, {'_id': 0}))
    df = json_normalize(df)
    drift_threshold = df["drift_threshold"][0]
    rebalancing_frequency = df["rebalancing_frequency"][0]
    my_tickers = df["my_tickers"][0]
    views1 = df["views"][0]
    risk_levels = df["risk_levels"][0]


    # # Initialize Data
    # views = json_normalize(views1)
    # ETF_tickers = df["my_tickers"][0]  # ETF_tickers = ['VTI', 'VEA', 'VWO', 'VIG', 'XLE', 'SCHP', 'MUB', 'VGSH']
    # build_start_date = "2013-01-01"
    # build_end_date = "2016-01-04"
    # initial_data = Data(ETF_tickers, start_date=build_start_date, end_date=build_end_date, host="localhost:27017")
    #
    # # Add "Research Affiliates" views
    # index = views.method[views.method == "Research Affiliates"].index.tolist()[0]
    # confidence = views.get_value(index, 'confidence')
    # Myblacklitterman = BlackLitterman(initial_data, confidence)
    #
    # amount = 100000
    # #Portfolio construction and backtesting
    # initial_portfolio1 = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=risk_levels[0],
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     #drift_limit=drift_threshold
    # )
    #
    # initial_portfolio2 = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=risk_levels[1],
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     #drift_limit=drift_threshold
    # )
    # initial_portfolio3 = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=risk_levels[2],
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     #drift_limit=drift_threshold
    # )
    # initial_portfolio4 = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=risk_levels[3],
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     #drift_limit=drift_threshold
    # )
    # initial_portfolio5 = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=risk_levels[4],
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     #drift_limit=drift_threshold
    # )
    # initial_benchmark = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=0,
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     #drift_limit=drift_threshold,
    #     if_benchmark=True
    # )
    #
    #
    #
    # # Prepare the data for plot
    # result1 = initial_portfolio1.back_testing_result
    # result2 = initial_portfolio2.back_testing_result
    # result3 = initial_portfolio3.back_testing_result
    # result4 = initial_portfolio4.back_testing_result
    # result5 = initial_portfolio5.back_testing_result
    # result_b = initial_benchmark.back_testing_result
    #
    # N = result1.shape[1]
    # weights1 = list(result1.iloc[-1])
    # weights1 = weights1[0:(N - 3)]
    # weights2 = list(result2.iloc[-1])
    # weights2 = weights2[0:(N - 3)]
    # weights3 = list(result3.iloc[-1])
    # weights3 = weights3[0:(N - 3)]
    # weights4 = list(result4.iloc[-1])
    # weights4 = weights4[0:(N - 3)]
    # weights5 = list(result5.iloc[-1])
    # weights5 = weights5[0:(N - 3)]
    #
    #
    # daily_total_value1 = result1['daily_total_value']
    # daily_total_value2 = result2['daily_total_value']
    # daily_total_value3 = result3['daily_total_value']
    # daily_total_value4 = result4['daily_total_value']
    # daily_total_value5 = result5['daily_total_value']
    #
    # benchmark = result_b['daily_total_value']
    # dates = result1.index.tolist()
    # asset_class = get_asset_class(host, ETF_tickers)
    #
    #
    #
    # # Plotly
    # plot_line_chart("line_1", dates, daily_total_value1, benchmark)
    # plot_pie_chart("pie_1", weights1, asset_class, ETF_tickers)
    # plot_line_chart("line_2", dates, daily_total_value2, benchmark)
    # plot_pie_chart("pie_2", weights2, asset_class, ETF_tickers)
    # plot_line_chart("line_3", dates, daily_total_value3, benchmark)
    # plot_pie_chart("pie_3", weights3, asset_class, ETF_tickers)
    # plot_line_chart("line_4", dates, daily_total_value4, benchmark)
    # plot_pie_chart("pie_4", weights4, asset_class, ETF_tickers)
    # plot_line_chart("line_5", dates, daily_total_value5, benchmark)
    # plot_pie_chart("pie_5", weights5, asset_class, ETF_tickers)




    context = {
        'my_tickers': my_tickers,
        'views': views1,
        'drift_threshold': drift_threshold*100,
        'rebalancing_frequency': rebalancing_frequency,
        'risk_levels': risk_levels,

    }

    return render(request, 'management/step_6.html', context)