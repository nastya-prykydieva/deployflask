import pytest
from app import create_app, db, bcrypt
from app.auth.models import User
from app.post.models import Post, Category, Tag


@pytest.fixture(scope='module')
def client():
    app = create_app('test')

    with app.app_context():
        db.create_all()
        user = User(username='user', email='user@gmail.com', password=bcrypt.generate_password_hash('qwerty'))
        post = Post(title='new post', text='it is a new post', type='news', user_id=1, category_id=1)
        category = Category(name='dancing')
        tag = Tag(name='info')
        db.session.add_all([user, post, category, tag])
        db.session.commit()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def log_in_default_user(client):
    client.post('/login/', data={'email': 'user@gmail.com', 'password': 'qwerty'})
    yield
    client.get("/logout/")
