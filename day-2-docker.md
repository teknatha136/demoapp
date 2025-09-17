# Docker in Development
## Day 2 - Containerization & Docker Compose

---

## Learning Objectives
By the end of this session,
- Understand containerization concepts and Docker fundamentals
- Build custom Docker images from base images using Dockerfiles
- Optimize Docker images with multi-stage builds and best practices
- Use Docker Compose to manage multi-container applications
- Apply Docker in real development workflows (development vs production)
- Prepare applications for Kubernetes deployment

---

## Session Structure

### **Part 1: Docker Fundamentals**
#### Docker Introduction & Concepts
#### Building Custom Docker Images  
#### Hands-on: Your First Container

### **Part 2: Advanced Docker**
#### Break
#### Multi-stage Builds & Production Optimization
#### Docker Networking, Volumes & Environment Management

### **Part 3: Docker Compose & Workflows**
#### Docker Compose: Multi-container Applications
#### Development vs Production & Next Steps

---

## Part 1: Docker Fundamentals

### Docker Introduction & Concepts

#### What is Docker?
Docker is a **containerization platform** used to develop, ship, and run containers. Docker doesn't use a hypervisor, and you can run Docker on your desktop or laptop for development and testing.

#### What is a Container?
A **container** is a loosely isolated environment that allows us to build and run software packages. These software packages include the code and all dependencies to run applications quickly and reliably on any computing environment.

#### Why Docker Matters
Docker solves common development challenges:
- **Environment Consistency**: Same container runs identically across dev, staging, and production
- **Dependency Management**: All libraries and dependencies packaged together
- **Resource Efficiency**: Lightweight alternative to virtual machines
- **Application Portability**: Move applications between different hosting environments easily

#### Docker vs Virtual Machines

**Traditional VMs:**
```
[App A] [App B] [App C]
[  OS  ] [  OS  ] [  OS  ]
[    Hypervisor (VMware)   ]
[       Host Operating System       ]
[           Physical Hardware       ]
```

**Docker Containers:**
```
[App A] [App B] [App C]
[    Docker Engine    ]
[  Host Operating System  ]
[    Physical Hardware    ]
```

**Key Advantages of Containers:**
- **Lightweight**: Share the host OS kernel, no need for separate OS per application
- **Fast Startup**: Containers start in seconds vs minutes for VMs
- **Efficient Resource Usage**: Lower memory and CPU overhead
- **Consistency**: Same container runs identically across environments
- **Portability**: Run anywhere Docker is supported

#### Key Docker Concepts
- **Image**: Blueprint/template for containers (like a class in programming)
- **Container**: Running instance of an image (like an object)  
- **Dockerfile**: Text file with instructions to build an image
- **Registry**: Repository for Docker images (Docker Hub, GitHub Container Registry)

### Building Custom Docker Images

#### Understanding Dockerfiles

**Basic Dockerfile Structure:**
```dockerfile
# Base image - starting point
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy files from host to container
COPY requirements.txt .

# Run commands during build
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port (documentation)
EXPOSE 8000

# Command to run when container starts
CMD ["python", "app.py"]
```

#### Dockerfile Instructions Explained
- **FROM**: Base image (always first instruction)
- **WORKDIR**: Sets working directory for subsequent instructions
- **COPY**: Copies files/folders from host to container
- **ADD**: Similar to COPY but supports URLs and auto-extraction of archives
- **RUN**: Executes commands during image build
- **CMD**: Default command when container starts (can be overridden)
- **ENTRYPOINT**: Command that always runs when container starts
- **EXPOSE**: Documents which ports the application uses
- **ENV**: Sets environment variables
- **ARG**: Defines build-time variables
- **LABEL**: Adds metadata to image
- **USER**: Sets user for subsequent instructions
- **VOLUME**: Creates mount points for external volumes
- **ONBUILD**: Instructions to run when image is used as base for another build
- **STOPSIGNAL**: Sets system call signal for container exit
- **HEALTHCHECK**: Instructions for checking container health
- **SHELL**: Override default shell for RUN commands

#### Key Dockerfile Instruction Comparisons

