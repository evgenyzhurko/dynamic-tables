import sys
import json
from tests.base_test import *
from pymongo import MongoClient

from main import DATA_DB_NAME, CONFIG_DB_NAME, drop_collections

def get_client():
    return MongoClient('mongodb://root:example@127.0.0.1:27017/')

def setup_mock_db():
    client = get_client()
    drop_collections(client[DATA_DB_NAME])
    drop_collections(client[CONFIG_DB_NAME])
    
    with open('tests/setup.json') as f:
        data = json.load(f)
        client[CONFIG_DB_NAME]['collections'].insert_many(
            data['config']
        )
        for collection in data['data']:
            client[DATA_DB_NAME][collection].insert_many(
                data['data'][collection]
            )


if __name__ == '__main__':
    if 'setup' in sys.argv:
        setup_mock_db()
    else:
        unittest.main()