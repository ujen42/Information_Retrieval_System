"""
    classes map to database
"""

from config.dbconfig import db


class Paper(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(1000), nullable=False)
    link = db.Column(db.String(1000), nullable=False)
    published_date = db.Column(db.String(120), nullable=True)
    authors = db.relationship('Author', backref='paper')


class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    profile_link = db.Column(db.String(1000), nullable=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id', ondelete='CASCADE'))