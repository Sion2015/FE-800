from django.shortcuts import render
from django.utils.safestring import mark_safe
from pymongo import MongoClient

from django import forms
from .database.collection_ETF import *




def management(request):
    risk_levels = []
    risk_levels.append(float(request.POST['tau1']))
    risk_levels.append(float(request.POST['tau2']))
    risk_levels.append(float(request.POST['tau3']))
    risk_levels.append(float(request.POST['tau4']))
    risk_levels.append(float(request.POST['tau5']))


    # --Connect to MongoDB to get all stock tickers
    # host = '155.246.104.19:27017'
    host = 'localhost:27017'
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    posts = db.Test
    posts.update(
        {'_id': "unique"},
        {'$set': {
            'risk_levels': risk_levels,

        }

        },
        upsert=True
    )


    df = list(posts.find({'_id': "unique"}, {'_id': 0, 'risk_levels':1}))
    df = json_normalize(df)
    risk_levels = df["risk_levels"][0]


    context = {
        'risk_levels': risk_levels

    }

    return render(request, 'parameter3/parameter3.html', context)
