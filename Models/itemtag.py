from db import db
class ItemTagModel(db.Model):
    __tablename__ = "ItemTagTable"
    id = db.Column(db.Integer,primary_key = True)
    
    tag_id = db.Column(db.Integer,db.ForeignKey("TagTable.id"))
    item_id = db.Column(db.Integer,db.ForeignKey("ItemTable.id"))