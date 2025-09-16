#!/usr/bin/env python3
"""
Development data seeding script
Creates a default user and sample tasks for development convenience
"""
import sys
import os
from datetime import datetime, date
sys.path.append('/app')

def seed_development_data():
    try:
        from app import app, db
        from models import User, Task
        from werkzeug.security import generate_password_hash

        with app.app_context():
            # Create tables if they don't exist
            db.create_all()
            print('✅ Database tables created')
            
            # Check if default user exists
            default_user = User.query.filter_by(username='demo').first()
            
            if not default_user:
                # Create default development user
                demo_user = User(
                    username='demo',
                    email='demo@taskmanager.dev',
                    password_hash=generate_password_hash('demo123')
                )
                db.session.add(demo_user)
                db.session.commit()
                
                # Create sample tasks
                sample_tasks = [
                    # Pending tasks
                    Task(
                        title='Learn Docker fundamentals',
                        description='Complete the Docker workshop exercises and understand containerization concepts',
                        status='pending',
                        due_date=date(2025, 9, 20),
                        user_id=demo_user.id
                    ),
                    Task(
                        title='Set up development environment',
                        description='Configure Docker Compose for local development with hot reload',
                        status='pending',
                        due_date=date(2025, 9, 18),
                        user_id=demo_user.id
                    ),
                    Task(
                        title='Review Kubernetes concepts',
                        description='Prepare for tomorrow\'s Kubernetes session by reviewing container orchestration',
                        status='pending',
                        due_date=date(2025, 9, 19),
                        user_id=demo_user.id
                    ),
                    Task(
                        title='Practice Git workflows',
                        description='Master branching, merging, and pull request workflows for team collaboration',
                        status='pending',
                        user_id=demo_user.id
                    ),
                    
                    # Completed tasks
                    Task(
                        title='Install Docker Desktop',
                        description='Download and install Docker Desktop for local development',
                        status='completed',
                        user_id=demo_user.id
                    ),
                    Task(
                        title='Complete Git workshop',
                        description='Successfully completed Day 1 Git and GitHub workshop exercises',
                        status='completed',
                        user_id=demo_user.id
                    ),
                    Task(
                        title='Create GitHub account',
                        description='Set up GitHub account and configure SSH keys for secure access',
                        status='completed',
                        user_id=demo_user.id
                    ),
                    Task(
                        title='Fork demo repository',
                        description='Fork the workshop repository and clone it locally for hands-on practice',
                        status='completed',
                        user_id=demo_user.id
                    ),
                    Task(
                        title='Test Flask application',
                        description='Run the task manager application locally and verify all features work',
                        status='completed',
                        user_id=demo_user.id
                    )
                ]
                
                # Add all sample tasks
                for task in sample_tasks:
                    db.session.add(task)
                
                db.session.commit()
                
                print('👤 Created default development user:')
                print('   Username: demo')
                print('   Password: demo123')
                print('   Email: demo@taskmanager.dev')
                print('📝 Seeded sample tasks:')
                print(f'   - {len([t for t in sample_tasks if t.status == "pending"])} pending tasks')
                print(f'   - {len([t for t in sample_tasks if t.status == "completed"])} completed tasks')
                print('🌐 Access the app at: http://localhost:8000')
                return True
            else:
                # Check if user has tasks
                task_count = Task.query.filter_by(user_id=default_user.id).count()
                print('👤 Default development user already exists:')
                print('   Username: demo')
                print('   Password: demo123')
                print(f'📝 User has {task_count} existing tasks')
                print('🌐 Access the app at: http://localhost:8000')
                return False
                
    except Exception as e:
        print(f'❌ Error seeding development data: {e}')
        return False

if __name__ == '__main__':
    seed_development_data()