from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from apis.inventory import inventory
from Config.marshmallow import ma
from Config.database import db
from Config.db_config import DB_CONFIG

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONFIG
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.app = app
db.init_app(app)
ma.app = app
ma.init_app(app)

app.register_blueprint(inventory)


if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
