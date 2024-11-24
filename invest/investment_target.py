from base.misc import *

price_server = 'http://localhost:8006/'
capital = 300000
sell_target = 0.06
invest_parts = 60
order_price = capital / invest_parts

def get_settings():
    return {
        'capital' : get_comma_format(capital),
        'sell_target' : get_percentage_format(sell_target),
        'order_price': get_comma_format(order_price)
    }