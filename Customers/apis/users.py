from flask import request, jsonify, Blueprint, abort
from Config.database import User, user_schema
from Config.database import db


users = Blueprint("users", __name__, url_prefix="/user")


def add_customer():
    errors = {}
    required_fields = [
        "full_name",
        "username",
        "password",
        "age",
        "address",
        "gender",
        "marital_status",
    ]

    for field in required_fields:
        if field not in request.json:
            errors[field] = f"{field} is missing"
        elif field == "age" and type(request.json[field]) != int:
            errors[field] = f"{field} must be an integer"
        elif field != "age" and type(request.json[field]) != str:
            errors[field] = f"{field} must be a string"

    if len(errors) != 0:
        return jsonify(errors), 400

    full_name = request.json["full_name"]
    username = request.json["username"]
    password = request.json["password"]
    age = request.json["age"]
    address = request.json["address"]
    gender = request.json["gender"]
    marital_status = request.json["marital_status"]

    userWithTheSameUsername = User.query.filter_by(username=username).first()
    if userWithTheSameUsername:
        return {"username": f"username {username} is taken"}, 409

    user = User(
        full_name=full_name,
        username=username,
        password=password,
        age=age,
        address=address,
        gender=gender,
        marital_status=marital_status,
    )
    db.session.add(user)
    db.session.commit()

    return (
        jsonify({"message": "User added successfully", "user": user_schema.dump(user)}),
        201,
    )


def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": f"User '{username}' not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User '{username}' deleted successfully"}), 200


def get_all_users():
    users = User.query.all()
    return (
        jsonify(
            {
                "message": "List of all users",
                "users": user_schema.dump(users, many=True),
            }
        ),
        200,
    )


def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": f"User '{username}' not found"}), 404

    return (
        jsonify(
            {
                "message": f"Details for user '{username}'",
                "user": user_schema.dump(user),
            }
        ),
        200,
    )


def deduce_money(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": f"User '{username}' not found"}), 404

    amount_to_charge = request.json.get("amount_to_charge")
    if not isinstance(amount_to_charge, (int, float)) or amount_to_charge <= 0:
        return jsonify({"message": "Invalid amount to charge"}), 400

    user.balance -= amount_to_charge
    db.session.commit()

    return (
        jsonify(
            {
                "message": f"Deducted {amount_to_charge} from user '{username}'",
                "user": user_schema.dump(user),
            }
        ),
        200,
    )


def charge_customer():
    user_to_charge = request.json.get("user_to_charge")
    amount_to_charge = request.json.get("amount_to_charge")

    if not user_to_charge or not amount_to_charge:
        return (
            jsonify(
                {"message": "Both user_to_charge and amount_to_charge are required"}
            ),
            400,
        )

    user = User.query.filter_by(username=user_to_charge).first()
    if not user:
        return jsonify({"message": f"User '{user_to_charge}' not found"}), 404

    user.balance += amount_to_charge
    db.session.commit()

    return (
        jsonify(
            {
                "message": f"Charged {amount_to_charge} to user '{user_to_charge}'",
                "user": user_schema.dump(user),
            }
        ),
        200,
    )


def update_information(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": f"User '{username}' not found"}), 404

    update_fields = request.json

    for key, value in update_fields.items():
        if hasattr(user, key) and key != "username" and key != "balance":
            setattr(user, key, value)
        else:
            return jsonify({"message": f"Invalid field '{key}'"}), 400

    db.session.commit()

    return (
        jsonify(
            {
                "message": f"User '{username}' information updated",
                "user": user_schema.dump(user),
            }
        ),
        200,
    )


@users.route("/", methods=["POST"], strict_slashes=False)
def api_add_customer():
    return add_customer()


@users.route("/<username>", methods=["DELETE"], strict_slashes=False)
def api_delete_user(username):
    return delete_user(username)


@users.route("/", methods=["GET"], strict_slashes=False)
def api_get_all_users():
    return get_all_users()


@users.route("/<username>", methods=["GET"], strict_slashes=False)
def api_get_user(username):
    return get_user(username)


@users.route("/transactions/<username>", methods=["PUT"], strict_slashes=False)
def api_deduce_money(username):
    return deduce_money(username)


@users.route("/transactions", methods=["PUT"], strict_slashes=False)
def api_charge_customer():
    return charge_customer()


@users.route("/<username>", methods=["PUT"], strict_slashes=False)
def api_update_information(username):
    return update_information(username)
