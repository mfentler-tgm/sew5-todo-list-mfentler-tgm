import pytest
import json
from server.server import app
from server.server import db,Task

@pytest.fixture
def client():
    client = app.test_client()

    t = Task('test task', 'for pytesting')
    db.create_all()
    db.session.add(t)
    db.session.commit()

    yield client

    allTasks = client.get('/').json
    for task in allTasks:
        client.delete('/'+str(task['id']))


def test_post(client):
    payload = {'name':'post task','description':'added through testing'}
    response = client.post('/', json=payload)
    assert 'post task' in response.json['name']

def test_getAll(client):
    response = client.get('/')
    for task in response.json:
       assert 'test task' in task['name']

def test_getOne(client):
    response = client.get('/1')
    assert 'test task' in response.json['name']

def test_put(client):
    response = client.get('/1')
    response.json['name'] = 'new name'
    putResponse = client.put('/1', json=response.json)
    assert 'new name' in putResponse.json['name']

def test_delete(client):
    client.delete('/1')
    response = client.get('/')
    assert response.json == []