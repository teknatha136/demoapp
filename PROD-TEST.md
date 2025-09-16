# 🚀 Production Test Environment

This directory contains a production-like testing environment that mimics the actual production deployment using the production Dockerfile and proper production configurations.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask App     │    │   PostgreSQL    │    │   Health Check  │
│   (Port 8000)   │───▶│   (Port 5433)   │    │   Endpoint      │
│   Production    │    │   Production    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## ⚙️ Configuration

### Production-like Settings:
- ✅ **FLASK_ENV=production** (No demo account, clean UI)
- ✅ **FLASK_DEBUG=0** (No debug information exposed)
- ✅ **Gunicorn WSGI server** (Production-grade server)
- ✅ **Non-root container user** (Security best practice)
- ✅ **Resource limits** (CPU and memory constraints)
- ✅ **Health checks** (Container monitoring)

## 🚀 Quick Start

### 1. Initial Setup
```bash
# Create environment file and set secure passwords
cp .env.example .env.prod

# Edit the generated .env.prod file
nano .env.prod
```

### 2. Start Production Test Environment
```bash
# Build and start all services
docker-compose -f docker-compose.prod-test.yml up --build

# Check status
docker-compose -f docker-compose.prod-test.yml ps
```

### 3. Access the Application
- **Main App**: http://localhost:8000
- **Database**: localhost:5433 (PostgreSQL)

### 4. Run Tests
```bash
# Run connectivity and health tests
curl http://localhost:8000/health
```

### 5. Monitor and Debug
```bash
# View logs
docker-compose -f docker-compose.prod-test.yml logs -f

# Open shell in web container
docker-compose -f docker-compose.prod-test.yml exec web bash

# Connect to database
docker-compose -f docker-compose.prod-test.yml exec db psql -U postgres -d todoapp_prod
```

### 6. Cleanup
```bash
# Stop services
docker-compose -f docker-compose.prod-test.yml down

# Complete cleanup (removes volumes)
docker-compose -f docker-compose.prod-test.yml down -v
```

## 📁 Files

- `docker-compose.prod-test.yml` - Production test compose configuration

## 🔒 Security Features

### Container Security:
- Non-root user (appuser)
- Minimal attack surface
- Resource constraints

## 🔧 Customization

### Environment Variables (.env.prod):
```bash
DB_PASSWORD=your-secure-database-password
SECRET_KEY=your-super-secret-flask-key
```

### Resource Limits:
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
```

## 🧪 Testing Production Features

### No Demo Account:
- ✅ Clean login page (no demo credentials visible)
- ✅ No demo user created in database
- ✅ Fresh production-like start

### Performance Testing:
```bash
# Load testing with curl
for i in {1..100}; do curl http://localhost:8000/health & done

# Monitor resources
docker stats
```

### Database Testing:
```bash
# Connect to production database
docker-compose -f docker-compose.prod-test.yml exec db psql -U postgres -d todoapp_prod

# Check tables (should be empty initially)
\dt
```

## 🚨 Important Notes

1. **Not for actual production**: This is for testing production-like behavior
2. **Change passwords**: Always update .env.prod with secure passwords  
3. **Resource monitoring**: Check CPU and memory usage during tests
4. **Clean up**: Use `docker-compose down -v` to remove test data

## 🔄 CI/CD Integration

This environment can be used in CI/CD pipelines to test production builds:

```yaml
# Example GitHub Actions step
- name: Test Production Build
  run: |
    docker-compose -f docker-compose.prod-test.yml up --build -d
    sleep 30
    curl http://localhost:8000/health
    docker-compose -f docker-compose.prod-test.yml down -v
```