"""
ronald bi shil
"""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from apis.inventory import inventory
from Config.marshmallow import ma
from Config.database import db
from db_config import DB_CONFIG
from flask_cors import CORS


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONFIG
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app, resources={r"/*": {"origins": "http://localhost:5002"}})


db.app = app
db.init_app(app)
ma.app = app
ma.init_app(app)

app.register_blueprint(inventory)


if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
