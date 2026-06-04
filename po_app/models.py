from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from po_app import app, db, login
from flask import send_file, current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
import os
import json
import exif
from datetime import datetime

class SerializerMixin:
    def to_dict(self):
        data = {}
        for col in self.__table__.columns:
            value = getattr(self, col.name)
            if isinstance(value, datetime):
                data[col.name] = value.isoformat()
            else:
                data[col.name] = value
        return data

class PO(SerializerMixin, db.Model):
    zip: so.Mapped[int] = so.mapped_column(primary_key=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True)
    street: so.Mapped[str] = so.mapped_column(sa.String(64))
    state: so.Mapped[str] = so.mapped_column(sa.String(2))
    visited: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=True)
    visited_date: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)
    latitude: so.Mapped[str] = so.mapped_column(sa.String(10), nullable=True)
    longitude: so.Mapped[str] = so.mapped_column(sa.String(10), nullable=True)    

    def __repr__(self):
        return '<Post Office {} {}>'.format(self.zip, self.city)
    
    @property
    def po_pic(self):
       pic = ''.join(word.capitalize() for word in self.city.split(' ')) + ".jpg"
       return pic
        
    def get_random_post_offices():
        po_list = db.select(PO).where(PO.visited).order_by(func.random()).limit(4)
        po_random = db.session.scalars(po_list).all()
        return po_random
    
    def po_count():
        count = db.session.scalar(db.select(func.count(PO.zip)).where(PO.visited == True))
        return count
    
    def po_chart():
        query = db.session.query(
            sa.func.extract('year', PO.visited_date).label('year'),
            sa.func.count(PO.zip).label('count')
        ).filter(PO.visited_date.isnot(None))\
         .group_by('year')\
         .order_by('year').all()
        
        years = []
        counts = []
        running_counts = []
        running_total = 0
        
        for row in query:
            year = str(int(row.year))
            count = row.count
            running_total += count
            
            years.append(year)
            counts.append(count)
            running_counts.append(running_total)    

        return years, counts, running_counts
    
    def update_po(zip):
        po = db.first_or_404(sa.select(PO).where(PO.zip == zip))

        image_path = os.path.join(current_app.config.get('STATIC_PATH'), 'static', po.city.title() + ".jpg")

        if os.path.isfile(image_path):
            visited_date_input = datetime.now()

            with open(image_path, 'rb') as image_file:
                exif_data = exif.Image(image_file)
                if exif_data.has_exif:   
                    if exif_data.get("datetime"):
                        visited_date_input = datetime.strptime(exif_data.datetime, "%Y:%m:%d %H:%M:%S")

            po.visited = True
            po.visited_date = visited_date_input
            db.session.commit()

    def prepare_backups():
        records = db.session.scalars(sa.select(PO)).all()
        backup_data = [record.to_dict() for record in records]
        
        with open('data/po_backup.json', 'w') as f:
            json.dump(backup_data, f, indent=4)
            
        open('data/needs_backup','w')

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
