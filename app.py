"""
Main Flask application entry point
Handles app initialization, configuration, and routing
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://todouser:todopass@localhost:5432/todoapp')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import and initialize models with database instance
from models import init_models
User, Task = init_models(db)

# Initialize Flask-Migrate after models are imported
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))

# Routes
@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise to login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Basic validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('register.html')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            app.logger.error(f"Registration error: {e}")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - display user's tasks"""
    status_filter = request.args.get('status', 'all')
    
    # Base query for current user's tasks
    query = Task.query.filter_by(user_id=current_user.id)
    
    # Apply status filter
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    # Order by due date and creation date
    tasks = query.order_by(Task.due_date.asc(), Task.created_at.desc()).all()
    
    # Get task counts for filter buttons
    task_counts = {
        'all': Task.query.filter_by(user_id=current_user.id).count(),
        'pending': Task.query.filter_by(user_id=current_user.id, status='pending').count(),
        'completed': Task.query.filter_by(user_id=current_user.id, status='completed').count()
    }
    
    return render_template('dashboard.html', 
                         tasks=tasks, 
                         status_filter=status_filter,
                         task_counts=task_counts)

@app.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    """Create a new task"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date_str = request.form.get('due_date', '')
        
        # Validation
        if not title:
            flash('Task title is required', 'error')
            return render_template('task_form.html', task=None)
        
        # Parse due date
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid due date format', 'error')
                return render_template('task_form.html', task=None)
        
        # Create task
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            user_id=current_user.id
        )
        
        try:
            db.session.add(task)
            db.session.commit()
            flash('Task created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to create task. Please try again.', 'error')
            app.logger.error(f"Task creation error: {e}")
    
    return render_template('task_form.html', task=None)

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit an existing task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date_str = request.form.get('due_date', '')
        status = request.form.get('status', 'pending')
        
        # Validation
        if not title:
            flash('Task title is required', 'error')
            return render_template('task_form.html', task=task)
        
        # Parse due date
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid due date format', 'error')
                return render_template('task_form.html', task=task)
        
        # Update task
        task.title = title
        task.description = description
        task.due_date = due_date
        task.status = status
        task.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update task. Please try again.', 'error')
            app.logger.error(f"Task update error: {e}")
    
    return render_template('task_form.html', task=task)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete task. Please try again.', 'error')
        app.logger.error(f"Task deletion error: {e}")
    
    return redirect(url_for('dashboard'))

@app.route('/api/task/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task_status(task_id):
    """AJAX endpoint to toggle task status"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    
    # Toggle status
    task.status = 'completed' if task.status == 'pending' else 'pending'
    task.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'status': task.status,
            'message': f'Task marked as {task.status}'
        })
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Task toggle error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to update task status'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

if __name__ == '__main__':
    # Initialize database and demo data on startup
    with app.app_context():
        print("📁 Creating database tables...")
        db.create_all()
        print("🎉 Database initialization completed!")
    
    # Run the app on port 8000 to match docker-compose
    app.run(host='0.0.0.0', port=8000, debug=True)