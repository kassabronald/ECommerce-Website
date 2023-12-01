from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
import marshmallow as ma
from enum import Enum
import json

db = SQLAlchemy()


class SinglePurchase:
    """Class representing a single purchase."""

    def __init__(self, product_name, quantity_bought, price_paid):
        """
        Initialize a SinglePurchase object.

        :param str product_name: The name of the product.
        :param int quantity_bought: The quantity bought.
        :param float price_paid: The price paid for the product.
        """
        self.product_name = product_name
        self.quantity_bought = quantity_bought
        self.price_paid = price_paid


class SinglePurchaseMeta(ma.Schema):
    """Marshmallow schema for SinglePurchase."""

    class Meta:
        fields = ("product_name", "quantity_bought", "price_paid")


single_purchase_schema = SinglePurchaseMeta()


class Purchases(db.Model):
    """Class representing purchase records."""

    __tablename__ = "Purchases"
    customer_username = db.Column(db.String(100), primary_key=True)
    purchase_history = db.Column(JSON)

    def __init__(self, customer_username):
        """
        Initialize a Purchases object.

        :param str customer_username: The username of the customer.
        """
        self.customer_username = customer_username
        self.purchase_history = json.dumps([])

    def add_purchase(self, triplet):
        """
        Add a purchase to the purchase history.

        :param triplet: The purchase information to be added.
        :type triplet: tuple
        """
        existing_history = (
            json.loads(self.purchase_history) if self.purchase_history else []
        )
        existing_history.append(triplet)
        self.purchase_history = json.dumps(existing_history)


class PurchasesSchema(ma.Schema):
    """Marshmallow schema for Purchases."""

    class Meta:
        fields = ("customer_username", "purchase_history")


purchase_schema = PurchasesSchema()
