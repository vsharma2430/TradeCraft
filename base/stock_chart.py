import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas import DataFrame
from datetime import datetime
from base.misc import *
import plotly.express as px

def get_simple_chart(df:DataFrame):
        fig = df.plot(backend='plotly')
        return fig.to_html(full_html=False)

def get_chart(df:DataFrame,simple_chart=True):
    subplot_titles=('OHLC','Volume','Patterns')
    row_width=[0.2,0.1,0.8]
    fig = make_subplots(rows=len(subplot_titles), cols=1, shared_xaxes=True, 
                vertical_spacing=min(row_width)/2, subplot_titles=subplot_titles, 
                row_width=row_width)

    dates = [datetime.fromtimestamp(dd/1000000000) for dd in df.index.values.tolist()]
    fig.add_trace(go.Candlestick(x=dates,open=df["Open"], high=df["High"],
                    low=df["Low"], close=df["Close"], name="OHLC"), 
                    row=1, col=1)
    candle_dates = np.array(df['CandlePattern'].to_numpy().nonzero()).tolist()[0]
    
    getScatter = lambda column,name=None:go.Scatter(x=dates,y=df[column], mode='lines' , name=column if name == None else name, showlegend=True)
    addTrace = lambda trace,trace_name=None,row=1,col=1: fig.add_trace(getScatter(trace,trace_name), row=row, col=col)   
        
    trace_types = ['DMA','Support','Resistance']
    for x in trace_types:
        addTrace(x,f'{x}_7')
    
    if(simple_chart == False):
        for x in trace_types:
            for y in ['1','20','60']:
                addTrace(f'{x}_{y}')

    fig.add_trace(go.Bar(x=dates,y=df['Volume'],name='Volume', showlegend=True), row=2, col=1)

    scatter_no = 5
    scatter_wid = row_width[0]/(scatter_no+1)
    colors = px.colors.qualitative.Pastel
    fig.update_layout(
        shapes = [
            dict(x0=dates[x], x1=dates[x], y0=0, y1=1, xref='x', yref='paper',line_width=1,line_color=colors[index%len(colors)]) for index,x in enumerate(candle_dates)
            ],
        annotations = [
            dict(x=dates[x], y=(scatter_wid*(index%scatter_no)), xref='x', yref='paper',showarrow=False, xanchor='left',bgcolor=colors[index%len(colors)],
                text= f'{first_chars_list(df.iloc[x]['CandlePattern'])} ({df.iloc[x]['CandleScore']},{df.iloc[x]['CandleCumSum']})') for index,x in enumerate(candle_dates)
            ]
    )

    fig.update(layout_xaxis_rangeslider_visible=False)
    return fig.to_html(full_html=False)

def get_chart_with_volume(df:DataFrame):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Candlestick(
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close']),
                secondary_y=True)
    fig.add_trace(go.Bar(y=df['Volume']),
                secondary_y=False)
    fig.layout.yaxis2.showgrid=False
    return fig.to_html(full_html=False)