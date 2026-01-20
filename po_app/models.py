from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from po_app import db
from flask import send_file
from sqlalchemy import func

class PO(db.Model):
    zip: so.Mapped[int] = so.mapped_column(primary_key=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True)
    address: so.Mapped[str] = so.mapped_column(sa.String(64))
    state: so.Mapped[str] = so.mapped_column(sa.String(2))
    visited: so.Mapped[bool] = so.mapped_column(index=True)

    def __repr__(self):
        return '<Post Office {} {}>'.format(self.zip, self.city)
    
    @property
    def po_pic(self):
        if self.visited:
            pic = ''.join(word.capitalize() for word in self.city.split(' ')) + ".jpg"
            return pic
        else:
            return None
        
    def get_random_post_offices():
        po_list = db.select(PO).where(PO.visited).order_by(func.random()).limit(3)
        po_random = db.session.scalars(po_list).all()
        return po_random