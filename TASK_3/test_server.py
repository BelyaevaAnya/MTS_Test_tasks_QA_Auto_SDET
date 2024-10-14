import json
import pytest
from server import app  # Make sure to import your Flask app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_inverse(client):
    response = client.post('/inverse', json={"key1": "value1"})
    assert response.status_code == 200
    assert response.json == {"value1": "key1"}

def test_unstable(client):
    response = client.get('/unstable')
    assert response.status_code in (200, 400)
    if response.status_code == 200:
        assert response.json == {"message": "HAPPY"}
    elif response.status_code == 400:
        assert response.json == {"message": "UNHAPPY"}
