# Following structure from: https://www.digitalocean.com/community/tutorials/unit-test-in-flask
# Following the basic structure on how to use pytest because I have never used it before
# Testing on: http://127.0.0.1:8000

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app 
import pytest

@pytest.fixture
def client():
    # Test: finding client (diff-level: easy)
    with app.test_client() as client:
        yield client
def test_getKey(client):
    # This test case works only for default fake key!
    # Do not put a real key before using this suite!
    response = client.get('/api/getKey')
    assert response.status_code == 200
    assert response.json == {"message": "super_secret_key"}

def test_searchArticles(client):
    # Test: test searchArticles route (diff-level: mid)
    # This test does work!
    # However, setting it to 400 because I do not want to expose my key!
    response = client.get('/api/searchArticles')
    assert response.status_code == 200
    assert response.json == {"message": "Error!"}

def test_non_existent_route(client):
    # Test: non-existant route (diff-level: easy)
    response = client.get('/non-existent')
    assert response.status_code == 404