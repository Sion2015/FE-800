

import pandas as pd
from pymongo import MongoClient
from pandas.io.json import json_normalize


def drop_parameters(host):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    db.Parameters.drop()


def reset_parameters(host):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    db.Parameters.drop()
    posts = db.Parameters
    ETF8 = ['VTI',  'VEA',  'VWO', 'VIG',  'VGSH', 'MUB', 'SCHP', 'XLE']
    posts.insert_one({
        '_id': "unique",
        'my_tickers': ETF8,
        'views': [
            {'method': "Research Affiliates",
             'confidence': 1.0,
             },
            {'method': "ARIMA",
             'confidence': 0.5,
             }
        ],
        'drift_threshold': 0.02,
        'rebalancing_frequency': "monthly",
        'risk_levels': [0.2, 0.3, 0.4, 0.5, 0.6]
    })
# reset_parameters(host)


def risk_tolerance_mapping(risk_level, host="localhost"):
    client = MongoClient(host=[host])
    db = client.RoboAdvisor
    posts = db.Parameters
    cursor = posts.find(
        {'_id': "unique"},
        {'_id': 0, 'risk_levels':1}
    )
    risk_levels = json_normalize(list(cursor))
    risk_levels = list(risk_levels['risk_levels'])
    risk_levels = list(risk_levels[0])

    if risk_level == 1:
        return risk_levels[0], "Very Conservative"
    elif risk_level == 2:
        return risk_levels[1], "Conservative "
    elif risk_level == 3:
        return risk_levels[2], "Moderate"
    elif risk_level == 4:
        return risk_levels[3], "Aggressive "
    elif risk_level == 5:
        return risk_levels[4], "Very Aggressive"
    else:
        return 99, "Undefined Risk Profile"



def main():
    host = "localhost"
    # reset_parameters(host)

    print(risk_tolerance_mapping(1))
    print(risk_tolerance_mapping(2))
    print(risk_tolerance_mapping(3))
    print(risk_tolerance_mapping(4))
    print(risk_tolerance_mapping(5))


if __name__ == "__main__":
    main()
    print("success!")