from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
import marshmallow as ma
from enum import Enum
import json

db = SQLAlchemy()


class Purchases(db.Model):
    __tablename__ = "Purchases"
    username = db.Column(db.String(100), primary_key=True)
    items_and_quantity_purchased = db.Column(JSON)
    total_price_paid = db.Column(db.Integer, nullable=False)

    def __init__(self, username, items_and_quantity_purchased, total_price_paid):
        self.username = username
        self.items_and_quantity_purchased = items_and_quantity_purchased
        self.total_price_paid = total_price_paid


class PurchasesSchema(ma.Schema):
    class Meta:
        fields = ("username", "items_and_quantity_purchased", "total_price_paid")


purchase_schema = PurchasesSchema()
