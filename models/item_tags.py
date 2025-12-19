from db import db


class ItemsTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))

    __table_args__ = (
        db.UniqueConstraint(
            "item_id",
            "tag_id",
            name="uq_items_tags_item_id_tag_id"
        ),
    )