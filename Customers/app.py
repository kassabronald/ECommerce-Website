from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from db_config import DB_CONFIG
from apis.users import users
from Config.marshmallow import ma
from Config.bcrypt import bcrypt
from Config.database import db
from flask_cors import CORS


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONFIG
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app, resources={r"/*": {"origins": "http://localhost:5002"}})


db.app = app
db.init_app(app)
ma.app = app
ma.init_app(app)
bcrypt.app = app
bcrypt.init_app(app)

app.register_blueprint(users)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
