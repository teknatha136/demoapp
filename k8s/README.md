# Kubernetes Manifests for Task Manager Application

This directory contains the production Kubernetes YAML files for deploying the Task Manager application.

## Directory Structure

```
k8s/                    # Production deployment files
├── 01-namespace.yaml   # Individual student namespace
├── 02-postgres.yaml    # PostgreSQL reference (not used - DB on VM)
├── 03-taskmanager.yaml # Task Manager app deployment and service
├── 04-ingress.yaml     # HTTP routing and external access
└── README.md          # This file

k8s-intro/             # Learning files for Kubernetes basics
├── hello-pod.yaml     # Simple Pod example with detailed comments
└── README.md          # Instructions for learning Pods

k8s-sample/            # Sample configuration files (DO NOT use in production)
├── configmap-sample.yaml  # Example ConfigMap with comments
├── secret-sample.yaml     # Example Secret with security warnings
└── README.md              # Security guidelines and best practices
```

## 🎓 **Student Deployment Instructions**

### Step 0: Prepare Your Student Information
Before starting, you'll need:
- **Student Number**: Your university student number (e.g., 0215539)
- **DockerHub Username**: From Day 3 CI/CD workshop
- **VM IP Address**: PostgreSQL database server IP

### Step 1: Set Up Your Personal Namespace
```bash
# Replace STUDENT_NUMBER with your actual student number
export STUDENT_NUMBER=0215539  # 📝 Change this to your number
export DOCKERHUB_USERNAME=your-dockerhub-username  # 📝 Change this
export VM_IP=192.168.1.100     # 📝 Change this to your VM IP

# Create your personal namespace file
sed "s/STUDENT_NUMBER/$STUDENT_NUMBER/g" 01-namespace.yaml > my-namespace.yaml

# Create the namespace
kubectl apply -f my-namespace.yaml

# Verify namespace creation
kubectl get namespace $STUDENT_NUMBER
```

### Step 2: Update Configuration Files
```bash
# Create personalized deployment files
sed -e "s/STUDENT_NUMBER/$STUDENT_NUMBER/g" \
    -e "s/YOUR_DOCKERHUB_USERNAME/$DOCKERHUB_USERNAME/g" \
    -e "s/VM_IP_ADDRESS/$VM_IP/g" \
    03-taskmanager.yaml > my-taskmanager.yaml

sed "s/STUDENT_NUMBER/$STUDENT_NUMBER/g" 04-ingress.yaml > my-ingress.yaml
```

### Step 3: Deploy Your Application
```bash
# Deploy the Task Manager application
kubectl apply -f my-taskmanager.yaml

# Deploy ingress for external access  
kubectl apply -f my-ingress.yaml

# Check deployment status in your namespace
kubectl get all -n student-$STUDENT_NUMBER
```

### Step 4: Set Up Local Access
```bash
# Add your personal domain to hosts file (Linux/Mac)
echo "127.0.0.1 taskmanager-$STUDENT_NUMBER.local" | sudo tee -a /etc/hosts

# For Windows, add to C:\Windows\System32\drivers\etc\hosts:
# 127.0.0.1 taskmanager-YOURSTUDENTNO.local

# For minikube users, also run:
minikube tunnel  # Keep this running in a separate terminal
```

### Step 5: Access Your Application
```bash
# Method 1: Via Ingress (recommended)
curl http://taskmanager-$STUDENT_NUMBER.local
# Or visit in browser: http://taskmanager-YOURSTUDENTNO.local

# Method 2: Via port-forward (fallback)
kubectl port-forward -n $STUDENT_NUMBER service/taskmanager-service 8080:80
# Then visit: http://localhost:8080
```

## 👥 **Multi-Student Environment Benefits**

### Isolation
- **Namespace separation**: Each student's resources are isolated in namespace by student number
- **No conflicts**: Multiple students can deploy simultaneously
- **Independent scaling**: Students can experiment without affecting others

### Learning
- **Personal environment**: Each student owns their deployment in their numbered namespace
- **Individual troubleshooting**: Problems don't affect other students
- **Realistic experience**: Mirrors real-world multi-tenant environments

### Management
- **Easy cleanup**: `kubectl delete namespace STUDENT_NUMBER` removes all student resources
- **Resource tracking**: Clear ownership and accountability by student number
- **Instructor overview**: Easy to monitor all student deployments

## Production Deployment Files

### `01-namespace.yaml` - Student Namespace
- **Individual namespaces**: Each student gets their own isolated environment
- **Conflict prevention**: No resource name conflicts between students
- **Resource organization**: Clean separation of student deployments

### `03-taskmanager.yaml` - Application
- **Task Manager Deployment**: 2 replicas for high availability
- **Task Manager Service**: ClusterIP service for internal routing
- **Includes**: Health checks, resource limits, environment configuration

