import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


#import numpy as np

# Plot the result --------------------------------------------------------------------------------------------------

#plotly.tools.set_credentials_file(username='afteradam', api_key='4B0cCLHHbHpwkGasGD5E')
plotly.tools.set_credentials_file(username='sion2015', api_key='krjGmvbNSXGWGrX23As9')


def plot_line_chart(plotname, dates, daily_total_value1, daily_total_value2, daily_total_value3, daily_total_value4,
                    daily_total_value5, benchmark, risk_levels):

    trace0 = go.Scatter(
        x=dates,
        y=list(benchmark),
        name="Equally Weighted Portfolio",
        visible=False,
    )
    trace1 = go.Scatter(
        x=dates,
        y=list(daily_total_value1),
        name="tau="+str(risk_levels[0]),
        # visible=False,
    )
    trace2 = go.Scatter(
        x=dates,
        y=list(daily_total_value2),
        name="tau=" + str(risk_levels[1]),

    )

    trace3 = go.Scatter(
        x=dates,
        y=list(daily_total_value3),
        name="tau=" + str(risk_levels[2]),

    )

    trace4 = go.Scatter(
        x=dates,
        y=list(daily_total_value4),
        name="tau=" + str(risk_levels[3]),

    )
    trace5 = go.Scatter(
        x=dates,
        y=list(daily_total_value5),
        name="tau=" + str(risk_levels[4]),

    )

    data = [trace0, trace1, trace2, trace3, trace4, trace5]
    layout = go.Layout(
        title='Historical Performance',
        autosize=False,
        width=1200,
        height=500,
        updatemenus=list([
            dict(
                x=1.20,
                #xanchor='left',
                y=1.11,
                yanchor='top',
                buttons=list([

                    dict(

                        label='CGM Portfolios',
                        method='restyle',
                        args=['visible', [False, True, True, True, True, True]],
                    ),

                    dict(
                        label='Compare',
                        method='restyle',
                        args=['visible', [True, True, True, True, True, True]],
                    ),
                ]),
            )
        ]),
    )
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename=plotname, auto_open=False)
    return


def plot_pie_chart(plotname, weights1,weights2, weights3, weights4,weights5, asset_class, ETF_tickers, risk_levels):
    fig = {
        "data": [
            {
                "values": weights1,
                "labels": asset_class,
                "domain": {"x": [0, 0.2]},
                "name": "Asset Allocation",
                "text": ETF_tickers,
                "hoverinfo": "label+text+percent",
                #"textinfo": "label+percent",
                'textinfo': 'none',
                "hole": 0.5,
                "type": "pie"
            },
            {
                "values": weights2,
                "labels": asset_class,
                "domain": {"x": [0.2, 0.4]},
                "name": "Asset Allocation",
                "text": ETF_tickers,
                "hoverinfo": "label+text+percent",
                # "textinfo": "label+percent",
                'textinfo': 'none',
                "hole": 0.5,
                "type": "pie"
            },

            {
                "values": weights3,
                "labels": asset_class,
                "domain": {"x": [0.4, 0.6]},
                "name": "Asset Allocation",
                "text": ETF_tickers,
                "hoverinfo": "label+text+percent",
                # "textinfo": "label+percent",
                'textinfo': 'none',
                "hole": 0.5,
                "type": "pie"
            },

            {
                "values": weights4,
                "labels": asset_class,
                "domain": {"x": [0.6, 0.8]},
                "name": "Asset Allocation",
                "text": ETF_tickers,
                "hoverinfo": "label+text+percent",
                # "textinfo": "label+percent",
                'textinfo': 'none',
                "hole": 0.5,
                "type": "pie"
            },
            {
                "values": weights5,
                "labels": asset_class,
                "domain": {"x": [0.8, 1]},
                "name": "Asset Allocation",
                "text": ETF_tickers,
                "hoverinfo": "label+text+percent",
                # "textinfo": "label+percent",
                'textinfo': 'none',
                "hole": 0.5,
                "type": "pie"
            }

        ],
        "layout": {
            "title":"Asset Allocation",
            "autosize": False,
            "width": 1200,
            "height": 300,
            'showlegend': False,
            "annotations": [
                {
                    "font": {
                        "size": 10
                    },
                    "showarrow": False,
                    "text": "tau="+str(risk_levels[0]),
                    "x": 0.08,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 10
                    },
                    "showarrow": False,
                    "text": "tau=" + str(risk_levels[1]),
                    "x": 0.29,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 10
                    },
                    "showarrow": False,
                    "text": "tau=" + str(risk_levels[2]),
                    "x": 0.5,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 10
                    },
                    "showarrow": False,
                    "text": "tau=" + str(risk_levels[3]),
                    "x": 0.71,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 10
                    },
                    "showarrow": False,
                    "text": "tau=" + str(risk_levels[4]),
                    "x": 0.92,
                    "y": 0.5
                },
            ]
        }
    }
    py.plot(fig, filename=plotname, auto_open=False)
    return
