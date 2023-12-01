import sys, os


user_data = {
    "full_name": "John Doe Kassab",
    "username": "johndoe",
    "password": "password123",
    "age": 30,
    "address": "123 Main St, City",
    "gender": "Male",
    "marital_status": "Single",
}
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pytest
from app import app
from flask import json
import faker


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def sample_user(client):
    user_data = {
        "full_name": "John Doe Kassab",
        "username": "johndoe",
        "password": "password123",
        "age": 30,
        "address": "123 Main St, City",
        "gender": "Male",
        "marital_status": "Single",
    }

    response = client.post("/user/", json=user_data)
    assert response.status_code == 200

    yield user_data

    response = client.delete(f"/user/johndoe")
    assert response.status_code == 200


def test_add_customer(client):
    response = client.post(
        "/user/",
        json={
            "full_name": "John Doe",
            "username": "johndoe",
            "password": "password123",
            "age": 30,
            "address": "123 Main St",
            "gender": "Male",
            "marital_status": "Single",
        },
    )
    assert response.status_code == 201


def test_delete_user(client):
    response = client.delete("/user/johndoe")
    assert response.status_code == 200


def test_get_all_users(client):
    response = client.get("/user/")
    assert response.status_code == 200


def test_get_user(client):
    client.post("/user/", json=user_data)
    response = client.get("/user/johndoe")
    assert response.status_code == 200


def test_deduce_money(client):
    client.post("/user/", json=user_data)
    response = client.put("/user/transactions/johndoe", json={"amount_to_charge": 50})
    assert response.status_code == 200


def test_charge_customer(client):
    client.post("/user/", json=user_data)
    response = client.put(
        "/user/transactions",
        json={"user_to_charge": "johndoe", "amount_to_charge": 100},
    )
    assert response.status_code == 200


def test_update_information(client):
    client.post("/user/", json=user_data)
    response = client.put("/user/johndoe", json={"address": "456 Elm St"})
    assert response.status_code == 200
