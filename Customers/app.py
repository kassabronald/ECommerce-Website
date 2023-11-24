from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from db_config import DB_CONFIG
from apis.users import users
from Config.marshmallow import ma
from Config.bcrypt import bcrypt
from Config.database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONFIG
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.app = app
db.init_app(app)
ma.app = app
ma.init_app(app)
bcrypt.app = app
bcrypt.init_app(app)

app.register_blueprint(users)


# def check_db_connection():
#     try:
#         db.engine.connect()
#         print("Database connection successful")
#     except Exception as e:
#         print("Database connection error: ", e)
#         return False
#     return True


# @app.route("/ok")
# def test_db_connection():
#     if check_db_connection():
#         return jsonify("Database connection successful")
#     else:
#         return jsonify("Database connection error")


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
