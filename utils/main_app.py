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

def main_engine(parameters: "Parameters", progress_bar = False, chartwithfact=True):
    '''
    Main engine of the application. It updates stock data from Yahoo Finance,
    manages the comparison and returns the next day change of the stock price.

    Parameters:
        parameters: Parameters object (ticker, indicator_setup, first_base_date, last_base_date, projection_date)
        progress_bar: QProgressBar object
        chartwithfact: bool (True if the chart should be generated with the fact data)

    Returns:
        success: tuple (returns False and a message if the comparison failed)
        candles_for_chart: pd.DataFrame (provided by get_data_from_mongodb or data_downloader module /with all indicators/)
        median_highchg: float (median of the highchg values of the matching benchmark)
        median_lowchg: float (median of the lowchg values of the matching benchmark)
        chartwithfact: bool
        next_day_chg_dict: dict {'Lowchg': list, 'Highchg': list} / next day change of the stock low and high price
    '''
    
    db_exists = check_stock_data_in_mongodb(coll=parameters.ticker)
    if db_exists[0] == False:
        stock_df = download_from_yahoofin(ticker=parameters.ticker, period='max')
        stock_df = add_indicator(stock_df, indicator='all')
        write_stock_data_to_mongodb(stock_df, coll=parameters.ticker)
        print(f'{stock_df}\n')
    else:
        stock_df_expasion = download_from_yahoofin(ticker=parameters.ticker, start=db_exists[1])
        stock_df = get_stock_data_from_mongodb(coll= parameters.ticker, range='last')
        stock_df = pd.concat([stock_df, stock_df_expasion], axis=0, ignore_index=True)
        stock_df = add_indicator(stock_df, indicator='all')
        write_stock_data_to_mongodb(stock_df, coll=parameters.ticker, replace=False)

    stock_df = get_stock_data_from_mongodb(coll=parameters.ticker)
    print(f'{stock_df}\n')

    compared_period = parameters.indicator_setup['days']
    candles = get_candles_from_df(stock_df, date=parameters.last_base_date, period=compared_period+1)
    if candles == False:
        message = "CLOSED fact data for the day before projection date doesn't exist!\nPlease wait the market closure!"
        return (False, message), False, False, False, False, False
    print(f'Candles:\n{candles}\n')

    pattern = AnalyserEngine(candles, period=compared_period)
    print(f'Fingerprint:\n{pattern.fingerprint}\n')

    print(f'Comparing data, may take several minutes!\n\nParameters:\nTime horizon: {parameters.first_base_date} - {parameters.last_base_date}\n'\
          f'Ticker: {parameters.ticker}\nIndicator setup: {parameters.indicator_setup}\n')

    first_base_date = QDate.fromString(parameters.first_base_date, 'yyyy-MM-dd')
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

            comparison_data = pattern.generate_comparison_dict(pattern_benchmark, parameters.indicator_setup)

            result = AnalyserEngine.check_similarity(comparison_data, pattern_benchmark.indexes)
            if result[1]:
                dates_of_matching_benchmark.update({result})
     
    print(f'{dates_of_matching_benchmark}\n')
    if dates_of_matching_benchmark == {}:
        message = "No hit with the chosen indicator setup!"
        return (False, message), False, False, False, False, False

    print(f'Number of hits: {len(dates_of_matching_benchmark)}')
    if len(dates_of_matching_benchmark) >767:
        message = "Too many hits with the chosen indicator setup!"
        return (False, message), False, False, False, False, False
    
    pattern.set_next_day_chg(stock_df, dates_of_matching_benchmark)
    
    if chartwithfact and stock_df.tail(1).index[0] > get_index_from_df(stock_df, parameters.last_base_date):
        last_day = stock_df['Date'][get_index_from_df(stock_df, parameters.last_base_date)+1]
    elif chartwithfact and not stock_df.tail(1).index[0] > get_index_from_df(stock_df, parameters.last_base_date):
        last_day = parameters.last_base_date
        chartwithfact = False
        print(f'Fact data for the following date of {parameters.last_base_date} is not available!\n')
    else:
        last_day = parameters.last_base_date
    
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
    from calculation_object import Parameters
    parameters = Parameters()
    main_engine(parameters)