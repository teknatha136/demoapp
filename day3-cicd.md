# CI/CD with GitHub Actions
## Day 3 - Automated Testing and Docker Deployment

**Duration:** 3 hours
**Format:** Hands-on CI/CD pipeline implementation

---

## Learning Objectives
By the end of this session, you will be able to:
- Understand CI/CD principles and benefits in modern software development
- Create GitHub Actions workflows for automated testing
- Implement automated Docker image building and deployment to Docker Hub
- Use GitHub secrets for secure credential management
- Experience complete DevOps automation pipeline from code commit to production deployment
- Prepare foundation for Kubernetes deployment (Day 4)

---

## Session Structure

### **Part 1: CI/CD Fundamentals**
#### What is CI/CD and Why It Matters
#### GitHub Actions Introduction and Architecture
#### Setting Up Your First Workflow

### **Part 2: Automated Testing Pipeline**
#### Creating Test Automation Workflows
#### Running Tests on Pull Requests
#### Code Quality and Test Reporting

### **Part 3: Docker Automation & Production Deployment**
#### Automated Docker Image Building
#### Pushing to Docker Hub via GitHub Actions
#### Production Environment Deployment
#### Secrets Management and Security

---

## Part 1: CI/CD Fundamentals

### What is CI/CD?

#### Continuous Integration (CI)
**Continuous Integration** is the practice of frequently integrating code changes into a main repository where automated builds and tests run.

**Key Benefits:**
- **Early bug detection** - Issues found within minutes, not days
- **Consistent code quality** - Every change is tested automatically
- **Faster development** - Quick feedback on code changes
- **Reduced integration problems** - Small, frequent changes are easier to debug

#### Continuous Deployment (CD)
**Continuous Deployment** is the practice of automatically deploying every change that passes automated tests to production.

**Key Benefits:**
- **Faster time to market** - Features reach users immediately
- **Reduced deployment risk** - Small, frequent deployments
- **Consistent deployments** - Same process every time
- **Quick rollback capability** - Easy to revert if issues arise

#### Traditional vs CI/CD Development

**Traditional Development:**
```
Developer → Code for days/weeks → Manual testing → Manual deployment → Hope it works
```

**CI/CD Development:**
```
Developer → Small change → Automated tests → Automated deployment → Immediate feedback
```

### GitHub Actions Architecture

### GitHub Actions Architecture

#### Key Components

**Workflows:**
- YAML files that define your automation
- Stored in `.github/workflows/` directory
- Triggered by events (push, pull request, schedule, etc.)

**Jobs:**
- Groups of steps that execute on the same runner
- Can run in parallel or sequentially
- Each job runs in a fresh virtual environment

**Steps:**
- Individual tasks within a job
- Can run commands or use pre-built actions
- Share the same runner environment

**Actions:**
- Reusable units of code
- Can be your own or from the GitHub Marketplace
- Examples: checkout code, setup Python, deploy to cloud

**Runners:**
- Virtual machines that execute your workflows
- GitHub provides Ubuntu, Windows, and macOS runners
- Can also use self-hosted runners

#### Who Creates Actions?

**GitHub (Official Actions):**
- `actions/checkout` - Check out repository code
- `actions/setup-python` - Set up Python environment
- `actions/upload-artifact` - Upload build artifacts

**Third-party Companies:**
- `docker/build-push-action` - Docker Inc.
- `aws-actions/configure-aws-credentials` - Amazon
- `azure/login` - Microsoft

