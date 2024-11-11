from datetime import datetime
from base.stock_enum import *
from pydantic import BaseModel, PositiveInt

class Trade(BaseModel):
    date : datetime
    operation : Stock_Trade
    symbol : str
    price : float
    quantity : float
    