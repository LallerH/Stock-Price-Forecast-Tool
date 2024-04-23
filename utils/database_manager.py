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

if __name__ == "__main__":
    test_dict = {
        '1' : [30_000, 'red', 'metal'],
        '2' : [40_000, 'blue', 'plastic']
        }

    test_df = pd.DataFrame.from_dict(test_dict, orient='index', columns=['price','color','material'])
    print(test_df)
    write_data_to_mongodb(test_df)

    stock_df = get_data_from_mongodb()
    print(f'\n{stock_df}')
