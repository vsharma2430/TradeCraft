stock_props = lambda stk : {'title':f'{stk.upper()}',
                                 'list':[{ 'caption': 'Lists' , 'href' : f'/{stk}/list/'},
                                         { 'caption': 'All Listed (NSE)' , 'href' : f'/{stk}/history/'},
                                         { 'caption': 'Portfolio' , 'href' : f'/{stk}/portfolio/'},
                                         { 'caption': 'Backtest' , 'href' : f'/{stk}/backtest/'} if stk == 'etf' else None,
                                         ],}

nav_props = {'nav_title':'TradeCraft',
             'nav_list':[{ 'caption': 'ETF' , 'href' : f'/etf/' , 'props' : stock_props(stk='etf')},
                        { 'caption': 'Stock' , 'href' : f'/stock/' , 'props' : stock_props(stk='stock')}],}

nav_context = {
                'nav_context':nav_props
                }