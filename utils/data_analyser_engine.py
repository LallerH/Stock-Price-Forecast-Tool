import pandas as pd

if __name__ != '__main__':
    try:
        from utils.stock_database_manager import get_candles_from_df
    except:
        from stock_database_manager import get_candles_from_df

class AnalyserEngine:

    def __init__(self, candles: dict, period=3):
        '''
    :Processing of data:
        - generate fingerprint for data of a certain date
        - searching for historical data having the same fingerprint
        - make projection based on historical data with the same fingerprint
    
    :Parameters: ()
        candles : {dict{dict}} stock data from DataFrame of data_downloader module with all indicators
            {keys -> keys of DataFrame, values -> {keys -> indexes of Dataframe, values: stock data}} 
        period : int
            valid period: no longer than (len(candles)-1)
        '''
        if len(candles) < period:
            raise Exception('Argument mismatch: number of days in CANDLES list /length/ must be '\
                            '1 day longer than PERIOD!')
        
        indexes = [] # build a list of indexes of candles (ascendent)
        for key in candles['Date']:
            indexes.append(key)
        indexes.sort()

        for item in indexes[:-1]: # security check if dates are ascendent
            if candles['Date'][item] >= candles['Date'][item+1]:
                raise Exception('Database error: stock data is not stored ascendent in database!')
        
        self.candles = candles
        self.indexes = indexes
        self.period = period
        self.date = candles['Date'][indexes[-1]]
        self.fingerprint = self.fingerprint()
        self.next_day_chg_dict = {}

    def fingerprint(self)-> dict:
        '''
        :Generate fingerprint for data of a certain date
        
        :Utilized arguments of AnalyserEngine class:
            candles : {dict{dict}} stock data from argument DataFrame of data_supply module with all indicators
                {keys -> keys of DataFrame, values -> {keys -> indexes of Dataframe, values: stock data}} 
            period : int
                valid period: no longer than (len(candles)-1)
        
        :Returns : dict
            -> DATE of stock data
                'Date' : {keys -> indexes of argument Dataframe, values: calculated data / str}
            -> %change of LOW data (T / T-1)
                'lowchg' : {keys, values -> as of previuos / int}
            -> %change of OPEN data (T / T-1)
                'openchg' : {keys, values -> as of previuos / int}
            -> %intraday change (CLOSE / OPEN)
                'body' : {keys, values -> as of previuos / int}
            -> %change of HIGH data (T / T-1)
                'highchg' : {keys, values -> as of previuos / int}
            -> color of candle / intraday change (CLOSE vs. OPEN)
                'color' : {keys as of previuos, values: str -> 'green' if incr., 'red' if decr. , 'neutral' if unchg.}
            -> %change of RSIAVG data (T / T-1)
                'RSIavgchg' : {keys, values -> as of previuos / int}
            -> abs. change of MACDHIST data (T - T-1)
                'MACDhistchg' : {keys, values -> as of previuos / int}
            -> %change of SMA20 data (T / T-1)
                'SMA20chg' : {keys, values -> as of previuos / int}
            -> %change of SMA50 data (T / T-1)
                'SMA50chg' : {keys, values -> as of previuos / int}
            -> range of MACDHIST (>0, <0) of the last date data
                'MACDrange' : str -> 'positive', 'negtaive', 'zero'
            -> range of RSI (>70%, <30%) of the last date data
                'RSIstate' : : str -> 'overbought', 'oversold', 'neutral'
            -> relation of SMA20 and SMA50 of the last date data
                'SMA20_50relation' : str -> 'above', 'below', 'equal'
        '''
        result = {'Date' : {},
                  'lowchg' : {},
                  'openchg' : {},
                  'body' : {},
                  'highchg' : {},
                  'color' : {},
                  'RSIavgchg' : {},
                  'RSIstate' : '',
                  'MACDhistchg' : {},
                  'MACDrange' : '',
                  'SMA20chg' : {},
                  'SMA50chg' : {},
                  'SMA20_50relation' : ''
                  }

        for idx, value in list(enumerate(self.indexes))[1:]:
            
            lowchg = self.candles['Low'][value] / self.candles['Low'][value-1]
            openchg = self.candles['Open'][value] / self.candles['Open'][value-1]
            body = self.candles['Close'][value] / self.candles['Open'][value]
            highchg = self.candles['High'][value] / self.candles['High'][value-1]
            rsiavgchg = self.candles['RSIavg'][value] / self.candles['RSIavg'][value-1]
            macdhistchg = self.candles['MACDhist'][value] - self.candles['MACDhist'][value-1]
            sma20chg = self.candles['SMA20'][value] / self.candles['SMA20'][value-1]
            sma50chg = self.candles['SMA50'][value] / self.candles['SMA50'][value-1]
            
            if self.candles['Close'][value] > self.candles['Open'][value]:
                result['color'].update({value : 'green'})
            elif self.candles['Close'][value] < self.candles['Open'][value]:
                result['color'].update({value : 'red'})
            else:
                result['color'].update({value : 'neutral'})
          
            result['Date'].update({value : self.candles['Date'][value]})
            result['lowchg'].update({value : lowchg})
            result['openchg'].update({value : openchg})
            result['body'].update({value : body})
            result['highchg'].update({value : highchg})
            result['RSIavgchg'].update({value : rsiavgchg})
            result['MACDhistchg'].update({value : macdhistchg})
            result['SMA20chg'].update({value : sma20chg})
            result['SMA50chg'].update({value : sma50chg})

        if self.candles['RSI'][self.indexes[-1]] > 70:
            result.update({'RSIstate' : 'overbought'})
        elif self.candles['RSI'][self.indexes[-1]] < 30:
            result.update({'RSIstate' : 'oversold'})
        else:
            result.update({'RSIstate' : 'neutral'})

        if self.candles['MACDhist'][self.indexes[-1]] > 0:
            result.update({'MACDrange' : 'positive'})
        elif self.candles['MACDhist'][self.indexes[-1]] < 0:
            result.update({'MACDrange' : 'negative'})
        else:
            result.update({'MACDrange' : 'zero'})

        if self.candles['SMA20'][self.indexes[-1]] > self.candles['SMA50'][self.indexes[-1]]:
            result.update({'SMA20_50relation' : 'above'})
        elif self.candles['SMA20'][self.indexes[-1]] < self.candles['SMA50'][self.indexes[-1]]:
            result.update({'SMA20_50relation' : 'below'})
        else:
            result.update({'SMA20_50relation' : 'equal'})

        return result

    def generate_comparison_dict(self, benchmark: "AnalyserEngine", indicator_setup: dict)-> dict:
        '''
        :Compares the self.fingerprint dict with a benchmark fingerprint dict
        
        :Arguments:
            benchmark: instance of AnalyserEngine class on benchmark data/date
            indicator setup: dict
        
        :Returns : dict
            -> with the same keys as of self.fingerprint dict
            -> values: TRUE if the benchmark is in the range of self.fingerprint value +/- tolerance range
                or self.fingerprint value == benchmark.fingerprint value in case of state keys (e.g.: color of candle)       
        '''
        result = {'Date' : {},
                  'lowchg' : {},
                  'openchg' : {},
                  'body' : {},
                  'highchg' : {},
                  'color' : {},
                  'RSIavgchg' : {},
                  'RSIstate' : '',
                  'MACDhistchg' : {},
                  'MACDrange' : '',
                  'SMA20chg' : {},
                  'SMA50chg' : {},
                  'SMA20_50relation' : ''
                  }
        
        numeric_indicators = ['lowchg', 'openchg', 'body', 'highchg', 'RSIavgchg', 'MACDhistchg', 'SMA20chg', 'SMA50chg']
        state_indicators = ['RSIstate', 'MACDrange', 'SMA20_50relation']

        for idx, value in list(enumerate(self.indexes))[1:]:
            result['Date'].update({(benchmark.indexes[idx]) : benchmark.candles['Date'][(benchmark.indexes[idx])]})

            for indicator in numeric_indicators:
                if indicator_setup[indicator]['selected']:
                    benchmark_value = benchmark.fingerprint[indicator][(benchmark.indexes[idx])]
                    self_value = self.fingerprint[indicator][value]
                    if indicator == 'MACDhistchg':
                        benchmark_min = benchmark_value - indicator_setup[indicator]['tolerance']
                        benchmark_max = benchmark_value + indicator_setup[indicator]['tolerance']
                    else:
                        benchmark_min = benchmark_value - indicator_setup[indicator]['tolerance']/10000
                        benchmark_max = benchmark_value + indicator_setup[indicator]['tolerance']/10000
                                      
                    if (self_value < benchmark_max) and (self_value > benchmark_min):
                        result[indicator].update({(benchmark.indexes[idx]) : True})
                    else:
                        result[indicator].update({(benchmark.indexes[idx]) : False})
            
            if indicator_setup['color']['selected']:
                if self.fingerprint['color'][value] == benchmark.fingerprint['color'][(benchmark.indexes[idx])]:
                    result['color'].update({(benchmark.indexes[idx]) : True})
                elif self.fingerprint['color'][value] == 'neutral' or benchmark.fingerprint['color'][(benchmark.indexes[idx])] == 'neutral':
                    result['color'].update({(benchmark.indexes[idx]) : True})            
                else:
                    result['color'].update({(benchmark.indexes[idx]) : False})
            
        for indicator in state_indicators:
            if indicator_setup[indicator]['selected']:
                if self.fingerprint[indicator] == benchmark.fingerprint[indicator]:
                    result.update({indicator : True})
                elif self.fingerprint[indicator] == 'equal' or self.fingerprint[indicator] == 'zero':
                    result.update({indicator : True})
                elif benchmark.fingerprint[indicator] == 'equal' or benchmark.fingerprint[indicator] == 'zero':
                    result.update({indicator : True})
                else:
                    result.update({indicator : False})

        return result

    def stats(self, indicator: str) -> int:
        '''
        :Returns the requested indicator
        
        Arguments: str ->
            'median_Lowchg',
            'median_Highchg'
        '''
        import matplotlib.cbook as cbk
        import numpy as np
        
        if indicator == 'median_Lowchg':
            return cbk.boxplot_stats(self.next_day_chg_dict['Lowchg'])[0]['med']
        
        if indicator == 'median_Highchg':
            return cbk.boxplot_stats(self.next_day_chg_dict['Highchg'])[0]['med']

    @staticmethod
    def check_similarity(comparison_dict: dict, indexes: list):
        '''
        :Evaluate comparison dict
        
        :Arguments:
            comparison dict of self.generate_comparison_dict method
            indexes: benchmark AnalyserEngine instance .indexes (needed to identify the date of similarty check)
        
        :Returns: str, bool
            -> date YYYY-MM-DD / 
            -> TRUE in case of similarity (False in else case)       
        '''
        multiplevalue_keys = ('lowchg', 'openchg', 'highchg', 'body', 'color', 'RSIavgchg', 'MACDhistchg' ,'SMA20chg', 'SMA50chg')
        singlevalue_keys = ('RSIstate', 'MACDrange', 'SMA20_50relation')

        indicator_check = {}
        for key in comparison_dict:
            if key in singlevalue_keys:
                indicator_check.update({key: comparison_dict[key]})
            elif key in multiplevalue_keys:
                indicator_check.update({key: True})
                for index in comparison_dict[key]:
                    if comparison_dict[key][index] == False:
                        indicator_check.update({key: False})

        result = True
        for key in indicator_check:
            if indicator_check[key] == False:
                result = False

        return comparison_dict['Date'][indexes[len(indexes)-1]], result

    def set_next_day_chg(self, stock_df: pd.DataFrame, dates_of_matching_benchmark: dict):
        '''
        :Calculates change of low/high price on following day of matching(similar) benchmark data
        
        :Arguments:
            stock_df: DataFrame of stock data (provided by database_manager package)
            dict object: containing matching(similar) benchmark dates: {{'YYYY-MM-DD': bool}, {...}}
        
        :sets class variable next_day_chg_dict to {{'Lowchg':[float,float,...]},{'Highchg':[float,float,...]}}
        '''
               
        lowchg_list = []
        highchg_list = []
        
        for date in dates_of_matching_benchmark:
            next_date_index = stock_df.index.get_loc(stock_df.loc[((stock_df.index[stock_df['Date'] == date])+1)].index[0])
            next_date = stock_df.loc[next_date_index]['Date']
            
            candles_benchmark = get_candles_from_df(stock_df, next_date, period=2)
            pattern_benchmark = AnalyserEngine(candles_benchmark, period=1)

            for key in pattern_benchmark.fingerprint['lowchg']:
                lowchg_list.append(pattern_benchmark.fingerprint['lowchg'][key])
            
            for key in pattern_benchmark.fingerprint['highchg']:
                highchg_list.append(pattern_benchmark.fingerprint['highchg'][key])
        
        self.next_day_chg_dict = {'Lowchg': lowchg_list, 'Highchg': highchg_list}

