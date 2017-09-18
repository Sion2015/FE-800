from django.shortcuts import render
from django.utils.safestring import mark_safe
from pymongo import MongoClient

from django import forms
from .database.collection_ETF import *


def reset_parameters(host):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    db.Parameters.drop()
    posts = db.Parameters
    ETF8 = ['VTI',  'VEA',  'VWO', 'VIG',  'VGSH', 'MUB', 'SCHP', 'XLE']
    posts.insert_one({
        '_id': "unique",
        'my_tickers': ETF8,
        'views': ['Research Affiliates'],
        'drift_threshold': 0.02,
        'rebalancing_frequency': "monthly"
    })
# reset_parameters(host)

def confirmation(request):

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




    context = {
        'my_tickers': my_tickers,
        'views': views,
        'drift_threshold': drift_threshold*100,
        'rebalancing_frequency': rebalancing_frequency,

    }

    return render(request, 'confirmation/confirmation.html', context)
