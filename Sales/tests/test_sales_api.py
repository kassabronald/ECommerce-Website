import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pytest
from app import app
from flask import json
import faker


@pytest.fixture
def client():
    return app.test_client()


def test_display_available_goods(client):
    response = client.get("/sales/available_goods")
    assert response.status_code == 200
    assert "available_goods" in response.json


def test_get_specific_item_information(client):
    response = client.get("/sales/TestItem")
    assert response.status_code == 200
    assert "item" in response.json


def test_make_sale(client):
    sale_data = {
        "item": "TestItem",
        "quantity": 1,
    }
    response = client.post("/sales/johndoe", json=sale_data)
    assert response.status_code == 201
    assert "Purchase" in response.json


def test_get_purchase_history(client):
    response = client.get(
        "/sales/purchase_history/johndoe"
    )  # Replace customer_name with an existing customer
    assert response.status_code == 200
    assert "purchase_history" in response.json
