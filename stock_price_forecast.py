import pandas as pd
from utils import initial_download_from_yahoofin,\
                  add_indicator,\
                  write_data_to_mongodb,\
                  get_data_from_mongodb

if __name__ == '__main__':
    stock_df = initial_download_from_yahoofin(period='3mo')
    stock_df = add_indicator(stock_df, indicator='all')
    write_data_to_mongodb(stock_df)
    print(f'{stock_df}\n')

    stock_df = get_data_from_mongodb()
    print(f'{stock_df}\n')
