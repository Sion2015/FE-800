from django.shortcuts import render
from django.utils.safestring import mark_safe
from pymongo import MongoClient

from django import forms
from .database.collection_ETF import *



def management(request):
    rebalancing_frequency = request.POST['rebalancing_frequency']
    drift_threshold = float(request.POST['drift_threshold'])/100
    # --Connect to MongoDB to get all stock tickers
    # host = '155.246.104.19:27017'
    host = 'localhost:27017'
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    posts = db.Test
    posts.update(
        {'_id': "unique"},
        {'$set': {
            'drift_threshold': drift_threshold,
            'rebalancing_frequency': mark_safe(rebalancing_frequency),
        }

        },
        upsert=True
    )



    df = list(posts.find({'_id': "unique"}, {'_id': 0, 'drift_threshold':1, 'rebalancing_frequency':1}))
    df = json_normalize(df)
    drift_threshold = df["drift_threshold"][0]
    rebalancing_frequency = df["rebalancing_frequency"][0]







    context = {
        'drift_threshold': drift_threshold*100,
        'rebalancing_frequency': rebalancing_frequency,

    }

    return render(request, 'parameter2/parameter2.html', context)
