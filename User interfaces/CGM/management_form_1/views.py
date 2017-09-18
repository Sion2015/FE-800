from django.shortcuts import render
from django.utils.safestring import mark_safe
from pymongo import MongoClient

from django import forms
from .database.collection_ETF import *



def management(request):
    my_tickers = request.POST.getlist('ETFs')
    # --Connect to MongoDB to get all stock tickers
    # host = '155.246.104.19:27017'
    host = 'localhost:27017'
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    posts = db.Test
    posts.update(
        {'_id': "unique"},
        {'$set': {
            'my_tickers': my_tickers,
        }

        },
        upsert=True
    )


    my_tickers = list(posts.find({'_id': "unique"}, {'_id': 0, 'my_tickers':1}))
    my_tickers = json_normalize(my_tickers)
    my_tickers = list(my_tickers["my_tickers"])
    my_tickers = my_tickers[0]
    asset_type = get_asset_class(host, my_tickers)

    # --Convert stocks list into a string. Then the html will parse the string into json object.
    tickers_choices = ['\"' + e + ', ' + asset_type[e] + '\",' for e in my_tickers]
    tickers_choices = ' '.join(tickers_choices)
    tickers_choices = '['+tickers_choices+']'





    context = {
        'tickers': mark_safe(tickers_choices),


    }

    return render(request, 'parameter1/parameter1.html', context)
