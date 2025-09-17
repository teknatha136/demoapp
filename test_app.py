"""
Basic tests for the Task Manager application
Tests authentication, task CRUD operations, and API endpoints
"""
import pytest
from models import User, Task
from werkzeug.security import generate_password_hash


class TestAuthentication:
    """Test user authentication features"""
    
    def test_register_user(self, client):
        """Test user registration"""
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        })
        assert response.status_code == 302  # Redirect after successful registration
        
        # Check user was created
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'
    
    def test_register_duplicate_username(self, client, test_user):
        """Test registration with duplicate username"""
        response = client.post('/register', data={
            'username': 'testuser',  # Already exists
            'email': 'another@example.com',
            'password': 'newpass123'
        })
        assert b'Username already exists' in response.data
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code == 302  # Redirect to dashboard
    
    def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpass'
        })
        assert b'Invalid username or password' in response.data
    
    def test_logout(self, client, authenticated_user):
        """Test user logout"""
        response = client.get('/logout')
        assert response.status_code == 302  # Redirect to login
        
        # Try to access protected page
        response = client.get('/dashboard')
        assert response.status_code == 302  # Redirect to login


class TestTaskManagement:
    """Test task CRUD operations"""
    
    def test_dashboard_access(self, client, authenticated_user):
        """Test dashboard access for authenticated user"""
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'My Tasks' in response.data
    
    def test_create_task(self, client, authenticated_user):
        """Test task creation"""
        response = client.post('/task/new', data={
            'title': 'Test Task',
            'description': 'This is a test task',
            'due_date': '2025-12-31'
        })
        assert response.status_code == 302  # Redirect to dashboard
        
        # Check task was created
        task = Task.query.filter_by(title='Test Task').first()
        assert task is not None
        assert task.user_id == authenticated_user.id
        assert task.status == 'pending'
    
    def test_create_task_missing_title(self, client, authenticated_user):
        """Test task creation without title"""
        response = client.post('/task/new', data={
            'title': '',
            'description': 'This is a test task'
        })
        assert b'Task title is required' in response.data
    
    def test_edit_task(self, client, authenticated_user):
        """Test task editing"""
        # Create a task first
        task = Task(
            title='Original Title',
            description='Original description',
            user_id=authenticated_user.id
        )
        from app import db
        db.session.add(task)
        db.session.commit()
        
        # Edit the task
        response = client.post(f'/task/{task.id}/edit', data={
            'title': 'Updated Title',
            'description': 'Updated description',
            'status': 'completed'
        })
        assert response.status_code == 302  # Redirect to dashboard
        
        # Check task was updated
        updated_task = Task.query.get(task.id)
        assert updated_task.title == 'Updated Title'
        assert updated_task.status == 'completed'
    
    def test_delete_task(self, client, authenticated_user):
        """Test task deletion"""
        # Create a task first
        task = Task(
            title='Task to Delete',
            user_id=authenticated_user.id
        )
        from app import db
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        
        # Delete the task
        response = client.post(f'/task/{task_id}/delete')
        assert response.status_code == 302  # Redirect to dashboard
        
        # Check task was deleted
        deleted_task = Task.query.get(task_id)
        assert deleted_task is None


class TestAPI:
    """Test API endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'
    
    def test_toggle_task_status(self, client, authenticated_user):
        """Test AJAX task status toggle"""
        # Create a task first
        task = Task(
            title='Task to Toggle',
            status='pending',
            user_id=authenticated_user.id
        )
        from app import db
        db.session.add(task)
        db.session.commit()
        
        # Toggle status
        response = client.post(f'/api/task/{task.id}/toggle')
        assert response.status_code == 200
        assert response.json['success'] is True
        assert response.json['status'] == 'completed'
        
        # Check task status was updated
        updated_task = Task.query.get(task.id)
        assert updated_task.status == 'completed'
    
    def test_toggle_nonexistent_task(self, client, authenticated_user):
        """Test toggling nonexistent task"""
        response = client.post('/api/task/99999/toggle')
        assert response.status_code == 404


class TestSecurity:
    """Test security measures"""
    
    def test_unauthorized_dashboard_access(self, client):
        """Test accessing dashboard without authentication"""
        response = client.get('/dashboard')
        assert response.status_code == 302  # Redirect to login
    
    def test_unauthorized_task_access(self, client, test_user):
        """Test accessing another user's task"""
        # Create a task for test_user
        task = Task(
            title='Private Task',
            user_id=test_user.id
        )
        from app import db
        db.session.add(task)
        db.session.commit()
        
        # Create and login as different user
        other_user = User(
            username='otheruser',
            email='other@example.com',
            password_hash=generate_password_hash('otherpass')
        )
        db.session.add(other_user)
        db.session.commit()
        
        client.post('/login', data={
            'username': 'otheruser',
            'password': 'otherpass'
        })
        
        # Try to access the task
        response = client.get(f'/task/{task.id}/edit')
        assert response.status_code == 404  # Should not be found


if __name__ == '__main__':
    pytest.main(['-v'])