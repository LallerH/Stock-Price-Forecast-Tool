import yfinance as yf
import pandas as pd
import pandas_ta as ta

def download_from_yahoofin(ticker='^GSPC', period='1y', interval='1d', start=None, end=None) -> pd.DataFrame:
    """
    :Gets stock histroical data with yfinance library. (Note: this version handles only ^GSPC ticker and the interval of 1 day.)
    
    :Parameters:
        ticker : str (as of Yahoo Finance)
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
            Note (!): default is the date of the last closed data (T-1 day),
            current day isn't downloaded by default

        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
        start: str
            Download start date string (YYYY-MM-DD)
        end: str
            Download end date string (YYYY-MM-DD)

    :Returned DataFrame: 
        index: num
        values: 'Date' / YYYY-MM-DD, 'Open', 'High', 'Low' ,'Close', 'Volume'
    """
    from datetime import date
    
    if interval != '1d':
        raise Exception('Current version only handles interval of 1 day!')
    
    today = str(date.today())

    stock = yf.Ticker(ticker)
    if start == None:
        stock_df = stock.history(period=period, interval=interval)
    else:
        stock_df = stock.history(interval=interval, start=start, end=today)
    
    stock_df.index = stock_df.index.strftime('%Y-%m-%d')
    stock_df = stock_df.rename_axis('Date').reset_index()
    stock_df = stock_df.drop(['Dividends', 'Stock Splits'], axis=1)
    
    if stock_df.loc[len(stock_df)-1, 'Date'] == today:
        stock_df.drop(len(stock_df)-1, axis='index', inplace=True)

    return stock_df

def add_indicator(stock_df: pd.DataFrame, indicator='all') -> pd.DataFrame:
    """
    :Inserts indicators into pd.DataFrame as a new column.
    
    :Parameters:
        stock_df : pd.DataFrame (see structure at initial_download_from_yahoofin() function)
        indicator : str
            Valid indicators: rsi, macd, sma20, sma50, all ('all' inserts all valid indicators)    
    """
    valid_indicators = ('rsi', 'macd', 'sma20', 'sma50', 'all')
    if indicator not in valid_indicators:
        raise Exception(f'Indicator: {indicator} is not handled in the add_indicator() function!')

    def add_rsi(stock_df: pd.DataFrame):
        """
        :Inserts RSI (source: close price; length: 14 days) and RSI moving average (MA period: 9 days) indicators
        into arg. pd.DataFrame.
        """
        if len(stock_df) < 23:
            raise Exception('Not enough records! 14 records are required to calculate RSI and further 9 to moving average!')
        
        rsi_values = ta.rsi(stock_df['Close'])
        stock_df.insert(len(stock_df.columns), 'RSI', rsi_values)
        
        rsi_avg = []
        for i in range(22):
            rsi_avg.append(float('NaN'))
        
        for i in range(22,len(stock_df)):
            rsi_sum = 0
            for j in range((i-8),(i+1)):
                rsi_sum += stock_df.loc[j, 'RSI']
            rsi_avg.append(rsi_sum/9)
        
        stock_df.insert(len(stock_df.columns), 'RSIavg', rsi_avg)

        return stock_df

    def add_macd(stock_df: pd.DataFrame):
        """
        :Inserts MACD (source: close price; fast EMA period: 12 days; slow EMA period: 26 days; signal /MACD avg./ period: 9 days) 
        MACD histogram and MACD signal (EMA) indicators into arg. pd.DataFrame.
        """
        if len(stock_df) < 34:
            raise Exception('Not enough records! 26 records are required to calculate MACD and further 9 to moving average (MACD signal)!')
        
        macd_values = ta.macd(stock_df['Close'])
        stock_df = pd.concat([stock_df, macd_values], axis=1)
        stock_df.rename(columns = {'MACD_12_26_9':'MACD', 'MACDh_12_26_9':'MACDhist', 'MACDs_12_26_9':'MACDavg'}, inplace = True)        
        
        return stock_df

    def add_sma20(stock_df: pd.DataFrame):
        """
        :Inserts moving average (source: close price; period: 20 days) indicator into arg. pd.DataFrame.
        """
        if len(stock_df) < 20:
            raise Exception('Not enough records! 20 records are required to calculate 20 days moving average!')
        
        sma20_values = ta.sma(stock_df['Close'], length=20)
        stock_df.insert(len(stock_df.columns), 'SMA20', sma20_values)
        
        return stock_df

    def add_sma50(stock_df: pd.DataFrame):
        """
        :Inserts moving average (source: close price; period: 50 days) indicator into arg. pd.DataFrame.
        """
        if len(stock_df) < 50:
            raise Exception('Not enough records! 50 records are required to calculate 50 days moving average!')
        
        sma50_values = ta.sma(stock_df['Close'], length=50)
        stock_df.insert(len(stock_df.columns), 'SMA50', sma50_values)
        
        return stock_df

    if indicator == 'rsi':
        stock_df = add_rsi(stock_df)
    
    elif indicator == 'macd':
        stock_df = add_macd(stock_df)

    elif indicator == 'sma20':
        stock_df = add_sma20(stock_df)

    elif indicator == 'sma50':
        stock_df = add_sma50(stock_df)

    elif indicator == 'all':
        if len(stock_df) < 50:
            raise Exception('Not enough records! 50 records are required to calculate 50 days moving average!')
        
        stock_df = add_rsi(stock_df)
        stock_df = add_macd(stock_df)
        stock_df = add_sma20(stock_df)
        stock_df = add_sma50(stock_df)

    return stock_df

if __name__ == '__main__':
    stock_df = download_from_yahoofin(period='1y')
    stock_df = add_indicator(stock_df, indicator='all')
    print(f'{stock_df}\n')


