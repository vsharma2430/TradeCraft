import pandas as pd
import plotly

if(__name__ == '__main__'):
    df = pd.DataFrame(dict(a=[1,3,2], b=[3,2,1]))
    fig = df.plot(backend='plotly')
    fig.to_html()
    #fig.write_html('abc.html')

    print(fig)