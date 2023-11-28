import pytest
import requests

BASE_URL = "http://localhost:5000/user"


sample_user = {
    "full_name": "John Doe",
    "username": "testJhonDoe",
    "password": "securepassword",
    "age": 30,
    "address": "123 Main St",
    "gender": "Male",
    "marital_status": "Single",
}


@pytest.fixture(scope="function")
def setup_user():
    response = requests.post(BASE_URL, json=sample_user)
    assert response.status_code == 201
    yield sample_user
    delete_response = requests.delete(f"{BASE_URL}/{sample_user['username']}")
    assert delete_response.status_code == 200


def test_add_customer():
    response = requests.post(BASE_URL, json=sample_user)
    assert response.status_code == 201


def test_delete_user():
    create_response = requests.post(BASE_URL, json=sample_user)
    assert create_response.status_code == 201

    delete_response = requests.delete(f"{BASE_URL}/{sample_user['username']}")
    assert delete_response.status_code == 200


def test_get_all_users():
    response = requests.get(BASE_URL)
    assert response.status_code == 200


def test_get_user():
    create_response = requests.post(BASE_URL, json=sample_user)
    assert create_response.status_code == 201

    response = requests.get(f"{BASE_URL}/{sample_user['username']}")
    assert response.status_code == 200


def test_deduce_money():
    create_response = requests.post(BASE_URL, json=sample_user)
    assert create_response.status_code == 201

    deduce_data = {"amount_to_charge": 10}  # Adjust amount as needed
    response = requests.put(
        f"{BASE_URL}/transactions/{sample_user['username']}", json=deduce_data
    )
    assert response.status_code == 200


def test_charge_customer():
    create_response = requests.post(BASE_URL, json=sample_user)
    assert create_response.status_code == 201

    charge_data = {
        "user_to_charge": sample_user["username"],
        "amount_to_charge": 20,
    }
    response = requests.put(f"{BASE_URL}/transactions", json=charge_data)
    assert response.status_code == 200


def test_update_information():
    create_response = requests.post(BASE_URL, json=sample_user)
    assert create_response.status_code == 201

    update_data = {"age": 31}
    response = requests.put(f"{BASE_URL}/{sample_user['username']}", json=update_data)
    assert response.status_code == 200