**Community Contributors:**
- Open source developers
- Individual maintainers
- Available on [GitHub Marketplace](https://github.com/marketplace?type=actions)

**Your Organization:**
- Create custom actions for internal use
- Share privately within your organization
- Composite actions combining multiple steps

#### Types of Triggers (`on:`)

**Push Events:**
```yaml
on:
  push:
    branches: [ main, develop ]    # Specific branches
    tags: [ 'v*' ]                # Tag patterns
    paths: [ 'src/**' ]           # Only when certain files change
```

**Pull Request Events:**
```yaml
on:
  pull_request:
    branches: [ main ]
    types: [opened, synchronize, reopened, closed]
```

**Scheduled Events:**
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
    - cron: '0 0 * * 0'  # Weekly on Sunday
```

**Manual Triggers:**
```yaml
on:
  workflow_dispatch:        # Manual trigger from UI
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
```

**External Events:**
```yaml
on:
  repository_dispatch:      # Triggered by external API calls
    types: [deploy-prod]
  
  workflow_run:            # After another workflow completes
    workflows: ["CI"]
    types: [completed]
```

**Issue/PR Events:**
```yaml
on:
  issues:
    types: [opened, labeled]
  pull_request_review:
    types: [submitted]
```

**Release Events:**
```yaml
on:
  release:
    types: [published, created]
```

#### Action Types

**JavaScript Actions:**
- Run directly on runners
- Fast execution
- Good for simple logic

**Docker Actions:**
- Run in containers
- More isolated
- Can use any programming language

**Composite Actions:**
- Combine multiple steps
- Reusable workflows
- Written in YAML

#### Workflow Syntax Example
```yaml
name: My Workflow
on: 
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Run a command
        run: echo "Hello World"
```

#### GitHub Actions Ecosystem

**Marketplace Benefits:**
- **Thousands of pre-built actions** - Don't reinvent the wheel
- **Community tested** - Popular actions are battle-tested
- **Continuous updates** - Maintained by creators and community
- **Easy integration** - One line to add powerful functionality

**Action Versioning:**
```yaml
# Use specific version (recommended for production)
uses: actions/checkout@v5

# Use major version (gets patches automatically)  
uses: actions/checkout@v4

# Use branch (not recommended)
uses: actions/checkout@main
```

**Security Considerations:**
- **Pin to specific versions** for critical workflows
- **Review third-party actions** before using
- **Use only trusted publishers** when possible
- **Check action source code** for sensitive operations

### Exercise 1: Your First GitHub Actions Workflow

**Step 1: Create Workflow Directory**
```bash
# In your repository, create the workflows directory
mkdir -p .github/workflows
```

**Step 2: Create a Simple Workflow**
Create `.github/workflows/hello-world.yml`:
```yaml
name: Hello World Workflow

# Trigger on push to any branch
on: [push]

jobs:
  greet:
    name: Greeting Job
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v5
        
      - name: Say hello
        run: |
          echo "Hello from GitHub Actions!"
          echo "Repository: ${{ github.repository }}"
          echo "Branch: ${{ github.ref_name }}"
          echo "Commit SHA: ${{ github.sha }}"
          
      - name: Show environment
        run: |
          echo "Runner OS: ${{ runner.os }}"
          echo "Available tools:"
          python --version
          node --version
          docker --version
```

**Step 3: Commit and Push**
```bash
git add .github/workflows/hello-world.yml
git commit -m "Add first GitHub Actions workflow"
git push
```

**Step 4: View Results**
1. Go to your GitHub repository
2. Click "Actions" tab
3. See your workflow running/completed
4. Click on the workflow run to see details and logs

---

## Part 2: Automated Testing Pipeline

### Why Automate Testing?

**Manual Testing Problems:**
- Inconsistent execution
- Forgotten test cases
- Time-consuming
- Human error prone
- Doesn't scale with team growth

**Automated Testing Benefits:**
- Consistent execution every time
- Immediate feedback on code changes
- Prevents regression bugs
- Enables confident refactoring
- Scales with team and codebase

### Exercise 2: Automated Testing Workflow

Let's create a comprehensive testing workflow using the existing CI pipeline from our project:

**Step 1: Create CI Workflow**
Create `.github/workflows/ci.yml`:
```yaml
# CI Pipeline for Task Manager
# Runs tests on pull requests and pushes to main

name: CI Pipeline

on:
  pull_request:
  push:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    permissions:
      checks: write
      pull-requests: write

    # PostgreSQL service for testing
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - name: Checkout code
      uses: actions/checkout@v5

    - name: Set up Python
      uses: actions/setup-python@v6
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        cache: 'pip'  # Cache pip dependencies for faster builds

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-flask pytest-github-actions-annotate-failures

    - name: Run tests
      env:
        DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
        SECRET_KEY: test-secret-key-for-ci
        FLASK_ENV: testing
      run: |
        pytest --tb=short -v --junitxml=test-results.xml

    - name: Upload test results
      uses: actions/upload-artifact@v4
      if: always()  # Upload even if tests fail
      with:
        name: test-results-${{ github.sha }}
        path: test-results.xml

    - name: Publish Test Results
      uses: EnricoMi/publish-unit-test-result-action@v2
      if: always()
      with:
        files: test-results.xml
        check_name: Test Results
```

**Step 2: Understanding the Workflow**

**Services Section:**
```yaml
services:
  postgres:
    image: postgres:15-alpine
    # ... configuration
```
- Starts a PostgreSQL container for testing
- Available to all steps in the job
- Uses health checks to ensure database is ready

**Caching:**
```yaml
cache: 'pip'
```
- Caches Python packages between runs
- Significantly speeds up builds
- Automatically manages cache invalidation

**Environment Variables:**
```yaml
env:
  DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
```
- Provides test database configuration
- Isolates test environment from production

**Step 3: Create a Pull Request Workflow**

Let's see this in action by creating a pull request:

```bash
# Create a feature branch
git checkout -b feature/add-ci-testing

# Add the CI workflow
git add .github/workflows/ci.yml
git commit -m "Add comprehensive CI testing pipeline"
git push -u origin feature/add-ci-testing
```

1. Create pull request on GitHub
2. Watch the CI pipeline run automatically
3. See test results in the PR checks
4. Merge only after tests pass

### Exercise 3: Advanced Testing Features

**Step 1: Add Code Coverage**
Update your CI workflow to include coverage reporting:

```yaml
    - name: Run tests with coverage
      env:
        DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
        SECRET_KEY: test-secret-key-for-ci
        FLASK_ENV: testing
      run: |
        pytest --tb=short -v --cov=. --cov-report=xml --junitxml=test-results.xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
```

**Step 2: Matrix Testing (Multiple Python Versions)**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v6
      with:
        python-version: ${{ matrix.python-version }}
```

---

## Part 3: Docker Automation & Production Deployment

### Why Automate Docker Builds?

**Manual Docker Build Problems:**
- Inconsistent build environments
- Forgotten build steps
- Manual tagging errors
- Security credential exposure
- Time-consuming for teams

**Automated Docker Benefits:**
- Consistent builds every time
- Automatic semantic versioning
- Secure credential management
- Integration with deployment pipelines
- Audit trail of all deployments

### Exercise 4: Automated Docker Build and Push

**Step 1: Set Up Docker Hub Credentials**

1. **Create Docker Hub Token:**
   - Go to [hub.docker.com](https://hub.docker.com)
   - Account Settings → Security → New Access Token
   - Name: "github-actions-workshop"
   - Copy the token (save it - you won't see it again!)

2. **Add GitHub Secrets:**
   - Go to your GitHub repository
   - Settings → Secrets and variables → Actions
   - Add these secrets:
     - `DOCKERHUB_USERNAME`: Your Docker Hub username
     - `DOCKERHUB_TOKEN`: The access token you just created

**Step 2: Create Docker Build Workflow**
Create `.github/workflows/docker-build.yml`:
```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: docker.io
  IMAGE_NAME: taskmanager

jobs:
  build-and-push:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v5

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Docker Hub
      if: github.event_name != 'pull_request'
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ secrets.DOCKERHUB_USERNAME }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha,prefix={{branch}}-

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        file: ./Dockerfile
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
        platforms: linux/amd64,linux/arm64
```

**Step 3: Understanding the Docker Workflow**

**Conditional Login:**
```yaml
if: github.event_name != 'pull_request'
```
- Only login to Docker Hub for actual pushes
- Pull requests just build (don't push) for security

**Metadata Extraction:**
```yaml
tags: |
  type=ref,event=branch      # branch-name
  type=ref,event=pr          # pr-123
  type=semver,pattern={{version}}  # 1.2.3 (for git tags)
  type=sha,prefix={{branch}}- # main-abc1234
```
- Automatically generates appropriate tags
- Different strategies for different trigger types

**Multi-platform Builds:**
```yaml
platforms: linux/amd64,linux/arm64
```
- Builds for both Intel and ARM architectures
- Important for modern deployment environments

**Build Cache:**
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```
- Uses GitHub Actions cache for Docker layers
- Significantly speeds up builds

### Exercise 5: Complete CI/CD Pipeline

Now let's combine testing and deployment into a complete pipeline:

**Step 1: Create Production Deployment Workflow**
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

# Only run after CI passes
on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types: [completed]
    branches: [main]

env:
  REGISTRY: docker.io
  IMAGE_NAME: taskmanager

jobs:
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    
    # Production environment protection
    environment:
      name: production
      url: https://taskmanager-production.example.com
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v5

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Build and push production image
      uses: docker/build-push-action@v5
      with:
        context: .
        file: ./Dockerfile
        push: true
        tags: |
          ${{ env.REGISTRY }}/${{ secrets.DOCKERHUB_USERNAME }}/${{ env.IMAGE_NAME }}:latest
          ${{ env.REGISTRY }}/${{ secrets.DOCKERHUB_USERNAME }}/${{ env.IMAGE_NAME }}:prod-${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Deployment notification
      run: |
        echo "🚀 Production deployment completed!"
        echo "📦 Image: ${{ env.REGISTRY }}/${{ secrets.DOCKERHUB_USERNAME }}/${{ env.IMAGE_NAME }}:prod-${{ github.sha }}"
        echo "🔗 Available at: https://hub.docker.com/r/${{ secrets.DOCKERHUB_USERNAME }}/${{ env.IMAGE_NAME }}"
        
        echo "⚡ Quick start command:"
        echo "docker run -p 8000:8000 ${{ secrets.DOCKERHUB_USERNAME }}/${{ env.IMAGE_NAME }}:latest"
```

**Note on Production Environments:**
In this workshop, we're deploying to Docker Hub as our "production" environment for simplicity. In real-world scenarios, you might have:
- **Staging Environment** - Pre-production testing
- **Production Environment** - Live application
- **Development Environment** - Developer testing
- **QA Environment** - Quality assurance testing

Each environment would have its own deployment pipeline, secrets, and configurations.

**Step 2: Environment Protection**
1. Go to your GitHub repository
2. Settings → Environments
3. Create "production" environment
4. Add protection rules:
   - Required reviewers (in team scenarios)
   - Wait timer (e.g., 5 minutes)
   - Environment secrets (if different from repo secrets)

### Exercise 6: Advanced CI/CD Features

**Step 1: Workflow Dependencies**
```yaml
# This workflow waits for CI to complete successfully
on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types: [completed]
    branches: [main]
```

**Step 2: Matrix Deployments (Multiple Environments)**
```yaml
jobs:
  deploy:
    strategy:
      matrix:
        environment: [staging, production]
    environment: ${{ matrix.environment }}
    # ... deployment steps
```

**Step 3: Rollback Capability**
```yaml
  rollback:
    name: Rollback on Failure
    runs-on: ubuntu-latest
    if: failure()
    steps:
    - name: Deploy previous version
      run: |
        # Logic to deploy previous successful version
        echo "Rolling back to previous version..."
```

---

## Session Assessment & Next Steps

### Individual Checkpoints
Each student should have:
- [ ] Created a GitHub Actions workflow for automated testing
- [ ] Successfully run tests automatically on pull request
- [ ] Set up Docker Hub credentials in GitHub secrets
- [ ] Created automated Docker build and push workflow
- [ ] Successfully deployed Docker image to Docker Hub via CI/CD
- [ ] Understanding of CI/CD principles and benefits
- [ ] Experience with GitHub Actions workflow syntax

### Key Takeaways
1. **CI/CD automates repetitive tasks** - Testing and deployment
2. **Early feedback prevents problems** - Catch issues in minutes, not days
3. **Consistent processes reduce errors** - Same steps every time
4. **Security through secrets management** - Never expose credentials in code
5. **Workflow dependencies enable complex pipelines** - Test → Build → Deploy

### Preparation for Day 4 (Kubernetes)
- [ ] Understand that containers are ready for orchestration
- [ ] Have working CI/CD pipeline that produces deployable images
- [ ] Ready to learn how Kubernetes can consume these automated deployments
- [ ] Foundation set for automated Kubernetes deployments

### Real-World Applications
- **Continuous Quality Assurance** - Every change is tested
- **Faster Time to Market** - Automated deployments reduce release cycles
- **Reduced Human Error** - Automation eliminates manual mistakes  
- **Scalable Development** - Supports growing teams and codebases
- **Audit Trail** - Complete history of what was deployed when

---

## Troubleshooting Guide

### Common Issues & Solutions

**Issue: Workflow not triggering**
```yaml
# Check your trigger configuration
on:
  push:
    branches: [ main ]  # Make sure branch name matches
  pull_request:
    branches: [ main ]
```

**Issue: Docker Hub authentication failed**
```bash
# Verify secrets are set correctly
# Repository → Settings → Secrets and variables → Actions
# Required: DOCKERHUB_USERNAME and DOCKERHUB_TOKEN
```

**Issue: Tests failing in CI but passing locally**
```yaml
# Common causes:
# - Environment variables missing
# - Database configuration different
# - Timezone differences
# - Case sensitivity (Linux vs Windows/Mac)
```

**Issue: Docker build context too large**
```dockerfile
# Add .dockerignore file to exclude unnecessary files
.git
.github
*.md
node_modules
__pycache__
.pytest_cache
```

**Issue: Secrets not accessible**
```yaml
# Secrets are only available in specific contexts
- name: Use secret
  env:
    MY_SECRET: ${{ secrets.MY_SECRET }}  # ✅ Correct
  run: echo $MY_SECRET

# Don't use: ${{ secrets.MY_SECRET }} in run directly  # ❌ Security risk
```

---

## Complete Workflow Files

### CI Workflow File (.github/workflows/ci.yml)

Here's the complete CI workflow file for your repository:

```yaml
# CI Pipeline for Task Manager Workshop
# Runs comprehensive tests on pull requests and pushes to main branch

name: CI Pipeline

on:
  pull_request:
  push:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    permissions:
      checks: write
      pull-requests: write

    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - name: Checkout code
      uses: actions/checkout@v5

    - name: Set up Python
      uses: actions/setup-python@v6
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-flask pytest-github-actions-annotate-failures

    - name: Run tests
      env:
        DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
        SECRET_KEY: test-secret-key-for-ci
        FLASK_ENV: testing
      run: |
        pytest --tb=short -v --junitxml=test-results.xml

    - name: Upload test results
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: test-results-${{ github.sha }}
        path: test-results.xml

    - name: Publish Test Results
      uses: EnricoMi/publish-unit-test-result-action@v2
      if: always()
      with:
        files: test-results.xml
        check_name: Test Results
```

### CD Workflow File (.github/workflows/cd.yaml)

Here's the complete CD workflow for Docker build and deployment:

```yaml
# Continuous Deployment Pipeline
# Builds and pushes Docker images to Docker Hub after successful CI

name: CD Pipeline

on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types: [completed]
    branches: [main]
  push:
    tags: ['v*']

env:
  REGISTRY: docker.io
  IMAGE_NAME: taskmanager-workshop

jobs:
  build-and-push:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' || github.event_name == 'push' }}
    
    environment:
      name: production
      url: https://hub.docker.com/r/${{ secrets.DOCKERHUB_USERNAME }}/taskmanager-workshop

    steps:
    - name: Checkout code
      uses: actions/checkout@v5

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ secrets.DOCKERHUB_USERNAME }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v6
      with:
        context: .
        file: ./Dockerfile
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
        platforms: linux/amd64,linux/arm64

    - name: Image digest
      run: |
        echo "🚀 Production deployment completed!"
        echo "📦 Image pushed to Docker Hub:"
        echo "   Repository: ${{ secrets.DOCKERHUB_USERNAME }}/taskmanager-workshop"
        echo "   Tags: ${{ steps.meta.outputs.tags }}"
        echo ""
        echo "⚡ Quick start commands:"
        echo "   docker pull ${{ secrets.DOCKERHUB_USERNAME }}/taskmanager-workshop:latest"
        echo "   docker run -p 8000:8000 ${{ secrets.DOCKERHUB_USERNAME }}/taskmanager-workshop:latest"
        echo ""
        echo "🔗 View on Docker Hub: https://hub.docker.com/r/${{ secrets.DOCKERHUB_USERNAME }}/taskmanager-workshop"

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: build-and-push
    if: ${{ github.event.workflow_run.conclusion == 'success' || github.event_name == 'push' }}
    
    steps:
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: '${{ secrets.DOCKERHUB_USERNAME }}/taskmanager-workshop:latest'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'
```

### How to Use These Workflow Files

**Step 1: Create the workflow directory structure**
```bash
mkdir -p .github/workflows
```

**Step 2: Create the CI workflow**
```bash
# Copy the CI workflow content above into:
.github/workflows/ci.yml
```

**Step 3: Create the CD workflow**  
```bash
# Copy the CD workflow content above into:
.github/workflows/cd.yaml
```

**Step 4: Set up required secrets**
Go to your GitHub repository → Settings → Secrets and variables → Actions:
- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token

**Step 5: Commit and push**
```bash
git add .github/workflows/
git commit -m "Add CI/CD workflows for automated testing and Docker deployment"
git push
```

**Step 6: Watch the magic happen**
1. **CI Pipeline** runs on every push and pull request
2. **CD Pipeline** runs only after CI passes successfully on main branch
3. **Docker images** are automatically built and pushed to Docker Hub
4. **Security scanning** runs on all published images

---

## Resources for Continued Learning

### Official Documentation
- [GitHub Actions Docs](https://docs.github.com/en/actions) - Complete GitHub Actions documentation
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) - YAML syntax reference
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions) - Pre-built actions

### Best Practices
- [GitHub Actions Security](https://docs.github.com/en/actions/security-guides) - Security best practices
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/) - Docker optimization
- [CI/CD Patterns](https://martinfowler.com/articles/continuousIntegration.html) - Martin Fowler's CI guide

### Advanced Topics
- Custom GitHub Actions development
- Self-hosted runners
- Kubernetes deployment automation
- Multi-cloud deployment strategies

---

**Ready for Kubernetes! Tomorrow we'll automate deployments to Kubernetes clusters using the images built by today's CI/CD pipelines.**