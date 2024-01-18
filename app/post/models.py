from app import db
from datetime import datetime
import enum


class Type(enum.Enum):
    news = 'news'
    publication = 'publication'
    other = 'other'


post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    image = db.Column(db.String, default='postdefault.jpg')
    created = db.Column(db.DateTime, default=datetime.now())
    type = db.Column(db.Enum(Type), default='news')
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', name='fk_post_category'), nullable=False)
    tags = db.relationship('Tag', secondary=post_tag, backref=db.backref('posts'))

    def __repr__(self):
        return f"Post('{self.title}', '{self.image}', '{self.created}, '{self.type}')"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    post = db.relationship('Post', backref='category')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
