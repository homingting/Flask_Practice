from db import db


class TagModel(db.Model):
    __tablename__ = "TagTable"
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(80), unique=False, nullable=False)

    store_id = db.Column(
        db.Integer, db.ForeignKey("StoreTable.id"), nullable=False, unique=False
    )
    store = db.relationship("StoreModel", back_populates="tags")

    items = db.relationship(
        "ItemModel", back_populates="tags", secondary="ItemTagTable"
    )
