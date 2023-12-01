import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pytest
from app import app
from flask import json
import faker

item_data = {
    "name": "TestItem",
    "item_category": "food",
    "price": 10,
    "description": "Test description",
    "available_quantity": 50,
}


@pytest.fixture
def client():
    return app.test_client()


def test_add_item(client):
    item_data = {
        "name": faker.Faker().name(),
        "item_category": "food",
        "price": 10,
        "description": "Test description",
        "available_quantity": 50,
    }
    response = client.post("/inventory/", json=item_data)
    assert response.status_code == 201


def test_get_all_items(client):
    response = client.get("/inventory/")
    assert response.status_code == 200
    assert "items" in response.json


def test_get_specific_item_information(client):
    response = client.get("/inventory/TestItem")
    assert response.status_code == 200
    assert "item" in response.json


def test_update_item(client):
    item_data = {
        "name": "TestItem",
        "price": 15,
        "description": "Updated description",
        "available_quantity": 40000000,
    }
    response = client.put("/inventory/TestItem", json=item_data)
    assert response.status_code == 201


def test_remove_item_from_stock(client):
    item_data = {"quantity_to_remove": 5}
    response = client.put("/inventory/remove/TestItem", json=item_data)
    assert response.status_code == 201
