import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


#import numpy as np

# Plot the result --------------------------------------------------------------------------------------------------

plotly.tools.set_credentials_file(username='afteradam', api_key='4B0cCLHHbHpwkGasGD5E')


def plot_line_chart(plotname, tau, return_list, vol_list):

    trace0 = go.Scatter(
        x=list(tau),
        y=return_list,
        name="Return",
        visible=True,
    )
    trace1 = go.Scatter(
        x=list(tau),
        y=vol_list,
        name="Volatility",
        visible=False,
    )


    data = [trace0, trace1]
    layout = go.Layout(
        title='Return & Volatility against Risk Tolerance',
        autosize=False,
        width=700,
        height=500,
        updatemenus=list([
            dict(
                x=1.3,
                # xanchor='left',
                y=1,
                yanchor='top',

                buttons=list([

                    dict(

                        label='Return Only',
                        method='restyle',
                        args=['visible', [True, False]],
                    ),
                    dict(

                        label='Volatility Only',
                        method='restyle',
                        args=['visible', [False, True]],
                    ),
                    dict(
                        label='All',
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


