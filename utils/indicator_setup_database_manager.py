from pymongo import MongoClient

def check_indicator_setup_database(client = "mongodb://localhost:27017", database = 'Indicator_setup') -> bool:
    """
    :Check the existence of mongodb Indicator_setup database
    
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

def initialize_indicator_setup_database(client = "mongodb://localhost:27017", database = 'Indicator_setup'):
    """
    :Creates a database in MongoDB and uploads the Basic indicator setup
    
    :Parameters:
        client : MongoDB client
        database : MongoDB database
    """
    setup = {
        'name' : 'Base setup',
        'days' : 2,
        'lowchg' : {'selected' : True, 'tolerance': 80},
        'openchg' : {'selected' : True, 'tolerance': 80},
        'highchg' : {'selected' : True, 'tolerance': 80},
        'body' : {'selected' : True, 'tolerance': 80},
        'color' : {'selected' : True, 'tolerance': False},
        'RSIavgchg' : {'selected' : False, 'tolerance': 100},
        'RSIstate' : {'selected' : False, 'tolerance': False},
        'MACDhistchg' : {'selected' : True, 'tolerance': 9},
        'MACDrange' : {'selected' : False, 'tolerance': False},
        'SMA20chg' : {'selected' : False, 'tolerance': 5},
        'SMA50chg' : {'selected' : False, 'tolerance': 4},
        'SMA20_50relation' : {'selected' : False, 'tolerance': False}
    }

    mongodb_client = MongoClient(f'{client}')
    mongodb_database = mongodb_client[f'{database}']
    mongodb_coll = mongodb_database[f'{setup["name"]}']    
    mongodb_coll.insert_one(setup)

def get_indicator_setups_from_mongodb(client = "mongodb://localhost:27017", database = 'Indicator_setup') -> list:
    """
    :Returns the list of indicator setups saved in database. (False if database not in client.)
    
    :Parameters:
        client : MongoDB client
        database : MongoDB database
    """
    mongodb_client = MongoClient(f'{client}')
    if database not in mongodb_client.list_database_names():
        return False
    
    mongodb_database = mongodb_client[f'{database}']
    return mongodb_database.list_collection_names()

def write_indicator_setup(setup: dict, client = "mongodb://localhost:27017", database = 'Indicator_setup'):
    """
    :Inserts one indicator setup to database.
    
    :Parameters:
        setup : dict / structure see at definition -> initialize_indicator_setup_database
        client : MongoDB client
        database : MongoDB database
    """

    mongodb_client = MongoClient(f'{client}')
    mongodb_database = mongodb_client[f'{database}']
    mongodb_coll = mongodb_database[f'{setup["name"]}']    
    mongodb_coll.insert_one(setup)

def load_indicator_setup(setup_name: str, client = "mongodb://localhost:27017", database = 'Indicator_setup') -> dict:
    """
    :Loads a specific indicator setup from database.
    
    :Parameters:
        setup_name : str
        client : MongoDB client
        database : MongoDB database
    """
    mongodb_client = MongoClient(client)
    mongodb_database = mongodb_client[database]
    mongodb_coll = mongodb_database[setup_name]    
    setup = list(mongodb_coll.find())
    setup[0].pop('_id')
    return setup[0]

def delete_indicator_setup(setup_name: str, client = "mongodb://localhost:27017", database = 'Indicator_setup'):
    """
    :Deletes one indicator setup in database.
    
    :Parameters:
        setup_name : str
        client : MongoDB client
        database : MongoDB database
    """

    mongodb_client = MongoClient(client)
    mongodb_database = mongodb_client[database]
    mongodb_coll = mongodb_database[setup_name]    
    mongodb_database.drop_collection(mongodb_coll)
    
if __name__ == "__main__":
    if check_indicator_setup_database() == False:
        initialize_indicator_setup_database()
    else:
        print('DB already exists!')
    
    load_indicator_setup('Base setup')
