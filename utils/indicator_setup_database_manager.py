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
        'days' : 3,
        'lowchg' : {'selected' : True, 'tolerance': 100},
        'openchg' : {'selected' : False, 'tolerance': 100},
        'highchg' : {'selected' : True, 'tolerance': 100},
        'body' : {'selected' : False, 'tolerance': 100},
        'color' : {'selected' : False, 'tolerance': False},
        'RSIavgchg' : {'selected' : True, 'tolerance': 100},
        'RSIstate' : {'selected' : True, 'tolerance': False},
        'MACDhistchg' : {'selected' : False, 'tolerance': 100},
        'MACDrange' : {'selected' : True, 'tolerance': False},
        'SMA20chg' : {'selected' : False, 'tolerance': 100},
        'SMA50chg' : {'selected' : False, 'tolerance': 100},
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

if __name__ == "__main__":
    if check_indicator_setup_database() == False:
        initialize_indicator_setup_database()
    else:
        print('DB already exists!')
    
    load_indicator_setup('Base setup')
