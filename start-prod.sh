#!/bin/bash
set -e

echo "🚀 Starting Task Manager in Production Mode..."

# Wait for database to be ready
echo "⏳ Waiting for database..."
while ! pg_isready -h db -p 5432 -U postgres 2>/dev/null; do
    echo "Database not ready, waiting..."
    sleep 1
done

echo "✅ Database is ready!"

# Initialize database (create database if needed, then tables)
echo "📊 Initializing database..."
python init_db.py

# Start the application with Gunicorn
echo "🌐 Starting Flask application with Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 --keep-alive 2 app:app