import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_check_even_with_even_number(client):
    response = client.post('/api/check_even', json={"number": 4})
    assert response.status_code == 200
    data = response.get_json()
    assert data["is_even"] is True
    assert data["number"] == 4

def test_check_even_with_odd_number(client):
    response = client.post('/api/check_even', json={"number": 5})
    assert response.status_code == 200
    data = response.get_json()
    assert data["is_even"] is False
    assert data["number"] == 5

def test_check_even_with_non_integer(client):
    response = client.post('/api/check_even', json={"number": "abc"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