**COPY vs ADD:**
| Aspect                 | COPY                                  | ADD                                         |
| ---------------------- | ------------------------------------- | ------------------------------------------- |
| **Purpose**            | Copy files/folders from build context | Copy files + additional features            |
| **Local Files**        | ✅ Yes                                 | ✅ Yes                                       |
| **URLs**               | ❌ No                                  | ✅ Yes (downloads from URL)                  |
| **Archive Extraction** | ❌ No                                  | ✅ Yes (auto-extracts .tar files)            |
| **Best Practice**      | Preferred for simple file copying     | Use only when you need URL/extraction       |
| **Example**            | `COPY app.py /app/`                   | `ADD https://example.com/file.tar.gz /tmp/` |

   


**CMD vs ENTRYPOINT:**
| Aspect                    | CMD                                         | ENTRYPOINT                                        |
| ------------------------- | ------------------------------------------- | ------------------------------------------------- |
| **Override Behavior**     | Can be overridden by `docker run` arguments | Cannot be overridden (arguments are passed to it) |
| **Usage**                 | Default command for container               | Fixed command that always runs                    |
| **Multiple Instructions** | Only last CMD is used                       | Only last ENTRYPOINT is used                      |
| **Best Practice**         | Use for default commands                    | Use for containers that act like executables      |
| **Example**               | `CMD ["python", "app.py"]`                  | `ENTRYPOINT ["python", "app.py"]`                 |

**Practical Examples:**

**Using CMD (can be overridden):**
```dockerfile
# Dockerfile with CMD
FROM python:3.11-slim
COPY app.py .
CMD ["python", "app.py"]
```
```bash
# Default behavior - runs app.py
docker run myapp

# Override - runs different command instead
docker run myapp python debug.py
docker run myapp /bin/bash
# CMD is completely ignored when arguments are provided
```

**Using ENTRYPOINT (arguments are passed to it):**
```dockerfile
# Dockerfile with ENTRYPOINT  
FROM python:3.11-slim
COPY app.py .
ENTRYPOINT ["python", "app.py"]
```
```bash
# Default behavior - runs app.py
docker run myapp

# Arguments are passed TO the python app.py command
docker run myapp --debug
docker run myapp --config prod.json
# Results in: python app.py --debug
# Results in: python app.py --config prod.json
```

**Best Pattern - ENTRYPOINT + CMD combination:**
```dockerfile
# Most flexible approach
FROM python:3.11-slim  
COPY app.py .
ENTRYPOINT ["python", "app.py"]
CMD ["--help"]  # Default arguments
```
```bash
# Shows help by default
docker run myapp
# Equivalent to: python app.py --help

# Pass custom arguments
docker run myapp --mode production
# Equivalent to: python app.py --mode production
```

**ENV vs ARG:**
| Aspect          | ENV                                 | ARG                             |
| --------------- | ----------------------------------- | ------------------------------- |
| **Scope**       | Available during build AND runtime  | Only available during build     |
| **Persistence** | Environment variable in final image | Not in final image              |
| **Override**    | Can be overridden at runtime        | Can be overridden at build time |
| **Usage**       | Configuration that containers need  | Build-time customization        |
| **Example**     | `ENV FLASK_ENV=production`          | `ARG PYTHON_VERSION=3.11`       |

#### Key Dockerfile Best Practices
- **Use COPY over ADD** unless you specifically need URL downloading or archive extraction
- **Use ENTRYPOINT for executable containers**, CMD for default arguments
- **Use ENV for runtime configuration**, ARG for build-time parameters
- **Use specific base image tags** (e.g., `python:3.11-slim` not `python:latest`)
- **Minimize layers** by combining RUN commands with `&&`
- **Order instructions by change frequency** (least to most likely to change)
- **Use .dockerignore** to exclude unnecessary files
- **Run as non-root user** for security
- **Use multi-stage builds** for smaller production images

#### Exercise 1: Build Simple Flask Container

**Step 1: Create Basic Dockerfile**
```dockerfile
# Simple Flask app container
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 8000

# Run the Flask app
CMD ["python", "app.py"]
```

