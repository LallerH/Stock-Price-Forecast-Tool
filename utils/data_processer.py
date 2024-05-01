
class AnalyserEngine:

    def __init__(self, candles: dict, period=3, tolerance=10):
        '''
    :Processing of data:
        - generate fingerprint for data of a certain date
        - searching for historical data having the same fingerprint
        - make projection based on historical data with the same fingerprint
    
    :Parameters: ()
        candles : {dict{dict}} stock data from DataFrame of data_supply module with all indicators
            {keys -> keys of DataFrame, values -> {keys -> indexes of Dataframe, values: stock data}} 
        period : int
            valid period: no longer than (len(candles)-1)
        tolerance: int
            percentage of tolerance range used in the search for similar historical data
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
        self.tolerance = tolerance

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
            -> %inraday change (CLOSE / OPEN)
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
                color = 'green'
            elif self.candles['Close'][value] < self.candles['Open'][value]:
                color = 'red'
            else:
                color = 'neutral'
          
            result['Date'].update({value : self.candles['Date'][value]})
            result['Lowchg'].update({value : lowchg})
            result['Openchg'].update({value : openchg})
            result['Body'].update({value : body})
            result['Highchg'].update({value : highchg})
            result['Color'].update({value : color})
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

    def matched_periods(self)-> list:
        '''
        '''
        ...
    
    def projection(self)-> dict:
        '''
        '''
        ...

if __name__ == '__main__':
    from database_manager import get_data_from_mongodb
    import pandas as pd

    stock_df = get_data_from_mongodb()
    # print(f'{stock_df}\n')

    candles = stock_df.iloc[(len(stock_df)-4):(len(stock_df))].to_dict('dict') # !!! a function in data_supply module is required
    print(f'Candles:\n{candles}')

    pattern = AnalyserEngine(candles)
    print(f'Fingerprint:\n{pattern.fingerprint()}')
    