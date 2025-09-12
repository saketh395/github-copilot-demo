import io
import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Welcome to the Flask backend!"

def test_api_data(client):
    response = client.post('/api/data', json={"data": "test"})
    assert response.status_code == 200
    assert response.get_json()["received"]["data"] == "test"

def test_upload_text_file(client):
    data = {
        'file': (io.BytesIO(b'Hello, world!'), 'test.txt')
    }
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'content' in json_data
    assert json_data['content'] == 'Hello, world!'
    assert json_data['filename'] == 'test.txt'

def test_upload_non_text_file(client):
    data = {
        'file': (io.BytesIO(b'\x00\x01\x02'), 'test.bin')
    }
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data
    assert json_data['error'] == 'Only text files are supported.'
