import pandas as pd
from utils import download_from_yahoofin,\
                  add_indicator,\
                  write_data_to_mongodb,\
                  get_data_from_mongodb,\
                  get_candles_from_df,\
                  AnalyserEngine,\
                  show_histogram,\
                  check_data_in_mongodb

if __name__ == '__main__':
       
    db_exists = check_data_in_mongodb()
    if db_exists[0] == False:
        stock_df = download_from_yahoofin(period='max')
        stock_df = add_indicator(stock_df, indicator='all')
        write_data_to_mongodb(stock_df)
        print(f'{stock_df}\n')
    else:
        stock_df_expasion = download_from_yahoofin(start=db_exists[1])
        stock_df = get_data_from_mongodb(range='last')
        stock_df = pd.concat([stock_df, stock_df_expasion], axis=0, ignore_index=True)
        stock_df = add_indicator(stock_df, indicator='all')
        write_data_to_mongodb(stock_df, replace=False)
        print(f'{stock_df}\n')

    stock_df = get_data_from_mongodb()
    print(f'{stock_df}\n')

    # ------------- MAIN drivers -------------
    date = '2024-05-09'
    compared_period = 2
    tolerance = 65
    # ----------------------------------------

    candles = get_candles_from_df(stock_df, date=date, period=compared_period+1)
    print(f'Candles:\n{candles}\n')

    pattern = AnalyserEngine(candles)
    print(f'Fingerprint:\n{pattern.fingerprint}\n')

    print('Downloading and preparing data could take several minutes!\n')

    dates_of_matching_benchmark = {}
    for index, row in stock_df.loc[13605:].iterrows(): # first correct data of GSPC is on index 13605 '1982-04-20'
        if pattern.date != row['Date']:

            benchmark_date = row['Date']
            candles_benchmark = get_candles_from_df(stock_df, benchmark_date, period=compared_period+1)
            pattern_benchmark = AnalyserEngine(candles_benchmark, period=compared_period)

            comparison_data = pattern.generate_comparison_dict(pattern_benchmark, tolerance=tolerance)

            result = AnalyserEngine.check_similarity(comparison_data, pattern_benchmark.indexes)
            if result[1]:
                dates_of_matching_benchmark.update({result})
     
    print(f'{dates_of_matching_benchmark}\n')

    next_day_chg_dict = AnalyserEngine.get_next_day_chg(stock_df, dates_of_matching_benchmark)

    print(next_day_chg_dict)

    show_histogram(date, Lowchg=next_day_chg_dict['Lowchg'], Highchg=next_day_chg_dict['Highchg'])