**Step 2: Development Dockerfile (Real Project Dev Version)**
Now let's look at the actual development Dockerfile we'll use:
```dockerfile
# Development Dockerfile  
# Optimized for development with hot reload and debugging
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including netcat for database health check
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make start script executable
RUN chmod +x /app/start-dev.sh

# Expose port
EXPOSE 8000

# Set environment variables for development
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONPATH=/app

# Start with initialization script
CMD ["/app/start-dev.sh"]
```

**Step 3: Build the Images**
```bash
# Build simple version
docker build -t taskmanager:basic .

# Build development version (using Dockerfile.dev)
docker build -f Dockerfile.dev -t taskmanager:dev .

# List images
docker images

# Check image details
docker inspect taskmanager:dev
```

### Hands-on: Your First Container

#### Exercise 2: Run and Interact with Container

**Step 1: Run Container**
```bash
# Run container with port mapping (development version)
docker run -p 8000:8000 --name my-taskmanager taskmanager:dev

# Run in background (detached mode)
docker run -d -p 8000:8000 --name my-taskmanager-bg taskmanager:dev
```

**Step 2: Container Management**
```bash
# List running containers
docker ps

# View container logs
docker logs my-taskmanager-bg

# Execute commands inside running container
docker exec -it my-taskmanager-bg /bin/bash

# Inside container:
ps aux              # See running processes
ls -la /app         # List app files
env                 # Check environment variables
exit                # Leave container

# Stop and remove container
docker stop my-taskmanager-bg
docker rm my-taskmanager-bg
```

**Step 3: Container Inspection**
```bash
# View container resource usage
docker stats

# View container details
docker inspect my-taskmanager-bg

# View port mappings
docker port my-taskmanager-bg
```

---

## Part 2: Advanced Docker

### Multi-stage Builds & Production Optimization

#### Why Multi-stage Builds?
- **Reduce image size** by excluding build tools from final image
- **Improve security** by minimizing attack surface
- **Separate build and runtime environments**

#### Exercise 3: Production-Ready Dockerfile

**Multi-stage Production Dockerfile:**
```dockerfile
# Stage 1: Build stage
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies to user directory
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production stage
FROM python:3.11-slim

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --uid 1000 appuser

WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application code with proper ownership
COPY --chown=appuser:appuser . .

# Make startup script executable
RUN chmod +x /app/start-prod.sh

# Switch to non-root user
USER appuser

# Set production environment variables
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Use production startup script
CMD ["/app/start-prod.sh"]
```

#### Docker Build Optimization Tips
```bash
# Build with build arguments
docker build --build-arg ENV=production -t taskmanager:prod .

# Use BuildKit for better performance
DOCKER_BUILDKIT=1 docker build -t taskmanager:optimized .

# Check image layers and sizes
docker history taskmanager:prod

# Compare image sizes
docker images | grep taskmanager
```

#### Exercise 4: Publishing Images to Docker Hub

**Why Push to Docker Hub?**
- **Share your images** with teammates and the community
- **Deploy anywhere** - pull images on any Docker-enabled system
- **Version control** for container images
- **Professional practice** - essential for real-world deployments

**Step 1: Create Docker Hub Account**
1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up for a free account (remember your username!)
3. Verify your email address

**Step 2: Create a Public Repository**
1. Click "Create Repository"
2. Repository name: `taskmanager-workshop`
3. Description: "Flask Task Manager from DevOps Workshop"
4. Visibility: **Public** (free tier)
5. Click "Create"

**Step 3: Login and Tag Your Image**
```bash
# Login to Docker Hub (enter your credentials when prompted)
docker login

# Tag your production image with your Docker Hub username
# Format: docker tag local-image:tag username/repository:tag
docker tag taskmanager:prod YOUR_DOCKERHUB_USERNAME/taskmanager-workshop:v1.0.0

# You can also tag as 'latest'
docker tag taskmanager:prod YOUR_DOCKERHUB_USERNAME/taskmanager-workshop:latest

# Verify the tags were created
docker images | grep YOUR_DOCKERHUB_USERNAME
```

