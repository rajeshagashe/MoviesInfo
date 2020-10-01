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

print("Testing with ", username, " for Exceptions")

@pytest.fixture
def client():
    app = create_app("test_config")
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_register(client):
    """Make sure register works."""
    res = register_with_duplicate_username(client)
    assert b"user_name taken." in res

    res = register_without_username(client)
    assert b"user_name required." in res
    
    res = register_without_password(client)
    assert b"password required." in res
    
    res = register_with_inavlid_role(client)
    assert b"Invalid user_role." in res

def test_login(client):
    """Make sure register works."""
    res = login_invalid_username(client)
    assert b"Incorrect username." in res

    res = login_invalid_password(client)
    assert b"Incorrect password." in res

def login_invalid_username(client):
    return client.post('user/login', json={
        "user_name" : username * 2,
        "password" : password
    }).data

def login_invalid_password(client):
    return client.post('user/login', json={
        "user_name" : username,
        "password" : password * 2
    }).data

def register_with_inavlid_role(client):
    return client.post('user/register', json={
        "user_name" : username * 3,
        "password" : password * 3,
        "user_role" : "invalid" 
    }).data

def register_without_password(client):
    return client.post('user/register', json={
        "user_name" : username * 2
    }).data

def register_without_username(client):
    return client.post('user/register', json={
        "password" : password
    }).data

def register_with_duplicate_username(client):
    client.post('user/register', json={
        "user_name" : username,
        "password" : password
    }).data

    return client.post('user/register', json={
        "user_name" : username,
        "password" : password
    }).data