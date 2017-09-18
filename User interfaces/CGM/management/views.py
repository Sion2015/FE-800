from django.shortcuts import render
from django.utils.safestring import mark_safe
from pymongo import MongoClient
from .database.collection_ETF import *



def current(request):

    # --Connect to MongoDB to get all stock tickers
    # host = '155.246.104.19:27017'
    host = 'localhost:27017'
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    posts = db.Parameters


    df = list(posts.find({'_id': "unique"}, {'_id': 0}))
    df = json_normalize(df)


    drift_threshold = df["drift_threshold"][0]
    rebalancing_frequency = df["rebalancing_frequency"][0]

    my_tickers = df["my_tickers"][0]
    views = df["views"][0]
    risk_levels = df["risk_levels"][0]




    context = {
        'my_tickers': my_tickers,
        'views': views,
        'drift_threshold': drift_threshold*100,
        'rebalancing_frequency': rebalancing_frequency,
        'risk_levels': risk_levels,

    }

    return render(request, 'management/home.html', context)