**Step 4: Push to Docker Hub**
```bash
# Push specific version
docker push YOUR_DOCKERHUB_USERNAME/taskmanager-workshop:v1.0.0

# Push latest tag
docker push YOUR_DOCKERHUB_USERNAME/taskmanager-workshop:latest

# View the upload progress
# This shows the layered nature of Docker images!
```

**Step 5: Verify and Test**
```bash
# Remove local images to test pull
docker rmi YOUR_DOCKERHUB_USERNAME/taskmanager-workshop:latest
docker rmi taskmanager:prod

# Pull from Docker Hub (anyone can do this now!)
docker pull YOUR_DOCKERHUB_USERNAME/taskmanager-workshop:latest

# Run the pulled image
docker run -p 8000:8000 YOUR_DOCKERHUB_USERNAME/taskmanager-workshop:latest
```

**Step 6: Share Your Image**
Your image is now publicly available! Share the pull command:
```bash
# Anyone can now run your application with:
docker pull YOUR_DOCKERHUB_USERNAME/taskmanager-workshop:latest
docker run -p 8000:8000 YOUR_DOCKERHUB_USERNAME/taskmanager-workshop:latest
```

**Best Practices for Image Naming:**
```bash
# Use semantic versioning
docker tag myapp:latest username/myapp:v1.2.3

# Include environment info
docker tag myapp:prod username/myapp:production
docker tag myapp:dev username/myapp:development  

# Use meaningful tags
docker tag myapp:latest username/myapp:2025-workshop
```

**Real-world Applications:**
- **CI/CD Pipelines:** Automatically build and push images
- **Team Collaboration:** Share consistent development environments
- **Deployment:** Pull production images on servers
- **Version Management:** Tag releases for rollback capabilities

### Docker Networking, Volumes & Environment Management

#### Container Networking Basics

**Network Types:**
- **Bridge**: Default network for containers on same host
- **Host**: Use host network directly (no isolation)
- **None**: No networking
- **Custom**: User-defined networks for better isolation

**Networking Commands:**
```bash
# List networks
docker network ls

# Create custom network
docker network create taskmanager-network

# Run containers on same network
docker run -d --name taskmanager-db --network taskmanager-network postgres:15-alpine
docker run -d --name taskmanager-web --network taskmanager-network -p 8000:8000 taskmanager:prod

# Containers can communicate by name
# web container can reach database at: taskmanager-db:5432
```

#### Volume Management

**Types of Data Persistence:**
- **Bind mounts**: Direct host directory mounting
- **Named volumes**: Docker-managed volumes
- **Tmpfs mounts**: Memory-only storage

**Volume Examples:**
```bash
# Named volume for database persistence
docker volume create postgres_data
docker run -d --name db -v postgres_data:/var/lib/postgresql/data postgres:15-alpine

# Bind mount for development (hot reload)
docker run -d -p 8000:8000 -v $(pwd):/app taskmanager:dev

# List volumes
docker volume ls

# Inspect volume
docker volume inspect postgres_data
```

#### Environment Variable Management

**Simple Methods to Pass Environment Variables:**
```bash
# Single environment variable
docker run -e FLASK_ENV=development taskmanager:dev

# Multiple environment variables
docker run -e FLASK_ENV=development -e DATABASE_URL=postgresql://user:pass@db/app taskmanager:dev

# Environment file
docker run --env-file .env.dev taskmanager:dev

# Inside container
docker run -it taskmanager:dev env
```

**Simple Environment File Example (.env.simple):**
```bash
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=postgresql://user:pass@localhost:5432/app
SECRET_KEY=simple-secret-key
```

**Our Actual Environment Files:**

**.env.example (for development):**
```bash
# Environment variables for development
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1

# Database configuration
DATABASE_URL=postgresql://todouser:todopass@db:5432/todoapp

# Security
SECRET_KEY=dev-secret-key-change-in-production

# Application settings
APP_NAME=Task Manager
ITEMS_PER_PAGE=10
```

