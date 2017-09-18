from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import pyflux as pf
from datetime import datetime
import matplotlib.pyplot as plt


def parser(x):
    return datetime.strptime('20' + x, '%Y-%m-%d')


series = read_csv(r'C:\Users\sprin\Dropbox\FE800\Code\data.csv', header=0, parse_dates=[0], index_col=0, squeeze=True,
                  date_parser=parser)
returns = (series - series.shift(1)) / series.shift(1)
returns = returns.dropna()
series = series.dropna()

view = []
for column in returns.columns[2:3]:

    X = returns[column].values

    size = int(len(X) * 0.66)
    train = X[0:size]
    test = X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(5, 1, 0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)

        print('predicted=%f, expected=%f' % (yhat, obs))
    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)

    # plot
    pyplot.plot(figsize=(20, 5))
    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.show()