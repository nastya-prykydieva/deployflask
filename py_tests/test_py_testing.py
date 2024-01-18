from app.post.models import Category, Post


def test_list_posts(client, log_in_default_user):
    response = client.get('/post/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Posts" in response.data
    assert b"Type: news" in response.data


def test_list_posts_if_logged_out(client):
    response = client.get('/post/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data


def test_view_post(client, log_in_default_user):
    response = client.get('/post/1', follow_redirects=True)
    assert response.status_code == 200
    assert b"new post" in response.data


def test_create_post(client, log_in_default_user):
    data = {
        'title': 'New title',
        'text': 'New text',
        'type': 'news',
        'enabled': 'y',
        'category': 'dancing'
    }
    response = client.post('/post/create', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'New title' in response.data
    post = Post.query.filter_by(title='test').first()
    assert post is not None
    assert post.text == 'New text'


def test_update_post(client, log_in_default_user):
    data = {
        'title': 'Updated title',
        'text': 'Updated text',
        'type': 'other',
        'enabled': 'y',
        'category': 'dancing'
    }
    response = client.post('/post/1/update', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'was updated' in response.data
    post = Post.query.filter_by(title='Updated title').first()
    assert post is not None
    assert post.text == 'Updated text'


def test_update_invalid_post(client, log_in_default_user):
    data = {
        'title': 'Updated title',
        'text': 'Updated text',
        'type': 'other',
        'enabled': 'y',
        'category': 'dancing'
    }
    response = client.post('/post/1111/update', data=data, follow_redirects=True)
    assert response.status_code == 404
    assert b'was updated' not in response.data


def test_delete_post(client, log_in_default_user):
    response = client.get('post/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'was deleted' in response.data
    post = Post.query.filter_by(id=1).first()
    assert post is None


def test_delete_invalid_post(client, log_in_default_user):
    response = client.get('post/1111/delete', follow_redirects=True)
    assert response.status_code == 404
    assert b'was deleted' not in response.data


def test_list_categories(client, log_in_default_user):
    response = client.get('/post/category', follow_redirects=True)
    assert response.status_code == 200
    assert b"Categories" in response.data


def test_create_category(client, log_in_default_user):
    response = client.post('/post/category/create', data={'name': 'sport'}, follow_redirects=True)
    assert response.status_code == 200
    category = Category.query.filter_by(id=1).first()
    assert category is not None
    assert category.name == 'sport'
    assert b"The new category was added successfully" in response.data


def test_update_category(client, log_in_default_user):
    response = client.post('/post/category/1/update', data={'name': 'art'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"was edited" in response.data
    category = Category.query.filter_by(id=1).first()
    assert category is not None
    assert category.name == 'art'


def test_delete_category(client, log_in_default_user):
    response = client.get('post/category/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"was deleted" in response.data
    category = Category.query.filter_by(id=1).first()
    assert category is None


def test_list_tags(client, log_in_default_user):
    response = client.get('/post/tag', follow_redirects=True)
    assert response.status_code == 200
    assert b"Tags" in response.data
