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

def test_register_and_login(client):
    """Make sure register works."""

    res = register(client)
    res_json = json.loads(res.decode("utf-8"))
    assert isinstance(res_json, list)
    assert len(res_json) == 1
    reg_user_id = res_json[0].get("id")
    reg_user_name = res_json[0].get("user_name")
    reg_user_role = res_json[0].get("user_role")
    assert reg_user_name == username
    assert reg_user_role == "user"

    res = login(client)
    res_json = json.loads(res.decode("utf-8"))
    assert len(res_json) == 1
    login_user_id = res_json[0].get("id")
    login_user_name = res_json[0].get("user_name")
    login_user_role = res_json[0].get("user_role")
    

    assert (login_user_id == reg_user_id and \
        login_user_name == reg_user_name and login_user_role == reg_user_role)

def test_read(client):
    "'Make sure crud/read works'"
    res = read(client)
    res_json = json.loads(res.decode("utf-8"))
    assert isinstance(res_json, list)

    for each in res_json:
        assert isinstance(each.get("id"), (int, float))
        assert isinstance(each.get("name"), str)
        assert isinstance(each.get("99popularity"), float)
        assert isinstance(each.get("director"), str)
        assert isinstance(each.get("genre"), str)
        assert isinstance(each.get("imdb_score"), float)

    test_movie = res_json[0] 
    movie_id = test_movie.get("id")
    
    res = read_with_id(client, movie_id)
    res_json = json.loads(res.decode("utf-8"))
    
    assert isinstance(res_json, list)
    assert len(res_json) == 1
    
    assert res_json[0] == test_movie

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
    "'Make sure search/movies works'"
    res = read(client)
    res_json = json.loads(res.decode("utf-8"))
    assert isinstance(res_json, list)

    for each in res_json:
        assert isinstance(each.get("id"), (int, float))
        assert isinstance(each.get("name"), str)
        assert isinstance(each.get("99popularity"), float)
        assert isinstance(each.get("director"), str)
        assert isinstance(each.get("genre"), str)
        assert isinstance(each.get("imdb_score"), float)

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

def read_with_id(client, movie_id):
    login(client)
    return client.get("crud/read/" + str(movie_id)).data    

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


    