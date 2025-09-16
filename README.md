# 📋 Task Manager - DevOps Learning Application
# new changes added
A 3-tier Task Management application for teaching DevOps concepts. Features user authentication, task CRUD operations, and modern deployment practices.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-✓-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-✓-blue)

## 🌟 Features
- ✅ **User Authentication** - Secure login/registration with password hashing
- ✅ **Task Management** - Complete CRUD operations for tasks
- ✅ **Real-time Updates** - AJAX-powered status toggling
- ✅ **Responsive UI** - Mobile-friendly Tailwind CSS interface
- 🐳 **Docker Ready** - Development containers with hot reload
- ☸️ **Kubernetes Deployments** - Production-ready manifests
- 🔄 **CI/CD Pipeline** - Automated testing and deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│                 │    │                 │    │                 │
│ • HTML/Tailwind │───▶│ • Flask App     │───▶│ • PostgreSQL    │
│ • JavaScript    │    │ • SQLAlchemy    │    │ • External VM   │
│ • AJAX          │    │ • Authentication│    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Local Development Setup

### Prerequisites
- Docker and Docker Compose
- Git

### Quick Start
```bash
# Clone and navigate to the project
git clone <repository-url>
cd task-manager/app

# Copy environment variables
cp .env.example .env

# Start all services (database will be auto-initialized)
docker-compose up --build

# Access at http://localhost:8000
# Demo login: demo / demo123
```

### Database Initialization

The application handles database setup automatically:

**For Development (Docker Compose):**
- Tables created automatically on first run
- Demo user and sample tasks inserted via `init_db.py`
- Database ready check ensures proper startup sequence
- No manual setup required

**For Production with Flask-Migrate:**
```bash
# Initialize migrations (first time only)
python setup_migrations.py

# For schema changes
flask db migrate -m "Description of changes"
flask db upgrade
```

### Manual Python Setup (Optional)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL container
docker run -d --name taskmanager-db \
  -e POSTGRES_USER=todouser \
  -e POSTGRES_PASSWORD=todopass \
  -e POSTGRES_DB=todoapp \
  -p 5432:5432 postgres:15-alpine

# Run the application
python app.py
```

## 🧪 Testing
```bash
# Run tests with coverage
docker-compose run web pytest --cov=. --cov-report=html
```

## 📦 Production Deployment

### Prerequisites
- Kubernetes cluster
- PostgreSQL database (external VM)
- Docker registry access

### Build and Deploy
```bash
# Build production image
docker build -t taskmanager:latest .

# Push to your registry
docker push your-registry/taskmanager:latest

# Update image in k8s/02-web-app.yaml
# Update DATABASE_URL in k8s/00-namespace-secrets.yaml

# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment
kubectl get pods -n taskmanager
```

### Required Environment Variables
- `DATABASE_URL`: PostgreSQL connection to external VM
- `SECRET_KEY`: Secure random key for Flask sessions

## 🔧 Key Features
- **Security**: Password hashing, CSRF protection, input validation
- **CI/CD**: Separate workflows for testing and deployment
- **Scalability**: Kubernetes HPA, resource management
- **Health Monitoring**: Built-in health checks and probes

## 🗂️ Project Structure
```
task-manager/
├── app.py                    # Main Flask application
├── models.py                 # Database models
├── templates/                # HTML templates
├── static/                   # CSS/JS assets
├── k8s/                     # Kubernetes manifests
├── .github/workflows/       # CI/CD pipelines
├── Dockerfile               # Production container
├── Dockerfile.dev          # Development container
├── docker-compose.yml      # Local development
└── requirements.txt        # Python dependencies
```

## 🛠️ Development Tips
- Use `docker-compose logs -f web` to follow application logs
- Reset database: `docker-compose down -v && docker-compose up -d`
- Access pgAdmin at http://localhost:8080 (admin@taskmanager.local / admin123)

---

**Happy Learning! 🚀**
