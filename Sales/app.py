from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from apis.sales import sales
from Config.marshmallow import ma
from Config.database import db
from db_config import DB_CONFIG

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONFIG
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.app = app
db.init_app(app)
ma.app = app
ma.init_app(app)

app.register_blueprint(sales)


if __name__ == "__main__":
    app.run(debug=True, port=5002, host="0.0.0.0")
