import pandas as pd
from utils import initial_download_from_yahoofin,\
                  add_indicator,\
                  write_data_to_mongodb,\
                  get_data_from_mongodb,\
                  AnalyserEngine

if __name__ == '__main__':
    stock_df = initial_download_from_yahoofin(period='1y')
    stock_df = add_indicator(stock_df, indicator='all')
    write_data_to_mongodb(stock_df)
    print(f'{stock_df}\n')

    stock_df = get_data_from_mongodb()
    print(f'{stock_df}\n')

    candles = stock_df.iloc[(len(stock_df)-4):(len(stock_df))].to_dict('dict') # !!! a function in data_supply module is required
    print(f'Candles:\n{candles}')

    pattern = AnalyserEngine(candles)
    print(f'Fingerprint:\n{pattern.fingerprint()}')

