import unittest
from flask_testing import TestCase
from app import create_app
from flask import url_for
from flask_login import current_user
from app import db
from app.auth.models import User
from app.todo.models import Todo


class MyTest(TestCase):
    def create_app(self):
        app = create_app('test')
        return app

    def setUp(self):
        db.create_all()
        user = User(username='user', email='user@gmail.com', password='password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_setup(self):
        """Test to check the setup before running the tests."""
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)

    def test_about_page(self):
        """View test to check access to the 'about' page."""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Anastasiia', response.data)

    def test_contact_page(self):
        """View test to check access to the 'contact' page."""
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact me', response.data)

    def test_ipz_page(self):
        """View test to check access to the 'ipz' page."""
        response = self.client.get('/ipz')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Vasyl Stefanyk', response.data)

    def test_skills_with_index(self):
        """View test to check access to the 'skill' page."""
        response = self.client.get('/skills/3')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'English', response.data)

    def test_skills_page(self):
        """View test to check access to the 'skills' page."""
        response = self.client.get('/skills')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Python', response.data)

    def test_register_page(self):
        """View test to check access to the 'register' page."""
        with self.client:
            response = self.client.get(url_for('auth.register'))
            self.assertIn(b'Register', response.data)

    def test_login_page(self):
        """View test to check access to the 'login' page."""
        with self.client:
            response = self.client.get(url_for('auth.login'))
            self.assertIn(b'Remember Me', response.data)

    def test_add_BD(self):
        """Test to add the new record to the User table."""
        user = User(username='user_test', email='user_test@gmail.com', password='password_test')
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username='user').first()
        self.assertEqual(user.username, 'user')
        self.assertEqual(user.email, 'user@gmail.com')
        self.assertNotEqual(user.password, 'password')
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        """Test to ensure that register behaves correctly."""
        with self.client:
            response = self.client.post(
                url_for('auth.register'),
                data=dict(username='user', email='user@gmail.com', password='password', confirm_password='password'),
                follow_redirects=True
            )
            self.assertIn(b'Account created', response.data)
            user = User.query.filter_by(email='user@gmail.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(user.email, 'user@gmail.com')

    def test_login_user(self):
        """Test to ensure that login behaves correctly with correct credentials."""
        with self.client:
            response = self.client.post(
                url_for('auth.login'),
                data=dict(email='user@gmail.com', password='password', remember=True),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(current_user.is_authenticated, True)
            self.assertIn(b'You have been logged in!', response.data)

    def test_login_user_incorrect(self):
        """Test to ensure that login behaves correctly with incorrect credentials."""
        with self.client:
            response = self.client.post(
                url_for('auth.login'),
                data=dict(email='user11111@gmail.com', password='password', remember=True),
                follow_redirects=True
            )
            self.assertEqual(current_user.is_authenticated, False)
            self.assertIn(b'Error! Please try again.', response.data)

    def test_logout_user(self):
        """Test to ensure that logout behaves correctly."""
        self.test_login_user()
        with self.client:
            response = self.client.get(url_for('auth.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(current_user.is_authenticated)
            self.assertIn(b'You have been logged out', response.data)

    def test_update_account(self):
        """Test to ensure that accounts info can be updated or changed correctly."""
        self.test_login_user()
        data = {
            'username': 'updated',
            'email': 'updated@gmail.com',
            'about_me': 'Updated info'
        }
        with self.client:
            response = self.client.post(url_for('auth.account'), data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Account', response.data)
            upd_user = User.query.filter_by(username='updated').first()
            self.assertIsNotNone(upd_user)
            self.assertEqual(upd_user.email, 'updated@gmail.com')
            self.assertEqual(upd_user.about_me, 'Updated info')

    def test_todo_page(self):
        """View test to check access to the To Do page."""
        response = self.client.get(url_for('todo_bp.todo'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'To do', response.data)

    def test_create_todo(self):
        """Test to create the new record in the 'To do' table."""
        with self.client:
            response = self.client.post(url_for('todo_bp.add'),
                                        data=dict(title='Test', description='Write test'),
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            todo = Todo.query.filter_by(id=1).first()
            self.assertEqual(todo.description, 'Write test')

    def test_update_todo(self):
        """Test to update the record in the 'To do' table."""
        todo_1 = Todo(title='title1', description='description1', complete=False)
        db.session.add(todo_1)
        db.session.commit()
        with self.client:
            response = self.client.get(url_for('todo_bp.update', id=1), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            todo = Todo.query.filter_by(id=1).first()
            self.assertTrue(todo.complete)

    def test_delete_todo(self):
        """Test to delete the record in the 'To do' table."""
        with self.client:
            response = self.client.post(url_for('todo_bp.delete', id=1), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            todo = Todo.query.filter_by(id=1).first()
            self.assertIsNone(todo)

    def test_list_todo(self):
        """Test to check the number of records in the To Do list."""
        todo_1 = Todo(title='title1', description='description1', complete=False)
        todo_2 = Todo(title='title2', description='description2', complete=False)
        db.session.add_all([todo_1, todo_2])
        all_todo = Todo.query.count()
        self.assertEqual(all_todo, 2)


if __name__ == '__main__':
    unittest.main()
