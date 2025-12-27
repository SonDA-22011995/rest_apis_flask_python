from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel


blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):

    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
        # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404, message="Item not found.")

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}
        # try:
        #     del items[item_id]
        #     return {"message": "Item deleted."}
        # except KeyError:
        #     abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if "name" in item_data:
            item.name = item_data["name"]
        if "price" in item_data:
            item.price = item_data["price"]
        if "store_id" in item_data:
            item.store_id = item_data["store_id"]

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the item.")

        return item
        # There's  more validation to do here!
        # Like making sure price is a number, and also both items are optional
        # Difficult to do with an if statement...
        # sonda change `or` to `and` operator
        # if "price" not in item_data and "name" not in item_data:
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'price', or 'name' are included in the JSON payload.",
        #     )
        # try:
        #     item = items[item_id]
        #
        #     # https://blog.teclado.com/python-dictionary-merge-update-operators/
        #     item |= item_data
        #
        #     return item
        # except KeyError:
        #     abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):

    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return item

