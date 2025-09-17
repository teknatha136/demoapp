# GitHub Actions Workflows

This directory contains the GitHub Actions workflow files for the Task Manager application.

## Workflow Files

### 1. `basic-ci.yml` - Basic CI Pipeline (Starter)
- **Purpose**: Simple CI pipeline for beginners
- **Triggers**: Push to main, Pull Requests to main
- **Jobs**:
  - Runs tests with PostgreSQL database
  - Basic Python testing setup

### 2. `ci.yml` - Complete CI Pipeline (Advanced)
- **Purpose**: Comprehensive CI with testing, linting, and security
- **Triggers**: Push to main/develop, Pull Requests to main
- **Jobs**:
  - **test**: Run pytest with PostgreSQL
  - **lint**: Code formatting (Black) and linting (Flake8)
  - **security-scan**: Dependency and code security scanning

### 3. `cd.yaml` - Complete CD Pipeline (Build & Deploy)
- **Purpose**: Full build and deployment pipeline combining Docker build with staging and production deployment
- **Triggers**: Push to main, tags, after CI completion
- **Jobs**:
  - **check-ci**: Verify CI workflow passed
  - **build-and-push**: Multi-platform Docker builds and push to Docker Hub
  - **security-scan**: Container vulnerability scanning
  - **deploy-staging**: Deploy to staging environment
  - **deploy-production**: Deploy to production (on tags only)
  - **cleanup**: Clean up old images

## Workflow Files

To use these workflows, add the following secrets in your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add **Repository secrets**:

### Docker Hub Secrets
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token (not password)

### How to get Docker Hub Access Token:
1. Go to [Docker Hub](https://hub.docker.com)
2. Sign in to your account
3. Go to **Account Settings** → **Security**
4. Click **New Access Token**
5. Give it a name (e.g., "GitHub Actions")
6. Copy the token and add it as `DOCKER_PASSWORD` secret

## Environment Setup

### For Production Deployments (cd.yml)
1. Create environments in GitHub:
   - Go to **Settings** → **Environments**
   - Create `staging` and `production` environments
   - Add protection rules as needed

### For Database Testing
The workflows use PostgreSQL service containers for testing:
- Database: `testdb`
- Username: `testuser`  
- Password: `testpass`
- Port: `5432`

## Usage Instructions

### Getting Started (Students)
1. Start with `basic-ci.yml` - rename it to `ci.yml` to activate
2. Make sure your tests pass locally first
3. Push code and watch the workflow run

### Intermediate (Docker Build & Deploy)
1. Set up Docker Hub secrets (see above)
2. Use `cd.yaml` to build, push images, and deploy
3. Check Docker Hub for your pushed images
4. Monitor staging deployments

### Advanced (Full CI/CD)
1. Use the complete `ci.yml` and `cd.yaml` workflows
2. Set up environments for staging/production
3. Create deployment scripts for your infrastructure

## Common Issues

### 1. Tests Failing
- Make sure `DATABASE_URL` environment variable is set correctly
- Check that PostgreSQL service is healthy
- Verify test database initialization

### 2. Docker Build Fails
- Check Dockerfile syntax
- Ensure all required files are in repository
- Verify Docker Hub credentials

### 3. Secrets Not Working
- Double-check secret names (case-sensitive)
- Ensure Docker Hub token has push permissions
- Verify repository has access to secrets

## Workshop Exercises

### Exercise 1: Basic CI
- Enable `basic-ci.yml` workflow
- Fix any test failures
- Add a new test and see it run

### Exercise 2: Docker Build & Deploy
- Set up Docker Hub account and token
- Enable `cd.yaml` workflow
- Verify image is pushed to Docker Hub
- Check staging deployment logs

### Exercise 3: Advanced Pipeline
- Implement the complete CI/CD pipeline with `ci.yml` and `cd.yaml`
- Set up staging environment
- Deploy using the CD workflow

## Best Practices

1. **Start Simple**: Begin with basic CI, then add complexity
2. **Test Locally**: Always test your changes locally first
3. **Monitor Workflows**: Check Actions tab for workflow status
4. **Use Caching**: Workflows include caching for faster builds
5. **Security**: Use secrets for sensitive data, never hardcode
6. **Environments**: Use GitHub environments for deployment protection

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)