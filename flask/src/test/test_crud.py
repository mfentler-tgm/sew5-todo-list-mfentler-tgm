import pytest
import json
from server.server import app
from server.server import db,Task
from server.server import initUserDb,initTaskDb
from flask_httpauth import HTTPBasicAuth
import base64

valid_credentials = base64.b64encode(b'admin:1234').decode('utf-8')

@pytest.fixture
def client():

    client = app.test_client()

    initTaskDb()
    initUserDb()

    yield client

    allTasks = client.get('/', headers={'Authorization': 'Basic '+valid_credentials})
    for task in allTasks.json:
        client.delete('/'+str(task['id']), headers={'Authorization': 'Basic '+valid_credentials})


def test_post(client):
    payload = {'name':'post task','description':'added through testing'}
    response = client.post('/', json=payload, headers={'Authorization': 'Basic '+valid_credentials})

    assert 'post task' in response.json['name']

def test_getAll(client):
    response = client.get('/', headers={'Authorization': 'Basic '+valid_credentials})
    for task in response.json:
       assert 'testTask' in task['name']

def test_getOne(client):
    response = client.get('/1', headers={'Authorization': 'Basic '+valid_credentials})

    assert 'testTask' in response.json['name']

def test_put(client):
    response = client.get('/1', headers={'Authorization': 'Basic '+valid_credentials})
    response.json['name'] = 'new name'
    putResponse = client.put('/1', json=response.json, headers={'Authorization': 'Basic '+valid_credentials})

    assert 'new name' in putResponse.json['name']

def test_delete(client):
    client.delete('/1', headers={'Authorization': 'Basic '+valid_credentials})
    response = client.get('/', headers={'Authorization': 'Basic '+valid_credentials})

    assert response.json == []