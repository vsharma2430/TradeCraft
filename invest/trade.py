from datetime import datetime
from base.stock_enum import *
from pydantic import BaseModel, PositiveInt
from typing import Optional

#HEADER - SYMBOL,DATE,OPERATION,PRICE,QTY

class Trade(BaseModel):
    date : datetime = None
    operation : Stock_Trade = Stock_Trade.BUY
    symbol : str = ''
    price : float = 0
    quantity : float = 0
    pl: Optional[float] = 0


    