### `04-ingress.yaml` - External Access
- **Ingress Controller**: HTTP/HTTPS routing and load balancing
- **Student-specific hosts**: Each student gets unique domain (taskmanager-STUDENTNO.local)
- **Includes**: SSL termination options, rate limiting, CORS support

## 👥 **Multi-Student Environment Benefits**

### Isolation
- **Namespace separation**: Each student's resources are isolated
- **No conflicts**: Multiple students can deploy simultaneously
- **Independent scaling**: Students can experiment without affecting others

### Learning
- **Personal environment**: Each student owns their deployment
- **Individual troubleshooting**: Problems don't affect other students
- **Realistic experience**: Mirrors real-world multi-tenant environments

### Management
- **Easy cleanup**: Delete namespace removes all student resources
- **Resource tracking**: Clear ownership and accountability
- **Instructor overview**: Easy to monitor all student deployments

## Quick Start (Legacy - Single Student)

### Prerequisites
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured to connect to your cluster
- Ingress controller installed (nginx-ingress recommended)

### Step 1: Update Configuration
```bash
# Update the Docker image in taskmanager deployment
sed -i 's/your-dockerhub-username/YOUR_ACTUAL_USERNAME/g' 03-taskmanager.yaml
```

### Step 2: Deploy Database
```bash
# Deploy PostgreSQL
kubectl apply -f 02-postgres.yaml

# Wait for database to be ready
kubectl wait --for=condition=available --timeout=300s deployment/postgres-deployment
```

### Step 3: Deploy Application
```bash
# Deploy Task Manager application
kubectl apply -f 03-taskmanager.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
```

### Step 4: Set Up External Access
```bash
# Deploy Ingress (requires ingress controller)
kubectl apply -f 04-ingress.yaml

# Add domain to /etc/hosts (for local testing)
echo "127.0.0.1 taskmanager.local" | sudo tee -a /etc/hosts

# For minikube users
minikube tunnel  # Run in separate terminal
```

### Step 5: Access Application
```bash
# Via Ingress (if configured)
curl http://taskmanager.local

# Via port-forward (fallback method)
kubectl port-forward service/taskmanager-service 8080:80
# Then visit http://localhost:8080
```

## Common Operations

### Scaling
```bash
# Scale application to 5 replicas
kubectl scale deployment taskmanager-deployment --replicas=5

# Check scaling status
kubectl get pods -l app=taskmanager
```

### Updates
```bash
# Update to new image version
kubectl set image deployment/taskmanager-deployment \
  taskmanager=your-username/task-manager:new-version

# Watch rollout progress
kubectl rollout status deployment/taskmanager-deployment

# Rollback if needed
kubectl rollout undo deployment/taskmanager-deployment
```

### Monitoring
```bash
# Check application status
kubectl get all -l app=taskmanager

# View application logs
kubectl logs -l app=taskmanager -f

# Check resource usage
kubectl top pods
```

## Troubleshooting

### Common Issues

**Pods not starting:**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Service not accessible:**
```bash
kubectl get endpoints
kubectl describe service taskmanager-service
```

**Ingress not working:**
```bash
kubectl get ingress
kubectl describe ingress taskmanager-ingress
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

**Database connection issues:**
```bash
# Test database connectivity
kubectl exec -it <taskmanager-pod> -- ping postgres-service
kubectl logs -l app=postgres
```

## Security Best Practices

⚠️ **Important**: This setup is for learning/development. For production:

1. **Use Secrets for sensitive data**:
   ```bash
   kubectl create secret generic app-secrets \
     --from-literal=DB_PASSWORD=your-secure-password \
     --from-literal=SECRET_KEY=your-secret-key
   ```

2. **Enable TLS/HTTPS**:
   - Add TLS certificates to Ingress
   - Use cert-manager for automatic certificate management

3. **Implement proper RBAC**:
   - Create service accounts with minimal permissions
   - Use network policies for traffic control

4. **Use persistent storage**:
   - Replace `emptyDir` with `PersistentVolumeClaims`
   - Set up backup strategies

5. **Monitor and observe**:
   - Set up Prometheus and Grafana
   - Use centralized logging (ELK stack)

## Cleanup

```bash
# Remove all resources
kubectl delete -f 04-ingress.yaml
kubectl delete -f 03-taskmanager.yaml
kubectl delete -f 02-postgres.yaml

# Verify cleanup
kubectl get all
```

## Learning Path

1. **Start with `k8s-intro/`** - Learn Pod basics
2. **Explore `k8s-sample/`** - Understand ConfigMaps and Secrets
3. **Deploy from `k8s/`** - Run the complete application
4. **Experiment** - Try scaling, updates, and monitoring

This structure separates learning materials from production-ready configurations while teaching security best practices from the beginning.