"""
Database models for the Task Management application
Includes User and Task models with relationships
"""
from flask_login import UserMixin
from datetime import datetime

# Database instance will be set by app.py
db = None

def init_models(database):
    """Initialize models with database instance"""
    global db
    db = database
    
    # Define the classes with the correct db instance
    class User(UserMixin, db.Model):
        """User model for authentication and task ownership"""
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False, index=True)
        email = db.Column(db.String(120), unique=True, nullable=False, index=True)
        password_hash = db.Column(db.String(255), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # Relationship with tasks
        tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
        
        def __repr__(self):
            return f'<User {self.username}>'
        
        def get_task_stats(self):
            """Get statistics for user's tasks"""
            total = len(self.tasks)
            completed = len([task for task in self.tasks if task.status == 'completed'])
            pending = total - completed
            return {
                'total': total,
                'completed': completed,
                'pending': pending,
                'completion_rate': round((completed / total * 100) if total > 0 else 0, 1)
            }

    class Task(db.Model):
        """Task model for todo items"""
        __tablename__ = 'tasks'
        
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        description = db.Column(db.Text, nullable=True)
        status = db.Column(db.String(20), nullable=False, default='pending')  # pending, completed
        due_date = db.Column(db.Date, nullable=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # Foreign key to user
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        
        def __repr__(self):
            return f'<Task {self.title}>'
        
        def to_dict(self):
            """Convert task to dictionary for API responses"""
            return {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'status': self.status,
                'due_date': self.due_date.isoformat() if self.due_date else None,
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat(),
                'user_id': self.user_id
            }

    # Make classes available at module level
    globals()['User'] = User
    globals()['Task'] = Task
    
    return User, Task