from flask_smorest import abort,Blueprint
from db import db
from Models import TagModel,StoreModel,ItemModel
from flask.views import MethodView
from schema import FullTagSchema,TagSchema,ItemTagSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Tag",__name__)

@blp.route("/store/<string:store_id>/tag")
class Create_and_Get_tag_in_store(MethodView):
    
    @blp.arguments(FullTagSchema) #在STORE裡面創造TAG
    @blp.response(201,FullTagSchema)
    def post(self,data,store_id):
        new_tag = TagModel(**data,store_id = store_id)
        try:
            db.session.add(new_tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(404,str(e))
        return new_tag
    
    @blp.response(200,TagSchema(many=True)) #獲得商店裡的所有TAG
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags #lazy導致這裡應回傳的是一個查詢對象，但是系統自動查詢了=>正確的是return store.tags.all()
    
@blp.route("/tag/<string:tag_id>")
class Get_specific_tag_and_Delete(MethodView):
    
    @blp.response(201,schema=FullTagSchema) #獲得特定TAG
    def get(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(200,example = {"message" : "delete successfully"}) #刪除TAG，若是TAG有和ITEM關聯則無法刪除
    @blp.alt_response(404,example = {"message":"This tag has a link with item"})
    def delete(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if tag.items:
            abort(404,message = "This tag has a link with item")
        db.session.delete(tag)
        db.session.commit()
        return  {"message" : "delete successfully"}
    
@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class Link_and_Unlink(MethodView):
    
    @blp.response(201,ItemTagSchema) #讓item與TAG相關聯
    def post(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if item.store_id != tag.store_id :
            abort(404,message = "Ensure item and tag are in the same store")
        item.tags.append(tag)
        db.session.add(item)
        db.session.commit()
        return {"message":"Link successfully","tag":tag,"item":item}
    
    @blp.response(200,ItemTagSchema) #解除ITEM與TAG的關聯
    def delete(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)
        db.session.add(item)
        db.session.commit()
        return {"message":"Unlink successfully","tag":tag,"item":item}
        