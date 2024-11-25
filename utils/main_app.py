import pandas as pd
import sys
from PyQt6.QtCore import QDate
if __name__ != '__main__':
    from utils import download_from_yahoofin,\
                    add_indicator,\
                    write_stock_data_to_mongodb,\
                    get_stock_data_from_mongodb,\
                    get_candles_from_df,\
                    get_index_from_df,\
                    AnalyserEngine,\
                    check_stock_data_in_mongodb,\
                    get_first_correct_date

def main_engine(progress_bar = False, ticker ='^GDAXI', first_base_date = '2000-01-01', last_base_date = '2024-10-18', chartwithfact=True):
    # ------------- MAIN DRIVERS -------------
    
    # -- ticker --
    # -> see ticker names on Yahoo Finance; tickers e.g.:
    # -> S&P500: ^GSPC
    # -> DAX: ^GDAXI
    # -> NASDAQ: ^IXIC
    # -> OTP: OTP.BD
    ticker_name = {'^GSPC': 'S&P 500', '^GDAXI': 'DAX', 'OTP.BD': 'OTP', '^IXIC': 'NASDAQ'}
    
    # -- last_base_date -- of last fact data; the projection will be prepared for the following day
    
    compared_period = 3
    tolerance = 100
    # -> proposed set: period = 2-3 , tolerance = 50-100
    # -> lower period and higher tolerance more hit
    
    # --- chartwithfact
    # -> puts fact data on japanese candle chart in case of projection for historical data (testing the model)
    # -> only available if last_base_date is not the last available data (not available for projections based on last day data)
    
    # first_base_date_index = get_first_correct_date(coll=ticker)[0]
    # -> yahoo database is not perfect; no suitable data is available in database before e.g:
    # -> ^GSPC: 1982-04-20 (index: 13602) 
    # -> ^GDAXI: 1993-12-15 (index: 1491)
    # -> ^IXIC: 1984-10-12 (index: 3459)
    # ----------------------------------------      
    
    if ticker not in ticker_name:
        ticker_name.update({ticker: ticker})

    db_exists = check_stock_data_in_mongodb(coll=ticker)
    if db_exists[0] == False:
        stock_df = download_from_yahoofin(ticker=ticker, period='max')
        stock_df = add_indicator(stock_df, indicator='all')
        write_stock_data_to_mongodb(stock_df, coll=ticker)
        print(f'{stock_df}\n')
    else:
        stock_df_expasion = download_from_yahoofin(ticker=ticker, start=db_exists[1])
        stock_df = get_stock_data_from_mongodb(coll= ticker, range='last')
        stock_df = pd.concat([stock_df, stock_df_expasion], axis=0, ignore_index=True)
        stock_df = add_indicator(stock_df, indicator='all')
        write_stock_data_to_mongodb(stock_df, coll=ticker, replace=False)

    stock_df = get_stock_data_from_mongodb(coll=ticker)
    print(f'{stock_df}\n')

    candles = get_candles_from_df(stock_df, date=last_base_date, period=compared_period+1)
    if candles == False:
        message = "CLOSED fact data for the day before projection date doesn't exist!\nPlease wait the market closure!"
        return (False, message), False, False, False, False, False
    print(f'Candles:\n{candles}\n')

    pattern = AnalyserEngine(candles, period=compared_period)
    print(f'Fingerprint:\n{pattern.fingerprint}\n')

    print('Comparing data, may take several minutes!\n')

    first_base_date = QDate.fromString(first_base_date, 'yyyy-MM-dd')
    while stock_df[stock_df['Date'] == first_base_date.toString('yyyy-MM-dd')].empty:
        first_base_date = first_base_date.addDays(1)
    else: 
        first_base_date_index = stock_df[stock_df['Date'] == first_base_date.toString('yyyy-MM-dd')].index[0]

    if progress_bar != False:
        progress_bar.setValue(0)
        progress_bar_max = 0
        progress_bar_value = 0
        for index, row in stock_df.loc[first_base_date_index+compared_period+50:].iterrows():
            progress_bar_max += 1
        progress_bar.setMaximum(progress_bar_max)
   
    dates_of_matching_benchmark = {}
    for index, row in stock_df.loc[first_base_date_index+compared_period+50:].iterrows():
        if pattern.date != row['Date']:
            
            if progress_bar != False:
                progress_bar_value += 1
                progress_bar.setValue(progress_bar_value)

            benchmark_date = row['Date']
            candles_benchmark = get_candles_from_df(stock_df, benchmark_date, period=compared_period+1)
            pattern_benchmark = AnalyserEngine(candles_benchmark, period=compared_period)

            comparison_data = pattern.generate_comparison_dict(pattern_benchmark, tolerance=tolerance)

            result = AnalyserEngine.check_similarity(comparison_data, pattern_benchmark.indexes)
            if result[1]:
                dates_of_matching_benchmark.update({result})
     
    print(f'{dates_of_matching_benchmark}\n')
    if dates_of_matching_benchmark == {}:
        message = "No hit with the chosen indicator setup!"
        return (False, message), False, False, False, False, False

    pattern.set_next_day_chg(stock_df, dates_of_matching_benchmark)
    
    if chartwithfact and stock_df.tail(1).index[0] > get_index_from_df(stock_df, last_base_date):
        last_day = stock_df['Date'][get_index_from_df(stock_df, last_base_date)+1]
    elif chartwithfact and not stock_df.tail(1).index[0] > get_index_from_df(stock_df, last_base_date):
        last_day = last_base_date
        chartwithfact = False
        print(f'Fact data for the following date of {last_base_date} is not available!\n')
    else:
        last_day = last_base_date
    
    candles_for_chart = get_candles_from_df(stock_df, date=last_day, period=compared_period+1)
    median_lowchg = pattern.stats('median_Lowchg')
    median_highchg = pattern.stats('median_Highchg')
    
    print(candles_for_chart)
    print(median_highchg)
    print(median_lowchg)

    success = (True, '')
    return success, candles_for_chart, median_highchg, median_lowchg, chartwithfact, pattern.next_day_chg_dict  

if __name__ == '__main__':
    from data_downloader import download_from_yahoofin, add_indicator
    from stock_database_manager import get_stock_data_from_mongodb, write_stock_data_to_mongodb, get_candles_from_df,\
                                check_stock_data_in_mongodb, get_index_from_df, get_first_correct_date
    from data_analyser_engine import AnalyserEngine
    from chart_generator import show_histogram, show_candle_chart, show_all_charts
    main_engine()