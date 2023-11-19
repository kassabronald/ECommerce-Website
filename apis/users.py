from flask import request, jsonify, Blueprint, abort
from Config.database import User, user_schema
from Config.database import db


users = Blueprint("users", __name__, url_prefix="/user")


@users.route("/", methods=["POST"], strict_slashes=False)
def addCustomer():
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
        elif type(request.json[field]) != str:
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

    return jsonify(user_schema.dump(user)), 201


@users.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
def deleteUser(id):
    user = User.query.get(id)
    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    return jsonify(user_schema.dump(user)), 200


@users.route("/", methods=["GET"], strict_slashes=False)
def getAllUsers():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True)), 200


@users.route("/<username>", methods=["GET"], strict_slashes=False)
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)

    return jsonify(user_schema.dump(user)), 200


@users.route("/transactions/<username>", methods=["PUT"], strict_slashes=False)
def deduceMoney(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)

    amount_to_charge = request.json["amount_to_charge"]
    user.balance -= amount_to_charge
    db.session.commit()

    return jsonify(user_schema.dump(user)), 200


@users.route("/transactions", methods=["PUT"], strict_slashes=False)
def chargeCustomer():
    user_to_charge = request.json["user_to_charge"]
    amount_to_charge = request.json["amount_to_charge"]

    user = User.query.filter_by(username=user_to_charge).first()
    if not user:
        abort(404)

    user.balance += amount_to_charge
    db.session.commit()

    return jsonify(user_schema.dump(user)), 200


@users.route("/<username>", methods=["PUT"], strict_slashes=False)
def update_information(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": f"User with username {username} not found"}), 404

    update_fields = request.json

    for key, value in update_fields.items():
        if hasattr(user, key):
            setattr(user, key, value)
        else:
            return jsonify({"message": f"Invalid field {key}"}), 400

    db.session.commit()

    return jsonify(user_schema.dump(user)), 200
