from flask_sqlalchemy import SQLAlchemy
import bcrypt
import marshmallow as ma

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))
    gender = db.Column(db.String(10))
    marital_status = db.Column(db.String(20))
    balance = db.Column(db.Float, default=0.0)
    amount_owed = db.Column(db.Float, default=0.0)

    def __init__(
        self, full_name, username, password, age, address, gender, marital_status
    ):
        super(User, self).__init__(username=username)
        self.full_name = full_name
        self.age = age
        self.address = address
        self.gender = gender
        self.marital_status = marital_status
        self.hashed_password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.username}>"


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "full_name")
        model = User


user_schema = UserSchema()
