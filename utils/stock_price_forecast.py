import pandas as pd
from data_supply import initial_download_from_yahoofin, add_indicator

if __name__ == '__main__':
    stock_df = initial_download_from_yahoofin(period='1y')
    stock_df = add_indicator(stock_df, indicator='all')
    print(f'{stock_df}\n')
    print(stock_df.iloc[251,:])
