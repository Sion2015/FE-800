# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 16:54:02 2017

@author: maowanting
"""

from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
from .Data import *
# import pyflux as pf


# from matplotlib import pyplot
# from sklearn.metrics import mean_squared_error
# import matplotlib.pyplot as plt
# from datetime import datetime

def get_arima_views(return_series, risk_free_rate=0.75/100/365):
    # Calculate AIC and get the order

    # series = np.ediff1d(return_series)
    res = sm.tsa.arma_order_select_ic(return_series.values,ic=['aic'], trend='nc')

    p = res.aic_min_order[0]
    q = res.aic_min_order[1]
    try:
        model0_fit = ARIMA(return_series.values, order=(p, 2, q)).fit(method= "MLE", disp=0)
    except ValueError:
        model0_fit = ARIMA(return_series.values, order=(1, 1, 0)).fit(method="MLE", disp=0)
    predictions = model0_fit.forecast()[0] / 22
    view = predictions - risk_free_rate
    return pd.Series(view)


def recalculate_ARIMA(data:Data, type="list"):
    monthly_return = data.returns.resample("M").mean()
    return_matrix = monthly_return.apply(lambda columns: get_arima_views(columns.dropna()), axis=0)
    if type == "list":
        return return_matrix.values.tolist()[0]
    else:
        return return_matrix


def get_Q_matrix(views):
    return np.matrix(views).transpose()


def main():
    ETF_tickers = ['VTI', 'SCHB', 'VEA', 'IXUS', 'IEMG', 'DVY', 'SCHD', 'VGSH',
                   'IEF', 'MUB', 'TFI', 'PZA', 'SCHP', 'DJP', 'VDE']
    initial_data = Data(ETF_tickers, start_date="2013-01-01", end_date="2016-01-04")
    P_matrix = np.diag(np.ones(len(ETF_tickers)))
    Q_matrix = recalculate_ARIMA(initial_data)
    print(type(Q_matrix))
    print(Q_matrix.values.tolist()[0])

if __name__ ==  "__main__":
    main()


# def parser(x):
#     return datetime.strptime('20' + x, '%Y-%m-%d')

# series = read_csv(r'C:\Users\sprin\Dropbox\FE800\Code\price data.csv', header=0, parse_dates=[0], index_col=0,
#                   squeeze=True,
#                   date_parser=parser)
# returns = (series - series.shift(1)) / series.shift(1)
# returns = returns.dropna()

# for column in returns.columns:
#     print("start " + returns[column].name + "\n")
#     X = returns[column].values
#     # fit model
#     model0 = ARIMA(X, order=(5, 1, 0))
#     model0_fit = model0.fit(disp=0)
#     print(model0_fit.summary())
#     size = int(len(X) * 0.66)
#     train = X[0:size]
#     test = X[size:len(X)]
#     history = [x for x in train]
#     predictions = list()
#     for t in range(len(test)):
#         model = ARIMA(history, order=(5, 1, 0))
#         model_fit = model.fit(disp=0)
#         output = model_fit.forecast()
#         yhat = output[0]
#         predictions.append(yhat)
#         obs = test[t]
#         history.append(obs)
#         print('predicted=%f, expected=%f' % (yhat, obs))
#
#
#         # plot
#     # pyplot.figure(figsize=(20, 5))
#     # pyplot.plot(test)
#     # pyplot.plot(predictions, color='red')
#     # pyplot.show()
#     return_diff = (predictions[-1] - risk_free_rate).item()
#     error = mean_squared_error(test, predictions)
#     view.append(return_diff)
#     print(view)
#
# print(view)