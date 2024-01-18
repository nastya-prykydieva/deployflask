from app import db, login_manager
from flask_login import UserMixin
from flask_bcrypt import check_password_hash, generate_password_hash
from datetime import datetime
from app.post.models import Post


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(128), nullable=False)
    about_me = db.Column(db.String(500))
    last_seen = db.Column(db.DateTime, default=datetime.now())
    post = db.relationship('Post', backref='user')

    @property
    def password(self):
        return AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, psw):
        self.password_hash = generate_password_hash(psw).decode('utf-8')

    def verify_password(self, psw):
        return check_password_hash(self.password_hash, psw)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
