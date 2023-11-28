from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
import marshmallow as ma
from enum import Enum
import json

db = SQLAlchemy()


class SinglePurchase:
    def __init__(self, product_name, quantity_bought, price_paid):
        self.product_name = product_name
        self.quantity_bought = quantity_bought
        self.price_paid = price_paid


class SinglePurchaseMeta(ma.Schema):
    class Meta:
        fields = ("product_name", "quantity_bought", "price_paid")


single_purchase_schema = SinglePurchaseMeta()


class Purchases(db.Model):
    __tablename__ = "Purchases"
    customer_username = db.Column(db.String(100), primary_key=True)
    purchase_history = db.Column(JSON)

    def __init__(self, customer_username):
        self.customer_username = customer_username
        self.purchase_history = json.dumps([])

    def add_purchase(self, triplet):
        existing_history = (
            json.loads(self.purchase_history) if self.purchase_history else []
        )
        existing_history.append(triplet)
        self.purchase_history = json.dumps(existing_history)


class PurchasesSchema(ma.Schema):
    class Meta:
        fields = ("customer_username", "purchase_history")


purchase_schema = PurchasesSchema()
