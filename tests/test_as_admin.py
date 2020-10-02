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
    res_json = json.loads(res.decode("utf-8"))
    assert len(res_json) == 1
    reg_user_id = res_json[0].get("id")
    reg_user_name = res_json[0].get("user_name")
    reg_user_role = res_json[0].get("user_role")
    assert reg_user_name == username
    assert reg_user_role == "admin"

    res = login(client)
    res_json = json.loads(res.decode("utf-8"))
    assert len(res_json) == 1
    login_user_id = res_json[0].get("id")
    login_user_name = res_json[0].get("user_name")
    login_user_role = res_json[0].get("user_role")
    

    assert (login_user_id == reg_user_id and \
        login_user_name == reg_user_name and login_user_role == reg_user_role)


# def test_login_admin(client):
#     """Make sure login works."""

#     res = login(client)
#     assert b"{\"status\": \"success\", \"msg\": \"Logged in\"}" in res

def test_read_admin(client):
    "'Make sure crud/read works'"
    res = read(client)
    res_json = json.loads(res.decode("utf-8"))
    assert isinstance(res_json, list)

    for each in res_json:
        assert isinstance(each.get("id"), (int, float))
        assert isinstance(each.get("name"), str)
        assert isinstance(each.get("nn_popularity"), float)
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

def test_create_update_delete_admin(client):
    "'Make sure crud/create works'"
    res = create(client)
    res_json = json.loads(res.decode("utf-8"))
    assert isinstance(res_json, list)
    assert len(res_json) == 1
    assert isinstance(res_json[0].get("id"), (int, float))
    assert isinstance(res_json[0].get("name"), str)
    assert isinstance(res_json[0].get("nn_popularity"), float)
    assert isinstance(res_json[0].get("director"), str)
    assert isinstance(res_json[0].get("genre"), str)
    assert isinstance(res_json[0].get("imdb_score"), float)

    movie_id = res_json[0].get("id")
    res = update(client, movie_id)
    res_json = json.loads(res.decode("utf-8"))
    assert isinstance(res_json, list)
    assert len(res_json) == 1

    updated_json = {
        "id" : movie_id,
        "name" : "movie",
        "director" : "director",
        "nn_popularity": 50.0, 
        "genre": ["Action"],
        "imdb_score": 5.0
    }
    updated_json["genre"] = ",".join(sorted([i.strip() for i in updated_json.get("genre")]))

    assert res_json[0] == updated_json

    res = delete(client, movie_id)
    res_json = json.loads(res.decode("utf-8"))
    assert isinstance(res_json, list)
    assert len(res_json) == 1
    assert res_json[0] == updated_json

def test_search_admin(client):
    "'Make sure search/movies works'"
    res = create(client)
    res_json = json.loads(res.decode("utf-8"))
    created_movie = res_json[0]
    movie_id = created_movie.get("id")
    
    res = search(client)
    res_json = json.loads(res.decode("utf-8"))
    assert isinstance(res_json, list)

    created_movie["genre"] = ",".join(sorted([i.strip() for i in created_movie.get("genre")]))
    for each in res_json:
        assert "movie" in each.get("name").lower() 
        assert "director" in each.get("director").lower()
    res = delete(client, movie_id)

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
    login(client)
    return client.get("crud/read").data

def read_with_id(client, movie_id):
    login(client)
    return client.get("crud/read/" + str(movie_id)).data

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