import unittest
from fastapi.testclient import TestClient
from pymongo import MongoClient


from main import app, CONFIG_DB_NAME, DATA_DB_NAME, drop_collections


def get_client():
    return MongoClient('mongodb://root:example@127.0.0.1:27017/')

def make_mock_db():
    # make configuration
    # fill with mock data
    drop_collections(get_client()[CONFIG_DB_NAME])
    drop_collections(get_client()[DATA_DB_NAME])

    config_collection = get_client()[CONFIG_DB_NAME].get_collection('collections')
    config_collection.insert_many([
        {
            'name': 'Products', 
            'params': [ 
                { 'name': 'name', 'type': 'String' },
                { 'name': 'description', 'type': 'String' },
            ]
        },
        {
            'name': 'Orders', 
            'params': [ 
                { 'name': 'product', 'type': 'Ref<Products>' },
                { 'name': 'count', 'type': 'int64' },
            ]
        }
    ])

    products_collection = get_client()[DATA_DB_NAME].get_collection('Products')
    inserted_products = products_collection.insert_many([
        { 'name': 'A', 'description': 'a' },
        { 'name': 'B', 'description': 'b' },
        { 'name': 'C', 'description': 'c' },
        { 'name': 'D', 'description': 'd' },
        { 'name': 'E', 'description': 'e' },
        { 'name': 'F', 'description': 'f' },
        { 'name': 'G', 'description': 'g' },
        { 'name': 'H', 'description': 'h' }
    ]).inserted_ids
    orders_collection = get_client()[DATA_DB_NAME].get_collection('Orders')
    inserted_orders = orders_collection.insert_many([
        { 'count': 1, 'product': str(inserted_products[0]) },
        { 'count': 2, 'product': str(inserted_products[1]) },
        { 'count': 3, 'product': str(inserted_products[2]) },
        { 'count': 4, 'product': str(inserted_products[3]) },
        { 'count': 5, 'product': str(inserted_products[5]) },
    ])


class BaseBackendTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        make_mock_db()

    def test_home_not_exists(self):
        response = self.client.get('/v1/')
        self.assertEqual(response.status_code, 404)

    def test_initialization(self):
        response = self.client.post('/v1/reset')
        self.assertEqual(response.status_code, 200)

    def test_get_collections_configuration(self):
        response = self.client.get('/v1/configuration/collections')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(collections), 2)

    def test_get_collections_configuration_with_limit(self):
        response = self.client.get('/v1/configuration/collections?limit=1')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(collections), 1)

    def test_get_collections_configuration_with_limit2(self):
        response = self.client.get('/v1/configuration/collections?limit=0')
        self.assertEqual(response.status_code, 422)

    def test_get_collections_configuration_with_skip(self):
        response = self.client.get('/v1/configuration/collections?skip=1')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(collections), 1)

    def test_get_collections_configuration_with_skip2(self):
        response = self.client.get('/v1/configuration/collections?skip=2')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(collections), 0)

    def test_get_collection_by_name2(self):
        response = self.client.get('/v1/configuration/collections?name=Products')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(collections), 1)

    def test_make_collection(self):
        response = self.client.post('/v1/configuration/collections', json={
            'name': 'Stock', 
            'params': [ 
                { 'name': 'product', 'type': 'Ref<Products>' },
                { 'name': 'count', 'type': 'int64' },
            ]
        })
        self.assertEqual(response.status_code, 201)

    def test_get_collection_count(self):
        response = self.client.get('/v1/configuration/collections/count')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(collections, 2)

    def test_make_data(self):
        response = self.client.post('/v1/data/Products', json={
            'name': 'X',
            'description': 'x'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_data_from_collection(self):
        response = self.client.get('/v1/data/Products')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(collections), 1)

    def test_get_data_from_collection_query(self):
        response = self.client.get('/v1/data/Products?skip=1&limit=1')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(collections), 1)


    def test_get_data_object_by_id(self):
        response = self.client.get('/v1/data/Products?skip=5&limit=1')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(collections), 1)

        response = self.client.get(f'/v1/data/Products?_id={collections[0]["_id"]}')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(collections), 1)

    
    def test_get_data_collection_count(self):
        response = self.client.get('/v1/data/Products/count')
        collections = response.json()['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(collections, 8)

    def test_execute_action(self):
        response = self.client.post('/v1/data/a/a/a')
        self.assertEqual(response.status_code, 200)