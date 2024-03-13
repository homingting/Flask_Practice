from flask_smorest import Blueprint,abort
from Models import StoreModel
from db import db
from schema import StoreSchema,FullStoreSchema
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("store",__name__)

@blp.route("/store")
class Create_and_Get_all(MethodView):
    
    @blp.arguments(StoreSchema) #創造商店
    @blp.response(201,StoreSchema)
    def post(self,data):
        if(StoreModel.query.filter(StoreModel.store_name == data["store_name"]).first()):
            abort(404,description = "This store is exist")
        new_store = StoreModel(**data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except SQLAlchemyError:
            abort(404,description = "Some wrong when create a store")
        return new_store
    
    @blp.response(202,StoreSchema(many=True)) #查詢所有商店
    def get(self):
        stores = StoreModel.query.all()
        return stores

@blp.route("/store/<string:store_id>")
class Delete_and_Get_specific(MethodView):
    
    @blp.response(200,example = {"message":"delete successfully"}) #刪除商店
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"delete successfully"}
    
    @blp.response(201,FullStoreSchema)  #獲得特定商店資訊
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store