**.env.prod (for production testing):**
```bash
# Production Test Environment Variables
# Copy this file to .env.prod and update the values for production testing
# Usage: docker-compose -f docker-compose.prod-test.yml --env-file .env.prod up

# Database Configuration
DB_PASSWORD=secure-prod-password-change-me-12345

# Flask Configuration  
SECRET_KEY=prod-secret-key-change-in-real-production-very-secure-key-67890

# Optional: Override database URL completely
# DATABASE_URL=postgresql://produser:password@db:5432/todoapp_prod

# Optional: Add additional security configurations
# FLASK_ENV=production (already set in docker-compose)
# FLASK_DEBUG=0 (already set in docker-compose)
```

#### Exercise 5: Manual Multi-Container Setup

**Step 1: Start Database Container**
```bash
# Create network
docker network create taskmanager-net

# Start PostgreSQL
docker run -d \
  --name taskmanager-db \
  --network taskmanager-net \
  -e POSTGRES_DB=todoapp \
  -e POSTGRES_USER=todouser \
  -e POSTGRES_PASSWORD=todopass \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine

# Check database is running
docker logs taskmanager-db
```

**Step 2: Start Web Application**
```bash
# Start Flask app connected to database
docker run -d \
  --name taskmanager-web \
  --network taskmanager-net \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://todouser:todopass@taskmanager-db:5432/todoapp \
  -e SECRET_KEY=dev-secret-key \
  taskmanager:dev

# Check application logs
docker logs taskmanager-web

# Test application
curl http://localhost:8000/health
```

---

## Part 3: Docker Compose & Workflows

### Docker Compose: Multi-container Applications

#### Why Docker Compose?
- **Simplify multi-container applications**
- **Define entire application stack** in one file
- **Easy environment management** (dev/staging/production)
- **Service dependencies and networking** handled automatically

#### Docker Compose File Structure

**Simple docker-compose.yml example:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: todoapp
      POSTGRES_USER: todouser  
      POSTGRES_PASSWORD: todopass
    ports:
      - "5432:5432"

  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://todouser:todopass@db:5432/todoapp
    ports:
      - "8000:8000"
    volumes:
      - .:/app  # Hot reload for development
    depends_on:
      - db
```

**Our Actual docker-compose.yml (Full-Featured):**
```yaml
# Docker Compose for Local Development
# Provides hot reload, volume mounts, and development database
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: taskmanager_db_dev
    environment:
      POSTGRES_DB: todoapp
      POSTGRES_USER: todouser
      POSTGRES_PASSWORD: todopass
      POSTGRES_HOST_AUTH_METHOD: md5
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U todouser -d todoapp"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Flask Web Application (Development)
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    container_name: taskmanager_web_dev
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
      - DATABASE_URL=postgresql://todouser:todopass@db:5432/todoapp
      - SECRET_KEY=dev-secret-key-change-in-production-12345
    ports:
      - "8000:8000"
    volumes:
      # Mount entire app directory for hot reload
      - .:/app
      - /app/__pycache__  # Exclude Python cache files
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  # pgAdmin (Database Management Tool) - Optional
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: taskmanager_pgadmin_dev
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@taskmanager.dev
      PGADMIN_DEFAULT_PASSWORD: admin123
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    ports:
      - "8080:80"
    depends_on:
      - db
    profiles:
      - debug  # Only start with: docker-compose --profile debug up

volumes:
  postgres_data:
    driver: local

networks:
  default:
    name: taskmanager_network
```

**Optional: pgAdmin Database Tool**
To start pgAdmin for database management:
```bash
# Start with pgAdmin included
docker-compose --profile debug up

# pgAdmin access:
# URL: http://localhost:8080
# Email: admin@taskmanager.dev
# Password: admin123
```

#### Exercise 6: Docker Compose in Action

**Step 1: Basic Compose Operations**
```bash
# Start all services (build if needed)
docker-compose up --build

# Start in background
docker-compose up -d

# View running services
docker-compose ps

# View logs to see default user creation
docker-compose logs web

# Follow logs in real-time
docker-compose logs -f web

# Stop all services
docker-compose down

