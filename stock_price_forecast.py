import pandas as pd
from utils import initial_download_from_yahoofin,\
                  add_indicator,\
                  write_data_to_mongodb,\
                  get_data_from_mongodb,\
                  get_candles_from_df,\
                  AnalyserEngine

if __name__ == '__main__':
    # stock_df = initial_download_from_yahoofin(period='max')
    # stock_df = add_indicator(stock_df, indicator='all')
    # write_data_to_mongodb(stock_df)
    # print(f'{stock_df}\n')

    stock_df = get_data_from_mongodb()
    print(f'{stock_df}\n')

    candles = get_candles_from_df(stock_df, date='2024-05-09', period=4)
    print(f'Candles:\n{candles}\n')

    pattern = AnalyserEngine(candles)
    print(f'Fingerprint:\n{pattern.fingerprint}\n')

    dates_of_matching_benchmark = {}
    for index, row in stock_df.loc[22000:].iterrows():
        if pattern.date != row['Date']:

            benchmark_date = row['Date']
            candles_benchmark = get_candles_from_df(stock_df, benchmark_date, period=4)
            pattern_benchmark = AnalyserEngine(candles_benchmark, period=3)

            comparison_data = pattern.generate_comparison_dict(pattern_benchmark, tolerance=70)

            result = AnalyserEngine.check_similarity(comparison_data, pattern_benchmark.indexes)
            if result[1]:
                dates_of_matching_benchmark.update({result})
     
    print(f'{dates_of_matching_benchmark}\n')

    next_day_chg_dict = AnalyserEngine.get_next_day_chg(stock_df, dates_of_matching_benchmark)

    print(next_day_chg_dict)
