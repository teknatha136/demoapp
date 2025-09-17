#!/usr/bin/env python3
"""
Simple database initialization script
Creates database if it doesn't exist, then creates tables
"""
import os
from sqlalchemy_utils import database_exists, create_database

def init_database():
    """Create database if it doesn't exist, then create tables"""
    database_url = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/taskmanager')
    
    # Create database if it doesn't exist
    if not database_exists(database_url):
        print(f"Creating database...")
        create_database(database_url)
        print("✅ Database created")
    else:
        print("✅ Database already exists")
    
    # Create tables using Flask app
    from app import app, db
    with app.app_context():
        db.create_all()
        print("✅ Tables created")
if __name__ == '__main__':
    init_database()