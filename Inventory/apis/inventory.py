from flask import request, jsonify, Blueprint, abort
from Config.database import Inventory, inventory_schema
from Config.database import db


inventory = Blueprint("inventory", __name__, url_prefix="/inventory")


def remove_item_from_stock(name):
    errors = {}

    if "quantity_to_remove" not in request.json:
        errors["quantity_to_remove"] = "quantity_to_remove is missing"
    elif type(request.json["quantity_to_remove"]) != int:
        errors["quantity_to_remove"] = "quantity_to_remove must be an integer"

    if len(errors) != 0:
        return {"message": "Invalid request", "errors": errors}, 400

    item = Inventory.query.filter_by(name=name).first()

    if not item:
        return {"message": f"Item {name} does not exist"}, 404

    quantity_to_remove = request.json["quantity_to_remove"]
    available_quantity = item.available_quantity

    if available_quantity < quantity_to_remove:
        return {
            "quantity_to_remove": f"Not enough {name} in stock to remove this {quantity_to_remove}: only {available_quantity.available_quantity} {name} are available"
        }, 409

    item.available_quantity -= quantity_to_remove
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Item removed successfully",
                "item": inventory_schema.dump(item),
            }
        ),
        201,
    )


def update_item(name):
    item = Inventory.query.filter_by(name=name).first()
    if not item:
        return {"message": f"Item {name} does not exist"}, 404

    errors = {}
    update_fields = request.json

    for key, value in update_fields.items():
        if hasattr(item, key) and key != "item_category":
            setattr(item, key, value)
        else:
            return jsonify({"message": f"Invalid field '{key}'"}), 400

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Item updated successfully",
                "item": inventory_schema.dump(item),
            }
        ),
        201,
    )


def add_item():
    errors = {}

    item_categories = ["food", "clothes", "accessories", "electronics"]

    required_fields = [
        "name",
        "item_category",
        "price",
        "description",
        "available_quantity",
    ]

    for field in required_fields:
        if field not in request.json:
            errors[field] = f"{field} is missing"
        elif (field == "price" or field == "available_quantity") and type(
            request.json[field]
        ) != int:
            errors[field] = f"{field} must be an integer"
        elif (
            field != "price"
            and field != "available_quantity"
            and type(request.json[field]) != str
        ):
            errors[field] = f"{field} must be a string"
        elif field == "item_category" and request.json[field] not in item_categories:
            errors[field] = f"{field} must be one of {item_categories}"

    if len(errors) != 0:
        return {"message": "Invalid request", "errors": errors}, 400

    name = request.json["name"]
    item_category = request.json["item_category"]
    price = request.json["price"]
    description = request.json["description"]
    available_quantity = request.json["available_quantity"]

    item = Inventory.query.filter_by(name=name).first()

    if item:
        return {"message": f"Item {name} already exists"}, 409

    new_item = Inventory(
        name=name,
        item_category=item_category,
        price=price,
        description=description,
        available_quantity=available_quantity,
    )

    db.session.add(new_item)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Item added successfully",
                "item": inventory_schema.dump(new_item),
            }
        ),
        201,
    )


def get_all_items():
    items = Inventory.query.all()
    if not items:
        return {"message": "No items found"}, 404

    return (
        jsonify(
            {
                "message": "Items retrieved successfully",
                "items": inventory_schema.dump(items, many=True),
            }
        ),
        200,
    )


def get_specific_item_information(name):
    item = Inventory.query.filter_by(name=name).first()
    if not item:
        return {"message": f"Item {name} does not exist"}, 404

    return (
        jsonify(
            {
                "message": "Item retrieved successfully",
                "item": inventory_schema.dump(item),
            }
        ),
        200,
    )


@inventory.route("/", methods=["POST"])
def api_add_item():
    return add_item()


@inventory.route("/<name>", methods=["PUT"])
def api_update_item(name):
    return update_item(name)


@inventory.route("/remove/<name>", methods=["PUT"])
def api_remove_item_from_stock(name):
    return remove_item_from_stock(name)


@inventory.route("/", methods=["GET"])
def api_get_all_items():
    return get_all_items()


@inventory.route("/<name>", methods=["GET"])
def api_get_specific_item_information(name):
    return get_specific_item_information(name)
