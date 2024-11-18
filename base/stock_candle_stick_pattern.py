import pandas as pd
import numpy as np
from base.stock_enum import *

def candle_score(lst_0,lst_1,lst_2):    
    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
    DojiSize = 0.1
    
    doji=(abs(O_0 - C_0) <= (H_0 - L_0) * DojiSize)
    
    hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((C_0 - L_0)/(.001 + H_0 - L_0) > 0.6) & ((O_0 - L_0)/(.001 + H_0 - L_0) > 0.6))
    
    inverted_hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((H_0 - C_0)/(.001 + H_0 - L_0) > 0.6) & ((H_0 - O_0)/(.001 + H_0 - L_0) > 0.6))
    
    bullish_reversal= (O_2 > C_2)&(O_1 > C_1)&doji
    
    bearish_reversal= (O_2 < C_2)&(O_1 < C_1)&doji
    
    evening_star=(C_2 > O_2) & (min(O_1, C_1) > C_2) & (O_0 < min(O_1, C_1)) & (C_0 < O_0 )
    
    morning_star=(C_2 < O_2) & (min(O_1, C_1) < C_2) & (O_0 > min(O_1, C_1)) & (C_0 > O_0 )
    
    shooting_Star_bearish=(O_1 < C_1) & (O_0 > C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & inverted_hammer
    
    shooting_Star_bullish=(O_1 > C_1) & (O_0 < C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & inverted_hammer
    
    bearish_harami=(C_1 > O_1) & (O_0 > C_0) & (O_0 <= C_1) & (O_1 <= C_0) & ((O_0 - C_0) < (C_1 - O_1 ))
    
    Bullish_Harami=(O_1 > C_1) & (C_0 > O_0) & (C_0 <= O_1) & (C_1 <= O_0) & ((C_0 - O_0) < (O_1 - C_1))
    
    Bearish_Engulfing=((C_1 > O_1) & (O_0 > C_0)) & ((O_0 >= C_1) & (O_1 >= C_0)) & ((O_0 - C_0) > (C_1 - O_1 ))
    
    Bullish_Engulfing=(O_1 > C_1) & (C_0 > O_0) & (C_0 >= O_1) & (C_1 >= O_0) & ((C_0 - O_0) > (O_1 - C_1 ))
    
    Piercing_Line_bullish=(C_1 < O_1) & (C_0 > O_0) & (O_0 < L_1) & (C_0 > C_1)& (C_0>((O_1 + C_1)/2)) & (C_0 < O_1)

    Hanging_Man_bullish=(C_1 < O_1) & (O_0 < L_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & hammer

    Hanging_Man_bearish=(C_1 > O_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & hammer

    strCandle=[]
    candle_score=0
    
    if doji:
        strCandle.append(Candle_Pattern.Doji)
    if evening_star:
        strCandle.append(Candle_Pattern.Evening_Star)
        candle_score=candle_score-1
    if morning_star:
        strCandle.append(Candle_Pattern.Morning_Star)
        candle_score=candle_score+1
    if shooting_Star_bearish:
        strCandle.append(Candle_Pattern.Shooting_Star_Bearish)
        candle_score=candle_score-1
    if shooting_Star_bullish:
        strCandle.append(Candle_Pattern.Shooting_Star_Bullish)
        candle_score=candle_score-1
    if    hammer:
        strCandle.append(Candle_Pattern.Hammer)
    if    inverted_hammer:
        strCandle.append(Candle_Pattern.Inverted_Hammer)
    if    bearish_harami:
        strCandle.append(Candle_Pattern.Bearish_Harami)
        candle_score=candle_score-1
    if    Bullish_Harami:
        strCandle.append(Candle_Pattern.Bullish_Harami)
        candle_score=candle_score+1
    if    Bearish_Engulfing:
        strCandle.append(Candle_Pattern.Bearish_Engulfing)
        candle_score=candle_score-1
    if    Bullish_Engulfing:
        strCandle.append(Candle_Pattern.Bullish_Engulfing)
        candle_score=candle_score+1
    if    bullish_reversal:
        strCandle.append(Candle_Pattern.Bullish_Reversal)
        candle_score=candle_score+1
    if    bearish_reversal:
        strCandle.append(Candle_Pattern.Bearish_Reversal)
        candle_score=candle_score-1
    if    Piercing_Line_bullish:
        strCandle.append(Candle_Pattern.Piercing_Line_Bullish)
        candle_score=candle_score+1
    if    Hanging_Man_bearish:
        strCandle.append(Candle_Pattern.Hanging_Man_Bearish)
        candle_score=candle_score-1
    if    Hanging_Man_bullish:
        strCandle.append(Candle_Pattern.Hanging_Man_Bullish)
        candle_score=candle_score+1
        
    #return candle_score
    return candle_score,strCandle

def support_resistance(data, window=20):
    low_marker = 'low' if 'low' in data else 'Low'
    high_marker = 'high' if 'high' in data else 'High'

    support = data[low_marker].rolling(window=window).min()
    resistance = data[high_marker].rolling(window=window).max()

    return support, resistance

def candle_df(df,dma_window:int=rolling_window,support_window:int=rolling_window):
    df_candle=df.copy()
    df_candle['CandleScore']=0
    df_candle['CandlePattern']=''

    for c in range(2,len(df_candle)):
        cscore,cpattern=0,''
        lst_2=[df_candle['Open'].iloc[c-2],df_candle['High'].iloc[c-2],df_candle['Low'].iloc[c-2],df_candle['Close'].iloc[c-2]]
        lst_1=[df_candle['Open'].iloc[c-1],df_candle['High'].iloc[c-1],df_candle['Low'].iloc[c-1],df_candle['Close'].iloc[c-1]]
        lst_0=[df_candle['Open'].iloc[c],df_candle['High'].iloc[c],df_candle['Low'].iloc[c],df_candle['Close'].iloc[c]]
        cscore,cpattern=candle_score(lst_0,lst_1,lst_2)    
        df_candle['CandleScore'].iat[c]=cscore
        df_candle['CandlePattern'].iat[c]='; '.join([f'{cp.name}' for cp in cpattern])
    
    df_candle['CandleCumSum']=df_candle['CandleScore'].rolling(3).sum()

    df_rolling = lambda df_head,rolling_window:df_candle[df_head].rolling(window=rolling_window).mean()
    
    for dmaX in dma_window:
        df_candle[f'DMA_{dmaX}']=df_rolling(df_head='Close',rolling_window=int(dmaX))

    for supportX in support_window:
        df_candle[f'Support_{supportX}'],df_candle[f'Resistance_{supportX}'] = support_resistance(data=df_candle,window=supportX)

    return {
        'candle_df':df_candle,
    }

