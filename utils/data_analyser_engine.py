import pandas as pd

if __name__ != '__main__':
    from .database_manager import get_candles_from_df

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
                'Lowchg' : {keys, values -> as of previuos / int}
            -> %change of OPEN data (T / T-1)
                'Openchg' : {keys, values -> as of previuos / int}
            -> %intraday change (CLOSE / OPEN)
                'Body' : {keys, values -> as of previuos / int}
            -> %change of HIGH data (T / T-1)
                'Highchg' : {keys, values -> as of previuos / int}
            -> color of candle / intraday change (CLOSE vs. OPEN)
                'Color' : {keys as of previuos, values: str -> 'green' if incr., 'red' if decr. , 'neutral' if unchg.}
            -> %change of RSIAVG data (T / T-1)
                'RSIavgchg' : {keys, values -> as of previuos / int}
            -> %change of MACDHIST data (T / T-1)
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
                  'Lowchg' : {},
                  'Openchg' : {},
                  'Body' : {},
                  'Highchg' : {},
                  'Color' : {},
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
                result['Color'].update({value : 'green'})
            elif self.candles['Close'][value] < self.candles['Open'][value]:
                result['Color'].update({value : 'red'})
            else:
                result['Color'].update({value : 'neutral'})
          
            result['Date'].update({value : self.candles['Date'][value]})
            result['Lowchg'].update({value : lowchg})
            result['Openchg'].update({value : openchg})
            result['Body'].update({value : body})
            result['Highchg'].update({value : highchg})
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

    def generate_comparison_dict(self, benchmark: "AnalyserEngine", tolerance=20)-> dict:
        '''
        :Compares the self.fingerprint dict with a benchmark fingerprint dict
        
        :Arguments:
            benchmark: instance of AnalyserEngine class on benchmark data/date
            tolerance: (int) percentage of tolerance range used in the search for similar historical data
        
        :Returns : dict
            -> with the same keys as of self.fingerprint dict
            -> values: TRUE if the benchmark is in the range of self.fingerprint value +/- tolerance range
                or self.fingerprint value == benchmark.fingerprint value in case of state keys (e.g.: color of candle)       
        '''
        tolerance = tolerance / 100
        result = {'Date' : {},
                  'Lowchg' : {},
                  'Openchg' : {},
                  'Body' : {},
                  'Highchg' : {},
                  'Color' : {},
                  'RSIavgchg' : {},
                  'RSIstate' : '',
                  'MACDhistchg' : {},
                  'MACDrange' : '',
                  'SMA20chg' : {},
                  'SMA50chg' : {},
                  'SMA20_50relation' : ''
                  }
        
        list_of_numeric_keys = ('Lowchg', 'Openchg', 'Body', 'Highchg',
                                'RSIavgchg', 'MACDhistchg')
        list_of_numeric_sensible_keys = ('SMA20chg', 'SMA50chg')
        
        for idx, value in list(enumerate(self.indexes))[1:]:
            result['Date'].update({(benchmark.indexes[idx]) : benchmark.candles['Date'][(benchmark.indexes[idx])]})
            
            if self.fingerprint['Color'][value] == benchmark.fingerprint['Color'][(benchmark.indexes[idx])]:
                result['Color'].update({(benchmark.indexes[idx]) : True})
            else:
                result['Color'].update({(benchmark.indexes[idx]) : False})
            
            if self.fingerprint['Color'][value] == 'neutral' or benchmark.fingerprint['Color'][(benchmark.indexes[idx])] == 'neutral':
                result['Color'].update({(benchmark.indexes[idx]) : True})

            for key in list_of_numeric_keys:
                benchmark_value = benchmark.fingerprint[key][(benchmark.indexes[idx])]
                self_value = self.fingerprint[key][value]
                
                if benchmark_value > 1.005:
                    if (self_value < (benchmark_value + (benchmark_value - 1) * tolerance)) and\
                       (self_value > (benchmark_value - (benchmark_value - 1) * tolerance)):
                        result[key].update({(benchmark.indexes[idx]) : True})
                    else:
                        result[key].update({(benchmark.indexes[idx]) : False})
                elif benchmark.fingerprint[key][(benchmark.indexes[idx])] >= 0.995:
                    if (self_value < (benchmark_value + tolerance/200)) and\
                       (self_value > (benchmark_value - tolerance/200)):
                        result[key].update({(benchmark.indexes[idx]) : True})
                    else:
                        result[key].update({(benchmark.indexes[idx]) : False})
                else:
                    if (self_value < (benchmark_value + (1 - benchmark_value) * tolerance)) and\
                       (self_value > (benchmark_value - (1 - benchmark_value) * tolerance)):
                        result[key].update({(benchmark.indexes[idx]) : True})
                    else:
                        result[key].update({(benchmark.indexes[idx]) : False})

            for key in list_of_numeric_sensible_keys:
                benchmark_value = benchmark.fingerprint[key][(benchmark.indexes[idx])]
                self_value = self.fingerprint[key][value]
                
                if (self_value < (benchmark_value + tolerance/2000)) and (self_value > (benchmark_value - tolerance/2000)):
                    result[key].update({(benchmark.indexes[idx]) : True})
                else:
                    result[key].update({(benchmark.indexes[idx]) : False})
                if (benchmark_value > 1 and self_value < 1) or (benchmark_value < 1 and self_value > 1):
                    result[key].update({(benchmark.indexes[idx]) : False})

        if self.fingerprint['RSIstate'] == benchmark.fingerprint['RSIstate']:
            result.update({'RSIstate' : True})
        else:
            result.update({'RSIstate' : False})

        if self.fingerprint['MACDrange'] == benchmark.fingerprint['MACDrange']:
            result.update({'MACDrange' : True})
        else:
            result.update({'MACDrange' : False})
        
        if self.fingerprint['SMA20_50relation'] == benchmark.fingerprint['SMA20_50relation']:
            result.update({'SMA20_50relation' : True})
        else:
            result.update({'SMA20_50relation' : False})

        return result

    def stats(self, indicator: str) -> int:
        '''
        '''
        import matplotlib.cbook as cbk
        import numpy as np
        # ha üres a self.next_day_chg_dict hibakezelés
        
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
        
        Note that this method is still in testing phase, the key indicators is needed to be identified
        1) to get convenient similar (quality) data 
        2) to get enough data (quantity) for the further statistical methods
        '''
        parameters = {'Lowchg' : bool,
                    #   'Openchg' : bool,
                    #   'Body' : bool,
                      'Highchg' : bool,
                    #   'Color' : bool,
                      'RSIavgchg' : bool,
                      'RSIstate' : bool,
                    #   'MACDhistchg' : bool,
                      'MACDrange' : bool,
                    #   'SMA20chg' : bool,
                    #   'SMA50chg' : bool,
                    #   'SMA20_50relation' : bool
                  }
        list_of_multiplevalue_keys = ('Lowchg', 'Highchg', 'RSIavgchg')#', Openchg', 'Body')
                                      #,'MACDhistchg' ,'SMA20chg', 'SMA50chg')
        list_of_singlevalue_keys = ('RSIstate', 'MACDrange')#, 'SMA20_50relation')
        list_of_strict_keys = ()#'Color')

        for key in comparison_dict:
            if key in list_of_singlevalue_keys:
                parameters.update({key: comparison_dict[key]})
            elif key in list_of_strict_keys:
                parameters.update({key: True})
                for index in comparison_dict[key]:
                    if comparison_dict[key][index] == False:
                        parameters.update({key: False})
            elif key in list_of_multiplevalue_keys:
                parameters.update({key: True})
                for index in comparison_dict[key]:
                    if comparison_dict[key][index] == False:
                        parameters.update({key: False})
        
        result = True
        for key in parameters:
            if parameters[key] == False:
                result = False

        return comparison_dict['Date'][indexes[len(indexes)-1]], result

    def get_next_day_chg(self, stock_df: pd.DataFrame, dates_of_matching_benchmark: dict):
        '''
        :Calculates change of open/close price on following day of matching(similar) benchmark data
        
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

            for key in pattern_benchmark.fingerprint['Lowchg']:
                lowchg_list.append(pattern_benchmark.fingerprint['Lowchg'][key])
            
            for key in pattern_benchmark.fingerprint['Highchg']:
                highchg_list.append(pattern_benchmark.fingerprint['Highchg'][key])
        
        self.next_day_chg_dict = {'Lowchg': lowchg_list, 'Highchg': highchg_list}

if __name__ == '__main__':
    from database_manager import get_data_from_mongodb, get_candles_from_df

    stock_df = get_data_from_mongodb()
    print(f'{stock_df}\n')

    candles = get_candles_from_df(stock_df, date='2024-05-30', period=3)
    print(f'Candles:\n{candles}\n')

    pattern = AnalyserEngine(candles, period=3)
    print(f'Fingerprint:\n{pattern.fingerprint}\n')

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

    # pattern.get_next_day_chg(stock_df, dates_of_matching_benchmark)

    pattern.next_day_chg_dict = {'Lowchg': [1.002761470327116, 1.000041061493693, 1.0372261654256407, 0.9932368456496866, 0.9935887890282025], 'Highchg': [1.0020899694486982, 0.9929869651965559, 1.0239271700303225, 0.9910996187996407, 0.9951449353133529]}

    print(pattern.next_day_chg_dict)

    print(pattern.stats('median_Lowchg'))
    print(pattern.stats('median_Highchg'))

