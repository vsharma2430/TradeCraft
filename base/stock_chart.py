import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas import DataFrame
from datetime import datetime
from base.misc import *
from base.stock_base import trace_types,rolling_window
from base.stock_enum import *
from plotly.express.colors import qualitative


colors_pastel = qualitative.Pastel

def get_dates(df):
    get_dt = lambda dd : datetime.fromtimestamp(dd/1000000000)
    return [get_dt(dd) for dd in df.index.values.tolist()]

def get_chart(history_data_df:DataFrame,chart_type:Chart_Type):
    chart=None
    if(chart_type == Chart_Type.CLASSIC):
            chart = get_detailed_chart(history_data_df,simple_chart=True)
    if(chart_type == Chart_Type.DETAILED):
            chart = get_detailed_chart(history_data_df,simple_chart=False)
    elif(chart_type == Chart_Type.VOLUME):
            chart = get_chart_with_volume(history_data_df)
    return chart

def get_simple_chart(df:DataFrame):
    fig = df.plot(backend='plotly')
    return fig.to_html(full_html=False)

def get_detailed_chart(df:DataFrame,simple_chart=True,simple_window=100):
    subplot_titles=('OHLC','Volume')
    row_width=[0.1,0.8]
    fig = make_subplots(rows=len(subplot_titles), cols=1, shared_xaxes=True, 
                vertical_spacing=min(row_width)/2, subplot_titles=subplot_titles, 
                row_width=row_width)

    dates = get_dates(df)
    fig.add_trace(go.Candlestick(x=dates,open=df["Open"], high=df["High"],
                    low=df["Low"], close=df["Close"], name="OHLC"), 
                    row=1, col=1)
    
    df_candle_marker = DataFrame()
    lowest_point = min(df['Open'].min(),df['Close'].min(),df['High'].min(),df['Low'].min())
    defer_y_factor = 0.05
    max_cs,min_cs = df['CandleCumSum'].max(),df['CandleCumSum'].min()
    candle_date_indices = np.array(df['CandlePattern'].to_numpy().nonzero()).tolist()[0]
    df_candle_marker['date'] = [dates[x].date() for x in candle_date_indices]
    df_candle_marker['candle_score'] = [df.iloc[x]['CandleScore'] for x in candle_date_indices]
    df_candle_marker['candle_cumsum_color'] = [colors_pastel[0] if df.iloc[x]['CandleCumSum'] > 0 else colors_pastel[1] for x in candle_date_indices]
    df_candle_marker['candle_cumsum_abs'] = [abs(df.iloc[x]['CandleCumSum'])/defer_y_factor for x in candle_date_indices]
    df_candle_marker['name'] = [f'{first_chars_list(df.iloc[x]['CandlePattern'])} ({df.iloc[x]['CandleScore']},{df.iloc[x]['CandleCumSum']})' for x in candle_date_indices]
    df_candle_marker['y'] = [lowest_point*(1-(max_cs-min_cs)*defer_y_factor) + df.iloc[x]['CandleCumSum']*2*defer_y_factor  for x in candle_date_indices]
    
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
                    
    fig.add_trace(go.Scatter(x=df_candle_marker['date'],y=df_candle_marker['y'],
                             text=df_candle_marker['name'], name='Candle Patterns',
                             marker=dict(size=df_candle_marker['candle_cumsum_abs'],
                             color=df_candle_marker['candle_cumsum_color']),
                             mode= 'markers', showlegend=True), row=1, col=1)
    
    fig.add_trace(go.Bar(x=dates,y=df['Volume'],name='Volume', showlegend=True), row=2, col=1)
    fig.update(layout_xaxis_rangeslider_visible=False)
    
    return fig.to_html(full_html=False)

def get_chart_with_volume(df:DataFrame):
    dates = get_dates(df)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Candlestick(x=dates,
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'],name="OHLC"),
                    secondary_y=True)
    fig.add_trace(go.Bar(x=dates,y=df['Volume'],name='Volume',marker_color='lightsalmon',opacity=0.5),
                secondary_y=False)
    fig.layout.yaxis2.showgrid=False
    return fig.to_html(full_html=False)

def add_chart_context(context:dict,chart:int):
    context['simple_url'],context['simple_selected']=f'1','selected' if chart == Chart_Type.CLASSIC else ''
    context['detailed_url'],context['detailed_selected']=f'2','selected' if chart == Chart_Type.DETAILED else ''
    context['volume_url'],context['volume_selected']=f'3','selected' if chart == Chart_Type.VOLUME else ''