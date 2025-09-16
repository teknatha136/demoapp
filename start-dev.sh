#!/bin/bash
set -e

echo "🔄 Starting Task Manager Development Server..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "✅ PostgreSQL is ready!"

# Start Flask development server
# The Flask app will handle database initialization on first request
echo "🌟 Starting Flask development server..."
exec python app.py