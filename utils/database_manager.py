from pymongo import MongoClient
import pandas as pd

def write_data_to_mongodb(stock_df: pd.DataFrame, client = "mongodb://localhost:27017", database = 'Stock_data',
                          coll = '^GSPC', replaced = True):
    """
    :Writes data to MongoDB (overwrite or append).
    
    :Parameters:
        DataFrame
        client : MongoDB client
        database : MongoDB database
        coll : MongoDB collection
        replace : bool
            True: existing collection is dropped and replaced
            False: existing collection is appended with the new data (only available if data is directly before or after the existing period)   
    """   
    mongodb_client = MongoClient(f'{client}')
    mongodb_database = mongodb_client[f'{database}']
    mongodb_coll = mongodb_database[f'{coll}']
    
    if replaced:
        mongodb_coll.drop()
    else:
        ...

    stock_df_dict = stock_df.to_dict('records')
    mongodb_coll.insert_many(stock_df_dict)

def get_data_from_mongodb(client = "mongodb://localhost:27017", database = 'Stock_data', coll = '^GSPC') -> pd.DataFrame:
    """
    :Loads all data from MongoDB collection.
    
    :Parameters:
        client : MongoDB client
        database : MongoDB database
        coll : MongoDB collection    
    """   
    mongodb_client = MongoClient(f'{client}')
    mongodb_database = mongodb_client[f'{database}']
    mongodb_coll = mongodb_database[f'{coll}']
    
    cursor = mongodb_coll.find()
    stock_df = pd.DataFrame(list(cursor))
    stock_df = stock_df.drop(['_id'], axis=1)

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
        raise Exception(f'No data for date: {date}!')
    
    date_idx = stock_df[stock_df['Date'] == date].index.item()
    
    if date_idx < period:
        raise Exception(f'Not enough anterior data for date: {date} for fingerprint period: {period}!')
   
    if date_idx < 49:
        raise Exception(f'Not enough anterior data for date: {date} to calculate all fingerprint elements'\
                        ' (min: 50 to calcluate SAM50!')
    
    candles = stock_df.iloc[(date_idx-(period-1)):(date_idx+1)].to_dict('dict')
    return candles

if __name__ == "__main__":
    stock_df = get_data_from_mongodb()
    print(f'\n{stock_df}')  
    candles = get_candles_from_df(stock_df)
    print(f'\n{candles}')

   