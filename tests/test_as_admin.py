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

print("Testing with ", username, "as Admin")

@pytest.fixture
def client():
    app = create_app("test_config")
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_register_admin(client):
    """Make sure register works."""

    res = register_as_admin(client)
    assert b"{\"status\": \"success\", \"msg\": \"User registered.\"}" in res

def test_login_admin(client):
    """Make sure login works."""

    res = login(client)
    assert b"{\"status\": \"success\", \"msg\": \"Logged in\"}" in res

def test_read_admin(client):
    "'Make sure crud/read works'"
    login(client)
    res = read(client)
    assert b"{\"status\": \"success\", \"msg\": \"crud/read msg\"}" in res

def test_create_update_delete_admin(client):
    "'Make sure crud/create works'"
    res = create(client)
    assert b"{\"status\": \"success\", \"msg\": \"New movie added.\"}" in res
    
    res_json = json.loads(res.decode("utf-8"))
    movie_id = res_json[0].get("id")
    
    res = update(client, movie_id)
    assert b"{\"status\": \"success\", \"msg\": \"Changes Saved.\"}" in res

    res = delete(client, movie_id)
    assert b"{\"status\": \"success\", \"msg\": \"Deleted.\"}" in res

def test_search_admin(client):
    "'Make sure crud/delete works'"
    res = create(client)
    res_json = json.loads(res.decode("utf-8"))
    movie_id = res_json[0].get("id")
    
    res = search(client)
    assert b"{\"status\": \"success\", \"msg\": \"Search results returned successfully.\"}" in res

    res = delete(client, movie_id)
    assert b"{\"status\": \"success\", \"msg\": \"Deleted.\"}" in res

def test_logout_admin(client):
    "'Make sure user/logout works'"
    res = logout(client)
    assert b"{\"status\": \"success\", \"msg\": \"Logged Out\"}" in res

def logout(client):
    login(client)
    return client.delete('user/logout').data

def search(client):
    login(client)
    return client.get('search/movies?name=movie&director=director').data

def delete(client, movie_id):
    login(client)
    return client.delete('crud/delete/' + str(movie_id)).data


def update(client, movie_id):
    login(client)
    return client.patch('crud/update/' + str(movie_id), json={
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
    return client.get("crud/read").data

def register_as_admin(client):
    return client.post('user/register', json={
        "user_name" : username,
        "password" : password,
        "user_role" : "admin"
    }).data

def login(client):
    return client.post('user/login', json={
        "user_name" : username,
        "password" : password
    }).data


    