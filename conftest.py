"""
Test configuration and fixtures for pytest
"""
import pytest
from app import app, db
from models import User, Task
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    """Create database tables once per test session"""
    with app.app_context():
        db.create_all()
        yield
        # Clean up after all tests
        db.drop_all()

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            # Clean up any existing data
            db.session.remove()
            # Truncate all tables
            db.session.execute(db.text('TRUNCATE TABLE users, tasks RESTART IDENTITY CASCADE'))
            db.session.commit()
            yield client

@pytest.fixture
def test_user():
    """Create a test user"""
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash=generate_password_hash('testpass123')
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def authenticated_user(client, test_user):
    """Log in a test user"""
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    })
    return test_user