# Stop and remove volumes (careful!)
docker-compose down -v
```

**🎯 Development Convenience - Default User & Sample Data**
When you start the development environment, a default user is automatically created for testing:
- **Username:** `demo`
- **Password:** `demo123`
- **Email:** `demo@taskmanager.dev`

**Sample Tasks Created:**
- **4 pending tasks** - Including Docker and Kubernetes learning objectives
- **5 completed tasks** - Showing progress from previous workshop sessions

You can immediately access the application at http://localhost:8000 and log in with these credentials to see a fully populated dashboard!

**Step 2: Development Workflow**
```bash
# Start development environment
docker-compose up -d

# Make code changes (files are mounted)
# Changes automatically reflected due to volume mount

# View application logs
docker-compose logs -f web

# Restart specific service
docker-compose restart web

# Execute commands in running container
docker-compose exec web python -c "print('Hello from container!')"
docker-compose exec db psql -U todouser -d todoapp
```

**Step 3: Service Scaling**
```bash
# Scale web service to multiple instances
docker-compose up --scale web=3

# Load balancer would be needed for production
# Kubernetes handles this automatically (preview of Day 3)
```

### Development vs Production & Next Steps

#### Development Configuration Features
- **Volume mounts** for hot reload
- **Debug mode** enabled
- **Exposed database ports** for debugging
- **Additional tools** (pgAdmin, debugging containers)

#### Production Configuration Features  
- **No volume mounts** (immutable containers)
- **Production Dockerfile** with optimizations
- **Environment variables** from secrets
- **Resource limits** and health checks
- **No debugging tools** or exposed internal ports

#### Exercise 7: Compare Development vs Production

**Development Compose File:**
```yaml
# docker-compose.yml (development)
services:
  web:
    build:
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app  # Hot reload
    environment:
      - FLASK_DEBUG=1
    ports:
      - "8000:8000"
      
  db:
    ports:
      - "5432:5432"  # Database access for debugging

  pgadmin:  # Database management tool
    image: dpage/pgadmin4
    # ... pgadmin configuration
```

**Production Testing Compose File (docker-compose.prod-test.yml):**
```yaml  
# Docker Compose for Production Testing
# Mimics production environment with production Dockerfile and settings
# Use: docker-compose -f docker-compose.prod-test.yml up --build

services:
  # PostgreSQL Database (Production-like)
  db:
    image: postgres:15-alpine
    container_name: taskmanager_db_prod_test
    environment:
      POSTGRES_DB: todoapp_prod
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secure-prod-password-change-me}
    ports:
      - "5433:5432"  # Different port to avoid dev conflicts
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d todoapp_prod"]
      interval: 3s
      timeout: 3s
      retries: 3
    restart: unless-stopped
    networks:
      - taskmanager_prod_network

  # Flask Web Application (Production)
  web:
    build:
      context: .
      dockerfile: Dockerfile  # Uses production Dockerfile
    container_name: taskmanager_web_prod_test
    environment:
      # Production environment settings
      - FLASK_ENV=production
      - FLASK_DEBUG=0
      - DATABASE_URL=postgresql://postgres:${DB_PASSWORD:-secure-prod-password-change-me}@db:5432/todoapp_prod
      - SECRET_KEY=${SECRET_KEY:-prod-secret-key-change-in-real-production-very-secure-key}
      - PYTHONUNBUFFERED=1
    ports:
      - "8000:8000"  # Direct access to Flask app
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 5s
      timeout: 10s
      retries: 3
    networks:
      - taskmanager_prod_network
    # No volume mounts - production-like immutable containers
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

volumes:
  postgres_prod_data:
    driver: local
    name: taskmanager_prod_db

networks:
  taskmanager_prod_network:
    driver: bridge
    name: taskmanager_prod_network
```

**Running Different Environments:**
```bash
# Development
docker-compose up

# Production-like testing
docker-compose -f docker-compose.prod-test.yml up

