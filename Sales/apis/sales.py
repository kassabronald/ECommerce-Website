from flask import request, jsonify, Blueprint, abort
from Config.database import (
    Purchases,
    SinglePurchase,
    purchase_schema,
    single_purchase_schema,
)
from Config.database import db
import requests, json


inventory_api_url = "http://172.17.0.4:5001/inventory"
customers_api_url = "http://172.17.0.3:5000/user"

sales = Blueprint("sales", __name__, url_prefix="/sales")


def display_available_goods():
    response = None
    response = requests.get(inventory_api_url)
    try:
        response = requests.get(inventory_api_url)
    except requests.exceptions.ConnectionError:
        return (
            jsonify(
                {
                    "error": "Failed to fetch data from inventory API",
                    "response": response,
                }
            ),
            500,
        )

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])

        available_items = [
            {"name": item["name"], "price": item["price"]}
            for item in items
            if item.get("available_quantity", 0) > 0
        ]

        return (
            jsonify(
                {
                    "available_goods": available_items,
                    "message": "Available goods retrieved successfully",
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"error": "Failed to fetch data from inventory API"}),
            response.status_code,
        )


def get_specific_item_information(item):
    response = None
    try:
        response = requests.get(f"{inventory_api_url}/{item}")
    except requests.exceptions.ConnectionError:
        return (
            jsonify({"error": "Failed to fetch data from inventory API"}),
            500,
        )

    if response.status_code == 200:
        data = response.json()
        item = data.get("item", {})
        return (
            jsonify(item),
            200,
        )
    else:
        return (
            jsonify({"error": "Failed to fetch data from inventory API"}),
            response.status_code,
        )


def make_sale(item_name, quantity_to_purchase, customer_username):
    response = None

    try:
        response = requests.get(f"{inventory_api_url}/{item_name}")
    except requests.exceptions.ConnectionError:
        return (
            jsonify({"error": "Failed to fetch data from inventory API"}),
            500,
        )

    if response.status_code != 200:
        return (
            jsonify({"error": "Failed to fetch data from inventory API"}),
            response.status_code,
        )
    data = response.json()
    item = data.get("item", {})
    price = item.get("price", 0)
    available_quantity = item.get("available_quantity", 0)
    if available_quantity < quantity_to_purchase:
        return (
            jsonify({"error": "Not enough items in stock"}),
            400,
        )
    price_to_pay = price * quantity_to_purchase

    customer_info = None

    try:
        customer_info = requests.get(f"{customers_api_url}/{customer_username}")
    except requests.exceptions.ConnectionError:
        return (
            jsonify({"error": "Failed to fetch data from customers API"}),
            500,
        )
    if customer_info.status_code != 200:
        return (
            jsonify({"error": "Failed to fetch data from customers API"}),
            customer_info.status_code,
        )
    customer_data = customer_info.json().get("user", {})
    balance = customer_data.get("balance", 0)

    if balance < price_to_pay:
        return (
            jsonify({"error": "Insufficient funds"}),
            400,
        )
    deduction_payload = {"amount_to_charge": price_to_pay}
    deduction_response = requests.put(
        f"{customers_api_url}/transactions/{customer_username}", json=deduction_payload
    )
    if deduction_response.status_code != 200:
        return (
            jsonify({"error": "Failed to charge customer"}),
            deduction_response.status_code,
        )

    purchase_data = {"quantity_to_remove": quantity_to_purchase}
    purchase_response = requests.put(
        f"{inventory_api_url}/remove/{item_name}", json=purchase_data
    )

    if purchase_response.status_code != 201:
        return (
            jsonify({"error": "Failed to make purchase"}),
            purchase_response.status_code,
        )

    purchase_history = Purchases.query.filter_by(
        customer_username=customer_username
    ).first()

    if purchase_history:
        purchase_history.add_purchase((item_name, quantity_to_purchase, price_to_pay))
        db.session.commit()
    else:
        purchase_history = Purchases(
            customer_username=customer_username,
        )
        purchase_history.add_purchase((item_name, quantity_to_purchase, price_to_pay))
        db.session.add(purchase_history)
        db.session.commit()

    return (
        jsonify(
            {
                "message": "Purchase successful",
                "customer": customer_username,
                "Purchase": single_purchase_schema.dump(
                    SinglePurchase(item_name, quantity_to_purchase, price_to_pay)
                ),
            }
        ),
        201,
    )


def get_purchase_history(customer_name):
    purchase_history = Purchases.query.filter_by(customer_username=customer_name).all()
    if purchase_history:
        purchase_history = purchase_schema.dump(purchase_history, many=True)
        return (
            jsonify({"purchase_history": purchase_history}),
            200,
        )
    else:
        return (
            jsonify({"error": "No purchase history found"}),
            404,
        )


@sales.route("/available_goods", methods=["GET"])
def api_diaplay_available_goods():
    return display_available_goods()


@sales.route("/<item>", methods=["GET"])
def api_get_specific_item_information(item):
    return get_specific_item_information(item)


@sales.route("/<customer>", methods=["POST"])
def api_make_sale(customer):
    item = request.json.get("item")
    quantity = request.json.get("quantity")
    if not item or not quantity:
        return (
            jsonify({"error": "Item and quantity must be provided"}),
            400,
        )
    return make_sale(item, quantity, customer)


@sales.route("/purchase_history/<customer>", methods=["GET"])
def api_get_purchase_history(customer):
    return get_purchase_history(customer)
