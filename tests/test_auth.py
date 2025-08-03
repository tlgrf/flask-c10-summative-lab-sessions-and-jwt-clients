import pytest
import sys
import os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_signup(client):
    username = f"testuser_{uuid.uuid4()}"
    response = client.post('/signup', json={
        'username': username,
        'password': 'testpass'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'token' in data
    assert data['user']['username'] == username

def test_login(client):
    username = f"testuser_{uuid.uuid4()}"
    # First, sign up
    client.post('/signup', json={
        'username': username,
        'password': 'testpass'
    })
    # Then, login
    response = client.post('/login', json={
        'username': username,
        'password': 'testpass'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert data['user']['username'] == username