import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


#import numpy as np

# Plot the result --------------------------------------------------------------------------------------------------

#plotly.tools.set_credentials_file(username='yunchen', api_key='zHwFGN63xYvdQGnmNiYT')
plotly.tools.set_credentials_file(username='sion2015', api_key='krjGmvbNSXGWGrX23As9')

def plot_line_chart(plotname, dates, daily_total_value, benchmark):
    trace1 = go.Scatter(
        x=dates,
        y=list(daily_total_value),
        name="CGM Portfolio",
        # visible=False,
    )
    trace2 = go.Scatter(
        x=dates,
        y=list(benchmark),
        name="Equally Weighted Portfolio",
        visible=False,
    )
    data = [trace1, trace2]
    layout = go.Layout(
        title='Historical Performance',
        updatemenus=list([
            dict(
                x=1.20,
                #xanchor='left',
                y=1.11,
                yanchor='top',
                buttons=list([

                    dict(

                        label='CGM Portfolio',
                        method='restyle',
                        args=['visible', [True, False]],
                    ),
                    dict(

                        label='Equally Weighted Portfolio',
                        method='restyle',
                        args=['visible', [False, True]],
                    ),
                    dict(
                        label='Compare',
                        method='restyle',
                        args=['visible', [True, True]],
                    ),
                ]),
            )
        ]),
    )
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename=plotname, auto_open=False)
    return


def plot_pie_chart(plotname, weights, asset_class, ETF_tickers):
    fig = {
        "data": [
            {
                "values": weights,
                "labels": asset_class,
                #"domain": {"x": [0.1, 0.5], "y":[0.9, 0.5]},
                "name": "Asset Allocation",
                "text": ETF_tickers,
                "hoverinfo": "label+text+percent",
                #"textinfo": "label+percent",
                'textinfo': 'none',
                "hole": 0.5,
                "type": "pie"
            }],
        "layout": {
            #"title":"Asset Allocation",
            'paper_bgcolor': 'rgb(244, 244, 244)',
            'showlegend': False,
            "annotations": [
                {
                    "font": {
                        "size": 10
                    },
                    "showarrow": False,
                    "text": "Asset<br>Allocation",
                    "x": 0.5,
                    "y": 0.5
                }
            ]
        }
    }
    py.plot(fig, filename=plotname, auto_open=False)
    return
