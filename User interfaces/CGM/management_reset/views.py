from django.shortcuts import render
from django.utils.safestring import mark_safe
from pymongo import MongoClient

from django import forms
from .database.collection_ETF import *


def reset_parameters(host):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    db.Test.drop()
    posts = db.Test
    ETF8 = ['VTI',  'VEA',  'VWO', 'VIG',  'VGSH', 'MUB', 'SCHP', 'XLE']
    posts.insert_one({
        '_id': "unique",
        'my_tickers': ETF8,
        'views':  [{'method': 'Research Affiliates', 'confidence': 1.0}],
        'drift_threshold': 0.02,
        'rebalancing_frequency': "monthly",
        'risk_levels': [0.25, 0.5, 0.75, 1, 1.25],
    })


def management(request):

    # --Connect to MongoDB to get all stock tickers
    # host = '155.246.104.19:27017'
    host = 'localhost:27017'
    reset_parameters(host)
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    posts = db.Test


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

    return render(request, 'reset/reset.html', context)
