from django.shortcuts import render
from django.utils.safestring import mark_safe
# import urllib.parse
import urllib.request
import codecs
import pandas as pd
from pandas.io.json import json_normalize
import json
# from datetime import datetime
import datetime
from .black_litterman.Black_Litterman import *
from .black_litterman.Portfolio import *
from pymongo import MongoClient
from .interface_functions.Typeform import Typeform
from .interface_functions.Risk_Tolerance_Mapping import risk_tolerance_mapping
from .interface_functions.Plotly_Charts import *




# Create random data with numpy
# import numpy as np

def show_plan(request):
    # Find the corresponding quiz answer -------------------------------------------------------------------------------
    # myEmail = request.POST['email']
    # print(myEmail)
    # typeform = Typeform(myEmail,
    #                     url='https://api.typeform.com/v1/form/L3dqRV?key=86b376b41e8ff574b2fd8a87cbbf7fd374998eac')
    # print(typeform.findMyResponse)
    # print(typeform.amount)
    # print(typeform.risk_tolerance)
    #
    # # Judge if there is a corresponding quiz answer and return different values to template
    # if typeform.findMyResponse == False:
    #     display1 = " "
    #     display2 = "w3-hide"
    #     txt1 = "We cannot find your information in our database. Please do the questionnaire first or check the " \
    #            "spelling of your email address."
    # else:
    #     display1 = "w3-hide"
    #     display2 = " "
    #     txt1 = "Your plan is ready!"


    txt1 = "Your plan is ready!"



    # Get parameters from MongoBD
    host = 'localhost:27017'
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    posts = db.Parameters
    df = list(posts.find({'_id': "unique"}, {'_id': 0}))
    df = json_normalize(df)
    # drift_threshold = df["drift_threshold"][0] #  Unused
    # rebalancing_frequency = df["rebalancing_frequency"][0]  #  Unused
    views = df["views"][0]
    views = json_normalize(views)
    drift_threshold = df["drift_threshold"][0]
    rebalancing_frequency = df["rebalancing_frequency"][0]
    tau = df["risk_levels"]

    # Initialize Data
    ETF_tickers = df["my_tickers"][0]  # ETF_tickers = ['VTI', 'VEA', 'VWO', 'VIG', 'XLE', 'SCHP', 'MUB', 'VGSH']
    build_start_date = "2013-01-01"
    build_end_date = "2016-01-04"
    initial_data = Data(ETF_tickers, start_date=build_start_date, end_date=build_end_date, host="localhost:27017")

    # Add views
    # if ("Research Affiliates" in list(views["method"])):
    #     index = views.method[views.method == "Research Affiliates"].index.tolist()[0]
    #     confidence = views.get_value(index, 'confidence')
    #     print("confidence", confidence)
    #     Myblacklitterman = BlackLitterman(initial_data, confidence)

    # Add "Research Affiliates" views
    index = views.method[views.method == "Research Affiliates"].index.tolist()[0]
    confidence = views.get_value(index, 'confidence')
    Myblacklitterman = BlackLitterman(initial_data, confidence)

    # if ("ARIMA" in list(views["method"])):
    #     index = views.method[views.method == "ARIMA"].index.tolist()[0]
    #     confidence = views.get_value(index, 'confidence')
    #     print("confidence", confidence)
    #     Myblacklitterman.add_arima(confidence)  # Unsecured

    if ("other" in list(views["method"])):
        index = views.method[views.method == "ARIMA"].index.tolist()[0]
        confidence = views.get_value(index, 'confidence')
        Myblacklitterman.add_arima(confidence)  # Unsecured

    # Risk_tolerance mapping
    #risk_level = typeform.risk_tolerance
    #tau, risk_tolerance = risk_tolerance_mapping(risk_level)
    print("request.POST.get('risk_level',6), ", request.POST.get('risk_level',6))
    risk_level = request.POST.get('risk_level', "3/")
    risk_level = int(risk_level.strip("/"))
    print("risk_level", risk_level)




    amount = 100000

    #Portfolio construction and backtesting
    # initial_portfolio1 = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=tau[0],
    #     host=initial_data.host,
    #     account_deposit=amount
    #     # frequency=rebalancing_frequency,
    #     # drift_limit=drift_threshold
    # )
    #
    # initial_portfolio2 = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=tau[1],
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     drift_limit=drift_threshold
    # )
    # initial_portfolio3 = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=tau[2],
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     drift_limit=drift_threshold
    # )
    # initial_portfolio4 = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=tau[3],
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     drift_limit=drift_threshold
    # )
    # initial_portfolio5 = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=tau[4],
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     drift_limit=drift_threshold
    # )
    # initial_benchmark = Portfolio(
    #     initial_data,
    #     Myblacklitterman,
    #     risk_tolerance=tau[4],
    #     host=initial_data.host,
    #     account_deposit=amount,
    #     frequency=rebalancing_frequency,
    #     drift_limit=drift_threshold,
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
    # # print(initial_portfolio.rebalance_times)
    # # print(initial_portfolio.target_weights)
    # # print(initial_benchmark.rebalance_times)
    # # print(initial_benchmark.target_weights)
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
        #"email": mark_safe(myEmail),
        "amount": amount,#typeform.amount,
        #"risk_tolerance": risk_tolerance,
        "risk_level": risk_level,
        "txt1": txt1,
    }

    return render(request, 'show_plan/show_plan.html', context)
