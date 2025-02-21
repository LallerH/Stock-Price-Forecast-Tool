from pymongo import MongoClient
import pandas as pd

def check_stock_database_in_mongodb(client = "mongodb://localhost:27017", database = 'Stock_data') -> bool:
    """
    :Check the existence of mongodb database
    
    :Parameters:
        client : MongoDB client
        database : MongoDB database
    :Returns:
        True : if database exists
        False : if database not exists
    """
    mongodb_client = MongoClient(f'{client}')
    if database not in mongodb_client.list_database_names():
        return False

    return True

def initial_upload_of_stock_database(client = "mongodb://localhost:27017", database = 'Stock_data'):
    from .data_downloader import download_from_yahoofin, add_indicator
    """
    :Creates Stock_data database and uploads ^GSPC, ^GDAXI, GOOGL data
    
    :Parameters:
        client : MongoDB client
        database : MongoDB database
    """
    mongodb_client = MongoClient(f'{client}')
    database = mongodb_client[database]
    
    tickers = ('^GSPC','^GDAXI','GOOGL')
    for item in tickers:
        stock_df = download_from_yahoofin(ticker=item, period='max')
        stock_df = add_indicator(stock_df, indicator='all')
        write_stock_data_to_mongodb(stock_df, coll=item)

def download_new_stock_data(ticker, client = "mongodb://localhost:27017", database = 'Stock_data'):
    from .data_downloader import download_from_yahoofin, add_indicator
    
    mongodb_client = MongoClient(f'{client}')
    database = mongodb_client[database]
    
    stock_df = download_from_yahoofin(ticker=ticker, period='max')
    stock_df = add_indicator(stock_df, indicator='all')
    write_stock_data_to_mongodb(stock_df, coll=ticker)

def check_stock_data_in_mongodb(client = "mongodb://localhost:27017", database = 'Stock_data', coll = '^GSPC') -> bool:
    """
    :Check the existence of mongodb database/collection
    
    :Parameters:
        client : MongoDB client
        database : MongoDB database
        coll : MongoDB collection
    :Returns:
        False : if collection not exists or no data in it
        True, date 'YYYY-MM-DD' : if collection and data exists, last record 'Date' data
    """
    mongodb_client = MongoClient(f'{client}')
    if database not in mongodb_client.list_database_names():
        return False, False
    
    mongodb_database = mongodb_client[f'{database}']
    if coll not in mongodb_database.list_collection_names():
        return False, False

    mongodb_coll = mongodb_database[f'{coll}']
    cursor = mongodb_coll.find().sort({'Date':-1})
    return True, cursor.next()['Date']

def get_stock_collections_from_mongodb(client = "mongodb://localhost:27017", database = 'Stock_data') -> list:
    """
    :Returns the existing collections in MongoDB
    
    :Parameters:
        client : MongoDB client
        database : MongoDB database
    :Returns:
        False: if database doesn't exist
        [list] - existing collections (in practice: the name of tickers with existing data)
    """
    mongodb_client = MongoClient(f'{client}')
    if database not in mongodb_client.list_database_names():
        return False
    
    mongodb_database = mongodb_client[f'{database}']
    return mongodb_database.list_collection_names()

def write_stock_data_to_mongodb(stock_df: pd.DataFrame, client = "mongodb://localhost:27017", database = 'Stock_data',
                          coll = '^GSPC', replace = True):
    """
    :Writes data to MongoDB (overwrite or append).
    
    :Parameters:
        DataFrame
        client : MongoDB client
        database : MongoDB database
        coll : MongoDB collection
        replace : bool
            True: existing collection is dropped and replaced
            False: existing collection is appended with the new data (existing data is not replaced)   
    """   
    mongodb_client = MongoClient(f'{client}')
    mongodb_database = mongodb_client[f'{database}']
    mongodb_coll = mongodb_database[f'{coll}']
    
    stock_df_dict = stock_df.to_dict('records')

    if replace:
        mongodb_coll.drop()
        mongodb_coll.insert_many(stock_df_dict)
    else:
        for item in stock_df_dict:
            cursor = mongodb_coll.find({'Date':item['Date']})
            if len(list(cursor)) == 0:
                mongodb_coll.insert_one(item)

