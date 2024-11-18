from enum import Enum

class Stock_Type(Enum):
    EQUITY = 1
    ETF = 2
    COMMODITY = 3
    
class Stock_Exchange(Enum):
    NSE = 1
    BSE = 2
    
class Stock_Symbol(Enum):
    PLAIN = 1
    GFIN = 2
    YFIN = 3
    
class Stock_Trade(Enum):
    BUY = 1
    SELL = 2

class Candle_Pattern(Enum):
    Doji = 1
    Evening_Star = 2
    Morning_Star = 3
    Shooting_Star_Bearish = 4
    Shooting_Star_Bullish = 5 
    Hammer = 5
    Inverted_Hammer = 6
    Bearish_Harami = 7
    Bullish_Harami = 8
    Bearish_Engulfing = 9
    Bullish_Engulfing = 10
    Bullish_Reversal = 11
    Bearish_Reversal = 12
    Piercing_Line_Bullish = 13
    Hanging_Man_Bearish = 14
    Hanging_Man_Bullish = 15

rolling_window:int=[5,10,20,50,100,200]
trace_types = ['DMA','Support','Resistance']

