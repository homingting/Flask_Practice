from db import db

class ItemModel(db.Model):
    __tablename__ = "ItemTable"
    id = db.Column(db.Integer,primary_key = True)
    item_price = db.Column(db.Float,unique = False,nullable = False)
    item_name = db.Column(db.String(60),nullable = False,unique = False)
    
    store_id = db.Column(db.Integer,db.ForeignKey("StoreTable.id"),nullable = False)
    store = db.relationship("StoreModel",back_populates = "items")
    
    tags = db.relationship("TagModel",back_populates = "items",secondary = "ItemTagTable")
    