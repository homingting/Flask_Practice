from db import db
from schema import ItemSchema, FullItemSchema, UpdateItemSchema
from Models import ItemModel, StoreModel
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Item", __name__)


@blp.route("/store/<string:store_id>/item")
class Create_and_Get_item_in_store(MethodView):

    @jwt_required(
        fresh=True
    )  # 只能fresh token才可以進行此動作，同常用於更改密碼刪除帳號等
    @blp.arguments(FullItemSchema)  # 創造商品
    @blp.response(201, schema=FullItemSchema)
    def post(self, data, store_id):
        new_item = ItemModel(**data, store_id=store_id)
        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError:
            abort(404, description="Error")
        return new_item

    @jwt_required()
    @blp.response(202, schema=ItemSchema)  # 獲得指定商店的商品
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.items


@blp.route("/item/<string:item_id>")
class Delete_and_Get_specific_and_Update(MethodView):

    @jwt_required()  # 刪除指定商品
    def delete(self, item_id):

        jwt = get_jwt()  # 查看jwt是否id為1
        if not jwt.get("is_admin"):
            abort(40, message="Admin privilege required.")

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Delete successfully"}, 201

    @jwt_required()
    @blp.response(200, schema=FullItemSchema)  # 獲得指定商品資訊
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(UpdateItemSchema)  # 更新商品資訊，若無此商品則進行創造
    @blp.response(201, UpdateItemSchema)
    def put(self, data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item and item.store_id == data["store_id"]:
            item.item_name = data["item_name"]
            item.item_price = data["item_price"]
            message = "update this item"
        else:
            item = ItemModel(**data)
            message = "This item not exist,so create a new one"
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(404, message=str(e))
        return {"message": message, "update_item": item}