def get_first_correct_date(client = "mongodb://localhost:27017", database = 'Stock_data', coll = '^GSPC') -> list:
    """
    :Checks the database and returns the first correct index (and date / YYYY-MM-DD) downloaded from Yahoo Finance.
    
    :Parameters:
        client : MongoDB client
        database : MongoDB database
        coll : MongoDB collection

    :Returns (index - int, 'yyyy-MM-dd' - str) / False if no available data
    """   
    mongodb_client = MongoClient(f'{client}')
    mongodb_database = mongodb_client[f'{database}']
    mongodb_coll = mongodb_database[f'{coll}']
    cursor = mongodb_coll.find()
    for index, item in enumerate(cursor):
        if item['Open'] != 0 and item['Open'] != item['High'] and item['Open'] != item['Low'] and item['Open'] != item['Close']:
            return index, item['Date']
    return False

def get_stock_data_from_mongodb(client = "mongodb://localhost:27017", database = 'Stock_data', coll = '^GSPC', range = 'all') -> pd.DataFrame:
    """
    :Loads all data from MongoDB collection.
    
    :Parameters:
        client : MongoDB client
        database : MongoDB database
        coll : MongoDB collection
        range :
            'all' -> all data
            'last' -> last data (gets 51 as a maximum)
    """   
    mongodb_client = MongoClient(f'{client}')
    mongodb_database = mongodb_client[f'{database}']
    mongodb_coll = mongodb_database[f'{coll}']
    
    if range == 'all' or (range == 'last' and mongodb_coll.count_documents({}) <= 50):
        cursor = mongodb_coll.find()
        stock_df = pd.DataFrame(list(cursor))
        stock_df = stock_df.sort_values(by='Date', ascending=True)
        stock_df = stock_df.drop(['_id'], axis=1)
    
    elif range == 'last' and mongodb_coll.count_documents({}) > 50:
        cursor = mongodb_coll.find().sort({'Date':-1}).limit(51)
        stock_df = pd.DataFrame(list(cursor)[1:])
        stock_df = stock_df.sort_values(by='Date', ascending=True)
        stock_df = stock_df.drop(['_id', 'RSI', 'RSIavg', 'MACD', 'MACDhist','MACDavg',\
                                  'SMA20', 'SMA50'], axis=1)
    return stock_df

def get_candles_from_df(stock_df: pd.DataFrame, date=None, period=4) -> dict:
    """
    :Gets stock data from pd.DataFrame.
    
    :Parameters:
        stock_df : pd.Dataframe (provided by get_data_from_mongodb or data_downloader module /with all indicators/)
        date : str / YYYY-MM-DD (if None: last day of pd.DataFrame)
        period : number of candles (must be 1 one candle more than the fingerprint period)
    
    :Returns: {dict{dict}} stock data from DataFrame of data_downloader module with all indicators
        {keys -> keys of DataFrame, values -> {keys -> indexes of Dataframe, values: stock data}} 
    """
    if date == None:
        idx = len(stock_df)
        candles = stock_df.iloc[(idx-period):idx].to_dict('dict')
        return candles

    if date not in stock_df['Date'].values:
        # raise Exception(f'No data for date: {date}!')
        return False
    
    date_idx = stock_df[stock_df['Date'] == date].index.item()
    
    if date_idx < period:
        raise Exception(f'Not enough anterior data for date: {date} for fingerprint period: {period}!')
   
    if date_idx < 49:
        raise Exception(f'Not enough anterior data for date: {date} to calculate all fingerprint elements'\
                        ' (min: 50 to calcluate SAM50!')
    
    candles = stock_df.iloc[(date_idx-(period-1)):(date_idx+1)].to_dict('dict')
    return candles

def get_index_from_df(stock_df: pd.DataFrame, date: str) -> int:
    """
    :Gets index from pd.DataFrame for a certain date
    
    :Parameters:
        stock_df : pd.Dataframe (provided by get_data_from_mongodb or data_downloader module /with all indicators/)
        date : str / YYYY-MM-DD (if None: last day of pd.DataFrame)
    
    :Returns: int
    """
    if date not in stock_df['Date'].values:
        raise Exception(f'No data for date: {date}!')
    
    return stock_df[stock_df['Date'] == date].index.item()  

if __name__ == "__main__":
    # print(check_data_in_mongodb())
    
    # print(get_collections_from_mongodb())

    # stock_df = get_data_from_mongodb()
    # print(f'\n{stock_df}')  
    
    # candles = get_candles_from_df(stock_df)
    # print(f'\n{candles}')
    # idx = get_index_from_df(stock_df, '2024-05-29')
    # print(stock_df['Date'][idx+1])

    print(get_first_correct_date())