if __name__ == '__main__':
    from stock_database_manager import get_stock_data_from_mongodb, get_candles_from_df
    from calculation_object import Parameters

    stock_df = get_stock_data_from_mongodb()
    print(f'{stock_df}\n')

    candles = get_candles_from_df(stock_df, date='2025-01-10', period=4)
    print(f'Candles:\n{candles}\n')

    pattern = AnalyserEngine(candles, period=3)
    print(f'Fingerprint:\n{pattern.fingerprint}\n')
    print(f'Indexes:\n{pattern.indexes}\n')
    print(f'Period:\n{pattern.period}\n')
    print(f'Date:\n{pattern.date}\n')

    candles_benchmark = get_candles_from_df(stock_df, date='2025-01-03', period=4)
    pattern_benchmark = AnalyserEngine(candles_benchmark, period=3)
    parameters = Parameters()
    comparison_data = pattern.generate_comparison_dict(pattern_benchmark, parameters.indicator_setup)
    
    print(f'Benchmark candles:\n{candles_benchmark}\n')
    print(f'Benchmark fingerprint:\n{pattern_benchmark.fingerprint}\n')
    print(f'Parameters:\n{parameters.indicator_setup}\n')
    print(f'Comparison:\n{comparison_data}\n')
    print(f'Check similarity:\n{AnalyserEngine.check_similarity(comparison_data, pattern_benchmark.indexes)}\n')

    # dates_of_matching_benchmark = {}
    # for index, row in stock_df.loc[22000:].iterrows():
    #     if pattern.date != row['Date']:

    #         benchmark_date = row['Date']
    #         candles_benchmark = get_candles_from_df(stock_df, benchmark_date, period=3)
    #         pattern_benchmark = AnalyserEngine(candles_benchmark, period=2)

    #         comparison_data = pattern.generate_comparison_dict(pattern_benchmark, tolerance=50)

    #         result = AnalyserEngine.check_similarity(comparison_data, pattern_benchmark.indexes)
    #         if result[1]:
    #             dates_of_matching_benchmark.update({result})
     
    # print(f'{dates_of_matching_benchmark}\n')

    # pattern.set_next_day_chg(stock_df, dates_of_matching_benchmark)

    # pattern.next_day_chg_dict = {'Lowchg': [1.002761470327116, 1.000041061493693, 1.0372261654256407, 0.9932368456496866, 0.9935887890282025], 'Highchg': [1.0020899694486982, 0.9929869651965559, 1.0239271700303225, 0.9910996187996407, 0.9951449353133529]}

    # print(pattern.next_day_chg_dict)

    # print(pattern.stats('median_Lowchg'))
    # print(pattern.stats('median_Highchg'))

