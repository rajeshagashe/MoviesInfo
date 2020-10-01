import pytest
import sys
import random
import string
import json

from app import create_app

def random_string_generator():
    allowed_chars = string.ascii_letters + string.punctuation
    size = 12
    return ''.join(random.choice(allowed_chars) for x in range(size))

username = random_string_generator()
password = random_string_generator()

print("Testing with ", username, " as User")

@pytest.fixture
def client():
    app = create_app("test_config")
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_register(client):
    """Make sure register works."""

    res = register(client)
    assert b"{\"status\": \"success\", \"msg\": \"User registered.\"}" in res

def test_login(client):
    """Make sure login works."""

    res = login(client)
    assert b"{\"status\": \"success\", \"msg\": \"Logged in\"}" in res

def test_read(client):
    "'Make sure crud/read works'"
    res = read(client)
    assert b"{\"status\": \"success\", \"msg\": \"crud/read msg\"}" in res

def test_create(client):
    "'Make sure crud/create works'"
    res = create(client)
    assert b"admin access required to perform this action." in res

def test_update(client):
    "'Make sure crud/update works'"
    res = update(client)
    assert b"admin access required to perform this action." in res

def test_delete(client):
    "'Make sure crud/delete works'"
    res = update(client)
    assert b"admin access required to perform this action." in res

def test_search(client):
    "'Make sure crud/delete works'"
    res = search(client)
    assert b"{\"status\": \"success\", \"msg\": \"Search results returned successfully.\"}" in res

def test_logout(client):
    "'Make sure user/logout works'"
    res = logout(client)
    assert b"{\"status\": \"success\", \"msg\": \"Logged Out\"}" in res

def logout(client):
    login(client)
    return client.delete('user/logout').data
    
def search(client):
    login(client)
    return client.get('search/movies').data

def delete(client):
    login(client)
    return client.delete('crud/delete/50').data

def update(client):
    login(client)
    return client.patch('crud/update/50', json={
        "name" : "movie",
        "director" : "director",
        "99popularity": 50.0, 
        "genre": ["Action"],
        "imdb_score": 5.0
    }).data

def create(client):
    login(client)
    return client.post('crud/create', json={
        "name" : "movie",
        "director" : "director",
        "99popularity": 50.0, 
        "genre": ["Action"],
        "imdb_score": 5.0
    }).data

def read(client):
    login(client)
    return client.get("crud/read").data    

def register(client):
    return client.post('user/register', json={
        "user_name" : username,
        "password" : password
    }).data

def login(client):
    return client.post('user/login', json={
        "user_name" : username,
        "password" : password
    }).data


    