from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as EnumSQL
import marshmallow as ma
from enum import Enum

db = SQLAlchemy()


class ItemCategoryEnum(Enum):
    food = "food"
    clothes = "clothes"
    accessories = "accessories"
    electronics = "electronics"


class Inventory(db.Model):
    __tablename__ = "Inventory"
    name = db.Column(db.String(100), primary_key=True)
    item_category = db.Column(EnumSQL(ItemCategoryEnum), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, name, item_category, price, description, available_quantity):
        self.name = name
        self.item_category = item_category
        self.price = price
        self.description = description
        self.available_quantity = available_quantity


class InventorySchema(ma.Schema):
    item_category = ma.fields.Function(lambda obj: obj.item_category.value)

    class Meta:
        fields = ("name", "item_category", "price", "description", "available_quantity")


inventory_schema = InventorySchema()
