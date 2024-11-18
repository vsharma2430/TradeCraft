import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas import DataFrame
from datetime import datetime
from base.misc import *
from base.stock_base import trace_types,rolling_window
import plotly.express as px

colors = px.colors.qualitative.Pastel

def get_dates(df):
    return [datetime.fromtimestamp(dd/1000000000) for dd in df.index.values.tolist()]
    
def get_simple_chart(df:DataFrame):
    fig = df.plot(backend='plotly')
    return fig.to_html(full_html=False)

def get_chart(df:DataFrame,simple_chart=True,simple_window=100):
    subplot_titles=('OHLC','Volume')
    row_width=[0.1,0.8]
    fig = make_subplots(rows=len(subplot_titles), cols=1, shared_xaxes=True, 
                vertical_spacing=min(row_width)/2, subplot_titles=subplot_titles, 
                row_width=row_width)

    dates = get_dates(df)
    fig.add_trace(go.Candlestick(x=dates,open=df["Open"], high=df["High"],
                    low=df["Low"], close=df["Close"], name="OHLC"), 
                    row=1, col=1)
    
    candle_dates = np.array(df['CandlePattern'].to_numpy().nonzero()).tolist()[0]
    
    getScatter = lambda column,name=None:go.Scatter(x=dates,y=df[column], mode='lines' , name=column if name == None else name, showlegend=True)
    addTrace = lambda trace,trace_name=None,row=1,col=1: fig.add_trace(getScatter(trace,trace_name), row=row, col=col)   

    for x in trace_types:
        simple_win_head = f'{x}_{simple_window}'
        if(simple_win_head in df):
            addTrace(simple_win_head,simple_win_head)
    
    if(simple_chart == False):
        for x in trace_types:
            for y in rolling_window:
                win_head = f'{x}_{y}'
                if(win_head in df):
                    addTrace(win_head)

    fig.add_trace(go.Bar(x=dates,y=df['Volume'],name='Volume', showlegend=True), row=2, col=1)
    fig.update(layout_xaxis_rangeslider_visible=False)
    
    return fig.to_html(full_html=False)

def get_chart_with_volume(df:DataFrame):
    dates = get_dates(df)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Candlestick(x=dates,
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close']),
                    secondary_y=True)
    fig.add_trace(go.Bar(x=dates,y=df['Volume'],marker_color='lightsalmon',opacity=0.5),
                secondary_y=False)
    fig.layout.yaxis2.showgrid=False
    return fig.to_html(full_html=False)