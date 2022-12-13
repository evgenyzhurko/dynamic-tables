from typing import Union
from fastapi import FastAPI, Path, Request, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId

from flowlang import Flow

CONFIG_DB_NAME = 'configuration'
DATA_DB_NAME = 'data'

def get_client():
    return MongoClient('mongodb://root:example@mongo:27017/')

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def filter_query_params(params: dict):
    if '_id' in params:
        params['_id'] = ObjectId(params['_id'])
    return dict(filter(lambda item: item[0] != 'limit' and item[0] != 'skip', params.items()))

def transform_id(data):
    data['_id'] = str(data['_id'])
    return data


def get_collection_curson(db, collection, params):
    return get_client()[db][collection].find(params)

def get_collection_size(db, collection, params):
    return get_client()[db][collection].count_documents(params)

def get_collection_curson_with_params(db, collection, params, skip, limit):
    return get_client()[db][collection].find(params).skip(skip).limit(limit)

def get_collection_to_json_with_params(db, collection, params, skip, limit):
    documents = list(map(transform_id, get_collection_curson_with_params(db, collection, params, skip, limit)))
    return { 'result': documents}

def delete_object_in_collection(db, collection, params):
    get_client()[db][collection].delete_one(params)

def drop_collections(db):
    for collection in db.list_collection_names():
        db[collection].drop()



@ app.post('/v1/reset', status_code=status.HTTP_200_OK)
async def initialize_configuration():
    client = get_client()
    drop_collections(client[CONFIG_DB_NAME])
    drop_collections(client[DATA_DB_NAME])

@ app.post('/v1/configuration/{collection_name}', status_code=status.HTTP_201_CREATED)
async def create_configuration_object(
        collection_name,
        document: Request):
    data = await document.json()
    collection = get_client()[CONFIG_DB_NAME][collection_name]
    collection.insert_one(data)
    return {}

@ app.get('/v1/configuration/{collection_name}')
async def get_configuration_objects(
        collection_name,
        request: Request, 
        skip: int = Query(default=0, gt=0), 
        limit: int = Query(default=10, gt=0)):
    params = filter_query_params(dict(request.query_params))
    return get_collection_to_json_with_params(CONFIG_DB_NAME, collection_name, params, skip, limit)


@app.delete('/v1/configuration/{collection_name}')
async def delete_configuration_object(
        collection_name,
        request: Request):
    params = filter_query_params(dict(request.query_params))
    return delete_object_in_collection(CONFIG_DB_NAME, collection_name, params)


@ app.get('/v1/configuration/{collection_name}/count')
async def get_configuration_objects_count(
        collection_name,
        request: Request):
    params = filter_query_params(dict(request.query_params))
    return { 'result': get_collection_size(CONFIG_DB_NAME, collection_name, params) }


@ app.post('/v1/data/{collection_name}', status_code=status.HTTP_201_CREATED)
async def create_data_object(
        document: Request,
        collection_name):
    data = await document.json()
    collection = get_client()[DATA_DB_NAME][collection_name]
    collection.insert_one(data)
    return {}

@ app.get('/v1/data/{collection_name}/count')
async def get_data_objects_count(
        collection_name,
        request: Request):
    params = filter_query_params(dict(request.query_params))
    return { 'result': get_collection_size(DATA_DB_NAME, collection_name, params) }

@ app.get('/v1/data/{collection_name}')
async def get_data_objects(
        collection_name,
        request: Request, 
        skip: int = 0,
        limit: int = 10):
    params = filter_query_params(dict(request.query_params))
    return get_collection_to_json_with_params(DATA_DB_NAME, collection_name, params, skip, limit)

@app.delete('/v1/data/{collection_name}')
async def delete_data_object(
        collection_name,
        request: Request):
    params = filter_query_params(dict(request.query_params))
    return delete_object_in_collection(DATA_DB_NAME, collection_name, params)

@ app.post('/v1/data/{collection_name}/{document_id}/{action_id}', status_code=status.HTTP_200_OK)
async def execute_action(
    collection_name,
    document_id,
    action_id
):
    client = get_client()
    action = list(get_client()[CONFIG_DB_NAME]['actions'].find({"_id": ObjectId(action_id)}))[0]
    flow = Flow()
    flow.from_json(action['code'])
    result = flow(
        db= client[DATA_DB_NAME],
        collection= client[DATA_DB_NAME][collection_name],
        document= list(get_client()[DATA_DB_NAME][collection_name].find({"_id": ObjectId(document_id)}))[0]
    )
    return { 'result': result }