# Note: Actual production deployment will be done on Kubernetes (Day 3)
# where we'll have proper secrets management, auto-scaling, and multi-node deployment
```

#### Preview: From Docker to Kubernetes (Day 3)

**Docker Compose (Single Machine):**
```bash
docker-compose up --scale web=3  # Limited to one machine
```

**Kubernetes (Multi-Machine Cluster):**
```bash
kubectl apply -f k8s/deployment.yaml  # Scales across cluster
kubectl scale deployment taskmanager --replicas=10
```

**Key Differences:**
- Docker Compose: Single machine, simple orchestration
- Kubernetes: Multi-machine, advanced orchestration, self-healing, auto-scaling
- Production deployments will use Kubernetes for true scalability and reliability

---

## Session Assessment & Next Steps

### Individual Checkpoints
Each student should have:
- [ ] Built at least 2 Docker images (basic and optimized)
- [ ] Run containers with port mapping and environment variables
- [ ] Created a Docker Hub account and public repository
- [ ] Tagged and pushed production image to Docker Hub
- [ ] Successfully pulled and run their image from Docker Hub
- [ ] Created a working docker-compose.yml file
- [ ] Successfully run multi-container application (Flask + PostgreSQL)
- [ ] Logged in to the application using default development credentials (demo/demo123)
- [ ] Explored the sample tasks showing pending and completed items
- [ ] Understand difference between development and production configurations

### Key Takeaways
1. **Docker solves environment consistency** - "works everywhere"
2. **Containers are lightweight** compared to VMs
3. **Docker Compose simplifies** multi-container applications  
4. **Multi-stage builds optimize** production images
5. **Docker Hub enables image sharing** and distribution
6. **Environment-specific configurations** enable flexible deployments

### Preparation for Day 3 (Kubernetes)
- [ ] Understand that containers need orchestration at scale
- [ ] Recognize limitations of single-machine Docker Compose
- [ ] Ready to learn multi-machine container orchestration
- [ ] Have working containerized application for K8s deployment

### Homework/Extended Learning
- [ ] Experiment with different base images
- [ ] Try running containers on different machines
- [ ] Explore Docker Hub and find useful images
- [ ] Practice docker-compose with other applications

---

## Troubleshooting Guide

### Common Issues & Solutions

**Issue: Port already in use**
```bash
# Find process using port
lsof -i :8000
# Or stop existing containers
docker-compose down
```

**Issue: pgAdmin email validation error**
```bash
# Error: 'admin@taskmanager.local' does not appear to be a valid email address
# Solution: Use .dev domain instead of .local (already fixed in our compose file)
# pgAdmin now rejects .local domains as invalid
# Access: http://localhost:8080 with admin@taskmanager.dev / admin123
```

**Issue: Permission denied**
```bash
# Check Docker daemon is running
docker info
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
```

**Issue: Container won't start**
```bash
# Check logs for errors
docker logs container-name
# Check container status
docker ps -a
```

**Issue: Database connection refused**
```bash
# Verify database is healthy
docker-compose exec db pg_isready -U todouser -d todoapp
# Check network connectivity
docker-compose exec web nc -z db 5432
```

**Issue: Changes not reflected (development)**
```bash
# Verify volume mount
docker-compose exec web ls -la /app
# Restart service
docker-compose restart web
```

**Issue: Image too large**
```bash
# Use multi-stage build
# Use alpine-based images  
# Clean up in same RUN command
RUN apt-get update && apt-get install -y package && rm -rf /var/lib/apt/lists/*
```

---

## Resources for Continued Learning

### Official Documentation
- [Docker Docs](https://docs.docker.com/) - Complete Docker documentation
- [Docker Compose Docs](https://docs.docker.com/compose/) - Compose file reference
- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/) - Official guidelines

### Learning Platforms
- [Docker Classroom](https://training.docker.com/) - Official Docker training
- [Play with Docker](https://labs.play-with-docker.com/) - Browser-based Docker playground
- [Docker Hub](https://hub.docker.com/) - Explore public images

### Next Level Topics
- Docker Swarm (Docker's orchestration)
- Container security scanning
- Multi-architecture builds
- Container registries and CI/CD integration

---

**Ready for Kubernetes!**

*Tomorrow we'll take these containers and deploy them to a multi-machine Kubernetes cluster with auto-scaling, self-healing, and zero-downtime deployments.*