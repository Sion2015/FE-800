from django.shortcuts import render
from django.utils.safestring import mark_safe
from pymongo import MongoClient

from django import forms
from .database.collection_ETF import *


def management(request):
    views = request.POST.getlist('views')
    # --Connect to MongoDB to get all stock tickers
    # host = '155.246.104.19:27017'
    print(views)
    host = 'localhost:27017'

    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    posts = db.Test
    posts.update(
        {'_id': "unique"},
        {'$set': {
            'views': []
        }
        },
        upsert=True
    )

    if ("Research Affiliates" in views):
        posts.update(
            {'_id': "unique"},
            {'$push': {
                'views': {
                    'method': "Research Affiliates",
                    'confidence': int(request.POST['RA_confidence'])/100
                }
            }
            },
            upsert=True
        )
    if ("ARIMA" in views):
        posts.update(
            {'_id': "unique"},
            {'$push': {
                'views': {
                    'method': "ARIMA",
                    'confidence': int(request.POST['ARIMA_confidence'])/100
                }
            }
            },
            upsert=True
        )
    if ("other" in views):
        posts.update(
            {'_id': "unique"},
            {'$push': {
                'views': {
                    'method': "other",
                    'confidence': float(request.POST('other_confidence'))
                }
            }
            },
            upsert=True
        )





    context = {
        'views': list(posts.find({'_id': "unique"}, {'_id': 0, 'views': 1}))


    }

    return render(request, 'parameter4/parameter4.html', context)
