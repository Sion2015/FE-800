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



def review(request):

    # --Connect to MongoDB to get all stock tickers
    # host = '155.246.104.19:27017'
    host = 'localhost:27017'
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    posts = db.Test
    df = list(posts.find({'_id': "unique"}, {'_id': 0}))
    df = json_normalize(df)
    drift_threshold = df["drift_threshold"][0]
    rebalancing_frequency = df["rebalancing_frequency"][0]
    my_tickers = df["my_tickers"][0]
    views1 = df["views"][0]
    risk_levels = df["risk_levels"][0]



    views = json_normalize(views1)


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
    #Portfolio construction and backtesting
    initial_portfolio1 = Portfolio(
        initial_data,
        Myblacklitterman,
        risk_tolerance=risk_levels[0],
        host=initial_data.host,
        account_deposit=amount,
        frequency=rebalancing_frequency,
        #drift_limit=drift_threshold
    )

    initial_portfolio2 = Portfolio(
        initial_data,
        Myblacklitterman,
        risk_tolerance=risk_levels[1],
        host=initial_data.host,
        account_deposit=amount,
        frequency=rebalancing_frequency,
        #drift_limit=drift_threshold
    )
    initial_portfolio3 = Portfolio(
        initial_data,
        Myblacklitterman,
        risk_tolerance=risk_levels[2],
        host=initial_data.host,
        account_deposit=amount,
        frequency=rebalancing_frequency,
        #drift_limit=drift_threshold
    )
    initial_portfolio4 = Portfolio(
        initial_data,
        Myblacklitterman,
        risk_tolerance=risk_levels[3],
        host=initial_data.host,
        account_deposit=amount,
        frequency=rebalancing_frequency,
        #drift_limit=drift_threshold
    )
    initial_portfolio5 = Portfolio(
        initial_data,
        Myblacklitterman,
        risk_tolerance=risk_levels[4],
        host=initial_data.host,
        account_deposit=amount,
        frequency=rebalancing_frequency,
        #drift_limit=drift_threshold
    )
    initial_benchmark = Portfolio(
        initial_data,
        Myblacklitterman,
        risk_tolerance=0,
        host=initial_data.host,
        account_deposit=amount,
        frequency=rebalancing_frequency,
        #drift_limit=drift_threshold,
        if_benchmark=True
    )



    # Prepare the data for plot
    result1 = initial_portfolio1.back_testing_result
    result2 = initial_portfolio2.back_testing_result
    result3 = initial_portfolio3.back_testing_result
    result4 = initial_portfolio4.back_testing_result
    result5 = initial_portfolio5.back_testing_result
    result_b = initial_benchmark.back_testing_result

    N = result1.shape[1]
    weights1 = list(result1.iloc[-1])
    weights1 = weights1[0:(N - 3)]
    weights2 = list(result2.iloc[-1])
    weights2 = weights2[0:(N - 3)]
    weights3 = list(result3.iloc[-1])
    weights3 = weights3[0:(N - 3)]
    weights4 = list(result4.iloc[-1])
    weights4 = weights4[0:(N - 3)]
    weights5 = list(result5.iloc[-1])
    weights5 = weights5[0:(N - 3)]

    # print(initial_portfolio.rebalance_times)
    # print(initial_portfolio.target_weights)
    # print(initial_benchmark.rebalance_times)
    # print(initial_benchmark.target_weights)

    daily_total_value1 = result1['daily_total_value']
    daily_total_value2 = result2['daily_total_value']
    daily_total_value3 = result3['daily_total_value']
    daily_total_value4 = result4['daily_total_value']
    daily_total_value5 = result5['daily_total_value']

    benchmark = result_b['daily_total_value']
    dates = result1.index.tolist()
    asset_class = get_asset_class(host, ETF_tickers)

    #Plotly
    # plot_line_chart("line_all", dates, daily_total_value1, daily_total_value2, daily_total_value3, daily_total_value4,
    #                 daily_total_value5, benchmark, risk_levels)
    # plot_pie_chart("pie_all", weights1,weights2, weights3, weights4,weights5, asset_class, ETF_tickers, risk_levels)
    #









    context = {
        'my_tickers': my_tickers,
        'views': views1,
        'drift_threshold': drift_threshold*100,
        'rebalancing_frequency': rebalancing_frequency,
        'risk_levels': risk_levels,

        'annual_return_1': "{:.4f}".format(initial_portfolio1.annual_return),
        'annual_vol_1': "{:.4f}".format(initial_portfolio1.annual_vol),
        'sharpe_ratio_1': "{:.3f}".format(initial_portfolio1.sharpe_ratio),
        'max_drawdown_1': "{:.3f}".format(initial_portfolio1.max_drawdown),
        'VaR_1': "{:.3f}".format(initial_portfolio1.VaR),
        'sortino_ratio_1': "{:.3f}".format(initial_portfolio1.sortino_ratio),

        'annual_return_2': "{:.4f}".format(initial_portfolio2.annual_return),
        'annual_vol_2': "{:.4f}".format(initial_portfolio2.annual_vol),
        'sharpe_ratio_2': "{:.3f}".format(initial_portfolio2.sharpe_ratio),
        'max_drawdown_2': "{:.3f}".format(initial_portfolio2.max_drawdown),
        'VaR_2': "{:.3f}".format(initial_portfolio2.VaR),
        'sortino_ratio_2': "{:.3f}".format(initial_portfolio2.sortino_ratio),

        'annual_return_3': "{:.4f}".format(initial_portfolio3.annual_return),
        'annual_vol_3': "{:.4f}".format(initial_portfolio3.annual_vol),
        'sharpe_ratio_3': "{:.3f}".format(initial_portfolio3.sharpe_ratio),
        'max_drawdown_3': "{:.3f}".format(initial_portfolio3.max_drawdown),
        'VaR_3': "{:.3f}".format(initial_portfolio3.VaR),
        'sortino_ratio_3': "{:.3f}".format(initial_portfolio3.sortino_ratio),

        'annual_return_4': "{:.4f}".format(initial_portfolio4.annual_return),
        'annual_vol_4': "{:.4f}".format(initial_portfolio4.annual_vol),
        'sharpe_ratio_4': "{:.3f}".format(initial_portfolio4.sharpe_ratio),
        'max_drawdown_4': "{:.3f}".format(initial_portfolio4.max_drawdown),
        'VaR_4': "{:.3f}".format(initial_portfolio4.VaR),
        'sortino_ratio_4': "{:.3f}".format(initial_portfolio4.sortino_ratio),

        'annual_return_5': "{:.4f}".format(initial_portfolio5.annual_return),
        'annual_vol_5': "{:.4f}".format(initial_portfolio5.annual_vol),
        'sharpe_ratio_5': "{:.3f}".format(initial_portfolio5.sharpe_ratio),
        'max_drawdown_5': "{:.3f}".format(initial_portfolio5.max_drawdown),
        'VaR_5': "{:.3f}".format(initial_portfolio5.VaR),
        'sortino_ratio_5': "{:.3f}".format(initial_portfolio5.sortino_ratio),

        'annual_return_b': "{:.4f}".format(initial_benchmark.annual_return),
        'annual_vol_b': "{:.4f}".format(initial_benchmark.annual_vol),
        'sharpe_ratio_b': "{:.3f}".format(initial_benchmark.sharpe_ratio),
        'max_drawdown_b': "{:.3f}".format(initial_benchmark.max_drawdown),
        'VaR_b': "{:.3f}".format(initial_benchmark.VaR),
        'sortino_ratio_b': "{:.3f}".format(initial_benchmark.sortino_ratio)

    }

    return render(request, 'management/step_5.html', context)