# Kubernetes Introduction & Container Orchestration
## Day 4 - From Docker to Kubernetes

**Duration:** 3 hours
**Format:** Interactive introduction with hands-on Kubernetes basics
**Prerequisites:** Docker knowledge from Day 2, CI/CD understanding from Day 3

---

## Learning Objectives
By the end of this session, you will be able to:
- Understand what Kubernetes is and why it's essential for modern applications
- Explain the difference between Docker and Kubernetes
- Set up a local Kubernetes environment using minikube or kind
- Deploy your Task Manager application to Kubernetes with personal namespace isolation
- Understand basic Kubernetes concepts (Pods, Services, Deployments)
- Use kubectl effectively with namespace contexts
- Connect Kubernetes deployments to CI/CD pipelines (if time permits)
- Troubleshoot common Kubernetes issues

---

## Session Structure

### **Part 1: Kubernetes Fundamentals** (45 minutes)
#### Why Kubernetes? From Single Container to Production Scale
#### Docker vs Docker Compose vs Kubernetes
#### Core Kubernetes Concepts and Architecture
#### Setting Up Local Kubernetes Environment

### **Part 2: Hands-on Kubernetes** (75 minutes)
#### Deploying Your First Pod
#### Creating Services and Deployments  
#### Deploying the Task Manager App to Kubernetes
#### Managing Application Updates and Scaling

### **Part 3: Integration & Advanced Topics** (60 minutes)
#### Kubernetes + CI/CD Integration (if time permits)
#### ConfigMaps and Secrets Management
#### Monitoring and Troubleshooting
#### Next Steps and Real-world Kubernetes

---

## Part 1: Kubernetes Fundamentals

### What is Kubernetes and Why Do We Need It?

#### The Container Journey
```
Single App → Docker Container → Docker Compose → Kubernetes Cluster
```

**Day 2 (Docker):** You learned to containerize a single application
**Day 3 (CI/CD):** You automated building and pushing container images  
**Day 4 (Today):** You'll orchestrate multiple containers at scale

#### Real-World Problems Kubernetes Solves

**Problem 1: Container Management at Scale**
```bash
# With Docker Compose (Day 2) - Good for development
docker-compose up  # Runs on one machine

# In Production - You need:
# - 100+ containers across 10+ servers
# - Automatic restart when containers crash
# - Load balancing between multiple app instances
# - Zero-downtime deployments
```

**Problem 2: High Availability**
```bash
# What happens when your server crashes?
# Docker Compose: Your app goes down ❌
# Kubernetes: Automatically moves containers to healthy servers ✅
```

**Problem 3: Scaling**
```bash
# Traffic spike? Need more app instances?
# Docker Compose: Manual intervention required
# Kubernetes: kubectl scale deployment app --replicas=10
```

### Kubernetes vs Docker: Understanding the Difference

| Aspect                | Docker              | Docker Compose                    | Kubernetes                              |
| --------------------- | ------------------- | --------------------------------- | --------------------------------------- |
| **Scope**             | Single container    | Multiple containers (one machine) | Multiple containers (multiple machines) |
| **Use Case**          | Development/Testing | Local development                 | Production at scale                     |
| **High Availability** | No                  | No                                | Yes                                     |
| **Auto-scaling**      | No                  | No                                | Yes                                     |
| **Self-healing**      | No                  | Limited                           | Yes                                     |
| **Load Balancing**    | Manual              | Basic                             | Advanced                                |
| **Complexity**        | Simple              | Medium                            | Complex                                 |

**Think of it this way:**
- **Docker** = A single shipping container
- **Docker Compose** = A small warehouse managing a few containers  
- **Kubernetes** = A massive shipping port managing thousands of containers across multiple ships

### Core Kubernetes Architecture

#### Master Node (Control Plane)
```
┌─────────────────────────────────┐
│           Master Node           │
├─────────────────────────────────┤
│  API Server  │  etcd  │ Scheduler│
│              │        │Controller│
└─────────────────────────────────┘
```
- **API Server**: The "front desk" - all requests go through here
- **etcd**: The "database" - stores all cluster state
- **Scheduler**: The "assignment manager" - decides where to run containers
- **Controller Manager**: The "supervisor" - ensures desired state

#### Worker Nodes
```
┌─────────────────────────────────┐
│           Worker Node           │
├─────────────────────────────────┤
│     kubelet    │    kube-proxy  │
│                │                │
│  ┌──────────┐  │  ┌──────────┐  │
│  │   Pod 1  │  │  │   Pod 2  │  │
│  │Container │  │  │Container │  │
│  └──────────┘  │  └──────────┘  │
└─────────────────────────────────┘
```
- **kubelet**: The "worker" - manages containers on this node
- **kube-proxy**: The "network manager" - handles networking
- **Pods**: The "working units" - groups of containers

### Key Kubernetes Concepts

#### 1. Pod - The Basic Unit
```yaml
# A Pod is like a "wrapper" around your container
apiVersion: v1
kind: Pod
metadata:
  name: task-manager-pod
spec:
  containers:
  - name: app
    image: your-username/task-manager:latest
    ports:
    - containerPort: 8000
```

**Key Points:**
- Smallest deployable unit in Kubernetes
- Usually contains one container (but can have more)
- Containers in a pod share network and storage
- Pods are mortal - they come and go

#### 2. Deployment - Managing Pods
```yaml
# A Deployment manages multiple Pods
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-manager-deployment
spec:
  replicas: 3  # Run 3 copies of your app
  selector:
    matchLabels:
      app: task-manager
  template:
    metadata:
      labels:
        app: task-manager
    spec:
      containers:
      - name: app
        image: your-username/task-manager:latest
        ports:
        - containerPort: 8000
```

**Key Benefits:**
- Ensures desired number of pods are running
- Handles updates and rollbacks
- Self-healing - replaces crashed pods

#### 3. Service - Networking and Discovery
```yaml
# A Service provides stable networking to pods
apiVersion: v1
kind: Service
metadata:
  name: task-manager-service
spec:
  selector:
    app: task-manager
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Why Services?**
- Pods have changing IP addresses
- Services provide stable endpoints
- Load balance traffic across multiple pods

### Exercise 1: Setting Up Kubernetes Access

#### Setting Up Your Kubeconfig
You will be provided with a kubeconfig file.
A `kubeconfig` file is a YAML-formatted configuration file that organizes information about Kubernetes clusters, users, namespaces, and authentication mechanisms. It is used by Kubernetes client tools, such as kubectl, to access and interact with Kubernetes clusters.

```bash
# Create .kube directory if it doesn't exist
mkdir -p ~/.kube

# Copy the provided kubeconfig file
# Your instructor will give you: kubeconfig-student-XXXX
cp kubeconfig-student-$STUDENT_NUMBER ~/.kube/config

# Or set KUBECONFIG environment variable (alternative method)
export KUBECONFIG=/path/to/kubeconfig-student-$STUDENT_NUMBER

# Verify cluster access
kubectl cluster-info
kubectl get nodes
```

#### Setting Up Your Personal Namespace Context
To avoid typing `-n student-STUDENT_NUMBER` with every command, set up a namespace context:

```bash
# Method 1: Set namespace as default for current context
kubectl config set-context --current --namespace=student-$STUDENT_NUMBER

# Method 2: Create a new context with your namespace (recommended)
kubectl config set-context student-$STUDENT_NUMBER \
  --cluster=$(kubectl config current-context) \
  --user=$(kubectl config current-context) \
  --namespace=student-$STUDENT_NUMBER

# Switch to your personal context
kubectl config use-context student-$STUDENT_NUMBER

# Verify your context and namespace
kubectl config current-context
kubectl config get-contexts

# Test - these commands now work in your namespace without -n flag
kubectl get pods        # Instead of: kubectl get pods -n student-STUDENT_NUMBER
kubectl get services    # Instead of: kubectl get services -n student-STUDENT_NUMBER
kubectl get all        # Shows only your resources
```

#### Useful Context Management Commands
```bash
# View all available contexts
kubectl config get-contexts

# Switch between contexts
kubectl config use-context <context-name>

# View current context
kubectl config current-context

# Get current namespace
kubectl config view --minify -o jsonpath='{..namespace}'

# Switch back to default namespace (if needed)
kubectl config set-context --current --namespace=default

# Create an alias for quick context switching (optional)
alias kctx='kubectl config use-context'
alias kns='kubectl config set-context --current --namespace'
```

---

## Part 2: Hands-on Kubernetes

### Exercise 2: Your First Pod

Let's start with understanding the basic building block of Kubernetes - the Pod.

#### Step 1: Explore the Learning Directory
```bash
# Navigate to the learning materials
cd k8s-intro

# View the simple Pod example
cat hello-pod.yaml
```

#### Step 2: Create Your First Pod
```bash
# Create the pod with detailed comments
kubectl apply -f hello-pod.yaml

# Check if it's running
kubectl get pods

# Expected output:
NAME        READY   STATUS    RESTARTS   AGE
hello-pod   1/1     Running   0          30s

# Get more details about the Pod
kubectl describe pod hello-pod

# Check logs from the container
kubectl logs hello-pod
```

#### Step 3: Access the Pod
```bash
# Forward port to access the pod
kubectl port-forward hello-pod 8080:80

# In another terminal or browser, visit:
# http://localhost:8080
# You should see the nginx welcome page
```

#### Step 4: Explore Inside the Pod
```bash
# Execute commands inside the running container
kubectl exec hello-pod -- ls /usr/share/nginx/html

# Get an interactive shell inside the container
kubectl exec -it hello-pod -- /bin/sh
# Now you're inside! Try:
# - env | grep WELCOME
# - ps aux
# - exit (to leave the container)
```

#### Step 5: Clean up
```bash
kubectl delete pod hello-pod
```

### Exercise 3: Deploying Task Manager to Kubernetes

Now let's deploy our actual Task Manager application. Since PostgreSQL is running on a VM, we'll only deploy the application to Kubernetes and configure it to connect to the external database.

**Important**: Each student will deploy to their own namespace using their student number to avoid conflicts.

#### Step 1: Set Up Your Student Environment
```bash
# Set your personal information (replace with your actual details)
export STUDENT_NUMBER=0215539  # 📝 Replace with YOUR student number
export DOCKERHUB_USERNAME=your-dockerhub-username  # 📝 Replace with YOUR username
export VM_IP=192.168.1.100     # 📝 Replace with the actual VM IP

# Navigate to the Kubernetes directory
cd k8s

# Verify your environment variables
echo "Student Number: $STUDENT_NUMBER"
echo "DockerHub Username: $DOCKERHUB_USERNAME"  
echo "VM IP: $VM_IP"
```
#### Step 2: Create Your Personal Namespace
```bash
# Create your personalized namespace file
sed "s/STUDENT_NUMBER/$STUDENT_NUMBER/g" 01-namespace.yaml > my-namespace.yaml

# Create the namespace in Kubernetes
kubectl apply -f my-namespace.yaml

# Verify namespace creation
kubectl get namespace $STUDENT_NUMBER

# ⭐ IMPORTANT: Set up namespace context to avoid using -n every time
kubectl config set-context $STUDENT_NUMBER \
  --cluster=$(kubectl config view -o jsonpath='{.current-context}') \
  --user=$(kubectl config view -o jsonpath='{.current-context}') \
  --namespace=$STUDENT_NUMBER

# Switch to your personal context
kubectl config use-context $STUDENT_NUMBER

# Verify your context setup
echo "Current context: $(kubectl config current-context)"
echo "Current namespace: $(kubectl config view --minify -o jsonpath='{..namespace}')"

# Test - these commands now work in your namespace automatically!
kubectl get pods        # No need for -n $STUDENT_NUMBER
kubectl get services    # No need for -n $STUDENT_NUMBER
```
#### Step 3: Configure Your Personal Deployment
```bash
# Create personalized deployment file
sed -e "s/STUDENT_NUMBER/$STUDENT_NUMBER/g" \
    -e "s/YOUR_DOCKERHUB_USERNAME/$DOCKERHUB_USERNAME/g" \
    -e "s/VM_IP_ADDRESS/$VM_IP/g" \
    03-taskmanager.yaml > my-taskmanager.yaml

# Create personalized ingress file
sed "s/STUDENT_NUMBER/$STUDENT_NUMBER/g" 04-ingress.yaml > my-ingress.yaml

# Review your personalized files
echo "=== Your Deployment Configuration ==="
grep -E "(namespace|image|DATABASE_URL|host)" my-taskmanager.yaml my-ingress.yaml
```

#### Step 4: Deploy Your Application
```bash
# Deploy the Task Manager application (no -n needed thanks to context!)
kubectl apply -f my-taskmanager.yaml

# Check if pods are starting in your namespace
kubectl get pods

# Watch the deployment progress
kubectl get pods -w

# Expected output (after a minute):
NAME                                     READY   STATUS    RESTARTS   AGE
taskmanager-deployment-xxx               1/1     Running   0          2m
taskmanager-deployment-yyy               1/1     Running   0          2m
```

#### Step 5: Set Up External Access
```bash
# Deploy your personal ingress
kubectl apply -f my-ingress.yaml

# Add your personal domain to hosts file (Linux/Mac)
echo "127.0.0.1 taskmanager-$STUDENT_NUMBER.local" | sudo tee -a /etc/hosts

# For Windows users, add this line to C:\Windows\System32\drivers\etc\hosts:
# 127.0.0.1 taskmanager-YOURSTUDENTNO.local

# For minikube users, enable tunnel (keep running in separate terminal)
minikube tunnel
```

#### Step 6: Access Your Personal Application
```bash
# Method 1: Via your personal Ingress domain
curl http://taskmanager-$STUDENT_NUMBER.local
# Or visit in browser: http://taskmanager-YOURSTUDENTNO.local

# Method 2: Via port-forward (if Ingress doesn't work)
kubectl port-forward service/taskmanager-service 8080:80
# Then visit: http://localhost:8080

# Method 3: Check service status
kubectl get ingress
kubectl get services
```

#### Step 7: Verify Database Connectivity
```bash
# Check application logs for database connection
kubectl logs -l app=taskmanager

# If there are connection issues, troubleshoot:
kubectl describe pods -l app=taskmanager

# Test database connectivity from your pods
POD_NAME=$(kubectl get pods -l app=taskmanager -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD_NAME -- ping $VM_IP
kubectl exec -it $POD_NAME -- telnet $VM_IP 5432
```

### Exercise 4: Scaling and Updates

#### Scaling Your Personal Application
```bash
# Scale up to 5 replicas in your namespace
kubectl scale deployment taskmanager-deployment --replicas=5

# Check the scaling progress
kubectl get pods -l app=taskmanager

# Watch pods being created
kubectl get pods -w

# Scale back down to 2
kubectl scale deployment taskmanager-deployment --replicas=2

# Verify scaling
kubectl get deployments
```

#### Rolling Updates
```bash
# Update to a new image version (from your CI/CD pipeline)
kubectl set image deployment/taskmanager-deployment \
  taskmanager=$DOCKERHUB_USERNAME/task-manager:new-version

# Watch the rolling update progress
kubectl rollout status deployment/taskmanager-deployment

# Check rollout history
kubectl rollout history deployment/taskmanager-deployment

# Rollback if needed
kubectl rollout undo deployment/taskmanager-deployment
```

#### Monitor Your Personal Deployment
```bash
# Check all your resources (automatically in your namespace!)
kubectl get all

# Check resource usage (if metrics-server is available)
kubectl top pods

# View logs from your application
kubectl logs -l app=taskmanager

# Describe your deployment
kubectl describe deployment taskmanager-deployment

# All these commands now work in your namespace without -n flag!
```

#### Clean Up Your Personal Environment
```bash
# Option 1: Delete individual resources
kubectl delete -f my-ingress.yaml
kubectl delete -f my-taskmanager.yaml

# Option 2: Delete entire namespace (removes everything)
# ⚠️ Note: This will switch you back to default context
kubectl delete namespace $STUDENT_NUMBER

# Remove from hosts file (Linux/Mac)
sudo sed -i "/taskmanager-$STUDENT_NUMBER.local/d" /etc/hosts

# Switch back to default context after cleanup
kubectl config use-context default

# Verify cleanup (this will show "No resources found" since namespace is gone)
kubectl get all --namespace $STUDENT_NUMBER
```

#### Context Management Tips for Workshop
```bash
# Quick reference commands you'll use frequently:

# Check what namespace you're currently in
kubectl config view --minify -o jsonpath='{..namespace}'

# Switch to your student context
kubectl config use-context $STUDENT_NUMBER

# Switch to default/shared context (if needed)
kubectl config use-context default

# List all available contexts
kubectl config get-contexts

# If you accidentally switch contexts, get back to your namespace:
kubectl config set-context --current --namespace=$STUDENT_NUMBER
```

### Exercise 5: Debugging and Troubleshooting

#### Common Kubectl Commands for Debugging
```bash
# Get overview of all resources
kubectl get all

# Detailed information about a pod
kubectl describe pod <pod-name>

# View pod logs
kubectl logs <pod-name>

# Follow logs in real-time
kubectl logs -f <pod-name>

# Execute commands in a running pod
kubectl exec -it <pod-name> -- /bin/bash

# Check events (very useful for troubleshooting)
kubectl get events --sort-by=.metadata.creationTimestamp
```

#### Common Issues and Solutions

**Issue 1: Pod stuck in Pending state**
```bash
# Check what's wrong
kubectl describe pod <pod-name>

# Common causes:
# - Not enough resources (CPU/Memory)
# - Image pull errors
# - Node selector issues
```

**Issue 2: CrashLoopBackOff**
```bash
# Check pod logs
kubectl logs <pod-name>

# Check previous logs if pod restarted
kubectl logs <pod-name> --previous

# Common causes:
# - Application error on startup
# - Wrong environment variables
# - Missing dependencies
```

**Issue: Service not accessible**
```bash
# Check service endpoints
kubectl get endpoints

# Test connectivity from inside cluster
kubectl run test-pod --image=busybox --rm -it --restart=Never -- wget -qO- http://taskmanager-service

# For external database connectivity issues
kubectl exec -it <pod-name> -- ping <VM_IP_ADDRESS>
kubectl exec -it <pod-name> -- telnet <VM_IP_ADDRESS> 5432
```

**Issue: Database connection refused**
```bash
# Check if PostgreSQL is accepting connections on the VM
# On the VM:
sudo systemctl status postgresql
sudo netstat -tlnp | grep 5432

# Check PostgreSQL configuration
sudo cat /etc/postgresql/*/main/postgresql.conf | grep listen_addresses
sudo cat /etc/postgresql/*/main/pg_hba.conf | grep host

# Make sure PostgreSQL allows connections from Kubernetes pods
# Add to pg_hba.conf: host all all <KUBERNETES_NETWORK>/24 md5
```

---

## Part 3: Integration & Advanced Topics

### ConfigMaps and Secrets (Better Configuration Management)

Let's explore how to properly manage configuration in Kubernetes using the sample files.

#### Step 1: Explore Sample Configuration Files
```bash
# Navigate to the sample directory
cd ../k8s-sample

# View the sample ConfigMap (safe to commit to Git)
cat configmap-sample.yaml

# View the sample Secret (⚠️ NEVER commit real secrets!)
cat secret-sample.yaml

# Read the security guidelines
cat README.md
```

#### Step 2: Create Sample Resources (Learning Only)
```bash
# Create the sample ConfigMap
kubectl apply -f configmap-sample.yaml

# Create the sample Secret (educational purposes only!)
kubectl apply -f secret-sample.yaml

# View created resources
kubectl get configmaps
kubectl get secrets
```

#### Step 3: Inspect the Resources
```bash
# View ConfigMap contents (visible)
kubectl describe configmap app-config

# View Secret metadata (data hidden for security)
kubectl describe secret app-secrets

# Decode a secret value (learning only)
kubectl get secret app-secrets -o jsonpath='{.data.DB_USERNAME}' | base64 -d
```

#### Step 4: Create Production-Ready Secrets
Instead of YAML files, create secrets securely:
```bash
# Create secrets from command line (recommended)
kubectl create secret generic taskmanager-secrets \
  --from-literal=SECRET_KEY=your-production-secret-key \
  --from-literal=DB_PASSWORD=your-vm-db-password

# Verify the secret was created
kubectl get secrets taskmanager-secrets
```

#### Step 5: Update Task Manager to Use Secrets
```bash
# Go back to main k8s directory
cd ../k8s

# Edit the taskmanager deployment to use the secret
# Replace the hardcoded SECRET_KEY and DB_PASSWORD with secret references
```

Here's how to update the deployment to use secrets:
```yaml
env:
- name: DATABASE_URL
  value: "postgresql://dbuser:$(DB_PASSWORD)@<VM_IP>:5432/taskmanager"
- name: SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: taskmanager-secrets
      key: SECRET_KEY
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: taskmanager-secrets
      key: DB_PASSWORD
```

### Kubernetes + CI/CD Integration (If Time Permits)

#### Extending Your GitHub Actions Workflow

Add Kubernetes deployment to your existing `cd.yaml`:

```yaml
# Add this job to your existing cd.yaml
  deploy-to-kubernetes:
    name: Deploy to Kubernetes
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v5
        
      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.28.0'
      
      - name: Configure kubeconfig
        run: |
          # This would be your actual cluster configuration
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
      
      - name: Deploy to Kubernetes
        run: |
          # Update image in deployment
          kubectl set image deployment/taskmanager-deployment \
            taskmanager=${{ secrets.DOCKER_USERNAME }}/task-manager:${{ github.sha }}
          
          # Wait for rollout to complete
          kubectl rollout status deployment/taskmanager-deployment
          
          # Verify deployment
          kubectl get pods -l app=taskmanager
```

#### The Complete CI/CD to Kubernetes Flow
```
Code Push → GitHub Actions → Build Image → Push to Registry → Deploy to Kubernetes → Verify
```

**Benefits:**
- **Automated deployments** - No manual kubectl commands
- **Consistent environments** - Same deployment process every time  
- **Rollback capability** - Easy to revert to previous versions
- **Audit trail** - Complete history of deployments

### Monitoring and Observability

#### Basic Monitoring with kubectl
```bash
# Monitor resource usage
kubectl top nodes
kubectl top pods

# Watch resource changes in real-time
kubectl get pods -w

# Check cluster events
kubectl get events --sort-by=.metadata.creationTimestamp
```

#### Application Health Checks
Add health checks to your deployment:
```yaml
spec:
  containers:
  - name: taskmanager
    image: your-username/task-manager:latest
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 5
```

### Next Steps: Production Kubernetes

#### What We Covered Today (Introduction Level)
- ✅ Basic Kubernetes concepts
- ✅ Local development setup
- ✅ Deploying applications to Kubernetes
- ✅ Basic scaling and updates
- ✅ Configuration management

#### What's Next (Production Level)
- **Managed Kubernetes**: AWS EKS, Google GKE, Azure AKS
- **Advanced Networking**: Ingress controllers, network policies
- **Storage**: Persistent volumes, storage classes
- **Security**: RBAC, pod security standards, network policies
- **Monitoring**: Prometheus, Grafana, logging aggregation
- **GitOps**: ArgoCD, FluxCD for deployment automation
- **Service Mesh**: Istio, Linkerd for microservices communication

---

## Workshop Summary & Assessment

### Individual Checkpoints
Each student should have:
- [ ] Successfully set up a local Kubernetes environment
- [ ] Deployed the Task Manager application to Kubernetes with external PostgreSQL on VM
- [ ] Configured proper database connectivity between Kubernetes and VM
- [ ] Scaled the application up and down
- [ ] Understood the relationship between Pods, Deployments, and Services
- [ ] Explored ConfigMaps and Secrets for configuration management
- [ ] Set up Ingress for external access
- [ ] Troubleshot common Kubernetes and connectivity issues
- [ ] Understood how Kubernetes integrates with CI/CD (if covered)

### Key Takeaways
1. **Kubernetes orchestrates containers at scale** - Beyond single-machine Docker
2. **Declarative configuration** - Describe desired state, Kubernetes makes it happen
3. **Self-healing and scaling** - Automatically handles failures and load
4. **Production readiness** - Foundation for running applications at enterprise scale
5. **CI/CD integration** - Natural extension of automated deployment pipelines

## Architecture Overview

### Workshop Infrastructure
```
┌─────────────────┐    ┌──────────────────────────────┐
│  PostgreSQL VM  │    │       Kubernetes Cluster     │
│                 │    │                              │
│  ┌──────────┐   │    │  ┌─────────┐  ┌─────────┐   │
│  │PostgreSQL│   │    │  │  Pod 1  │  │  Pod 2  │   │
│  │Port: 5432│◄──┼────┼──┤Task Mgr │  │Task Mgr │   │
│  └──────────┘   │    │  └─────────┘  └─────────┘   │
│                 │    │       ▲                     │
└─────────────────┘    │       │                     │
                       │  ┌─────────┐                │
                       │  │ Service │                │
                       │  │(LoadBal)│                │
                       │  └─────────┘                │
                       │       ▲                     │
                       │  ┌─────────┐                │
                       │  │ Ingress │                │
                       │  │Controller│                │
                       │  └─────────┘                │
                       └──────────▲───────────────────┘
                                  │
                            External Traffic
                         (taskmanager.local)
```

This architecture demonstrates:
- **Separation of concerns**: Database on VM, application in Kubernetes
- **Hybrid infrastructure**: Mix of traditional VMs and container orchestration  
- **External connectivity**: Kubernetes pods connecting to external services
- **Production patterns**: How real applications often integrate existing infrastructure

---

## Complete Kubernetes Manifests

### All-in-One Deployment File
Since PostgreSQL runs on a VM, here's a simplified deployment file for the Task Manager application only.

Create this as a reference - `k8s/taskmanager-complete.yaml`:
```yaml
# Task Manager Application - Complete Deployment
# PostgreSQL runs on external VM

# Deployment - Manages the application pods
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taskmanager
spec:
  replicas: 2
  selector:
    matchLabels:
      app: taskmanager
  template:
    metadata:
      labels:
        app: taskmanager
    spec:
      containers:
      - name: app
        image: your-dockerhub-username/task-manager:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: "postgresql://dbuser:dbpass123@<VM_IP_ADDRESS>:5432/taskmanager"
        - name: SECRET_KEY
          value: "kubernetes-secret"
        livenessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
# Service - Provides internal networking
apiVersion: v1
kind: Service
metadata:
  name: taskmanager
spec:
  selector:
    app: taskmanager
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
---
# Ingress - Provides external access
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: taskmanager-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: taskmanager.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: taskmanager
            port:
              number: 80
```

### Quick Deploy Commands
```bash
# Navigate to the k8s directory
cd k8s

# Update the Docker image name and VM IP address
sed -i 's/your-dockerhub-username/YOUR_ACTUAL_USERNAME/g' 03-taskmanager.yaml
sed -i 's/<VM_IP_ADDRESS>/YOUR_VM_IP/g' 03-taskmanager.yaml

# Deploy the application
kubectl apply -f 03-taskmanager.yaml

# Deploy ingress for external access
kubectl apply -f 04-ingress.yaml

# Check status
kubectl get all

# Access application via port-forward
kubectl port-forward service/taskmanager-service 8080:80

# Or via ingress (after setting up hosts file)
echo "127.0.0.1 taskmanager.local" | sudo tee -a /etc/hosts
# Visit http://taskmanager.local

# Scale application
kubectl scale deployment taskmanager-deployment --replicas=5

# Update application
kubectl set image deployment/taskmanager-deployment \
  taskmanager=your-username/task-manager:new-version

# Clean up
kubectl delete -f 03-taskmanager.yaml
kubectl delete -f 04-ingress.yaml
```

---

## Troubleshooting Guide

### Common Issues & Solutions

**Issue: minikube won't start**
```bash
# Check Docker is running
docker ps

# Reset minikube
minikube delete
minikube start

# Check resources
minikube status
```

**Issue: Image pull errors**
```bash
# Check if image exists
docker pull your-username/task-manager:latest

# Use local images in minikube
minikube docker-env
eval $(minikube docker-env)
docker build -t task-manager .
```

**Issue: Service not accessible**
```bash
# For minikube LoadBalancer services
minikube tunnel

# Check service endpoints
kubectl get endpoints

# Use port-forward as fallback
kubectl port-forward service/taskmanager 8080:80
```

---

## Resources for Continued Learning

### Official Documentation
- [Kubernetes.io](https://kubernetes.io/) - Official Kubernetes documentation
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes by Example](https://kubernetesbyexample.com/)

### Interactive Learning
- [Katacoda Kubernetes Scenarios](https://katacoda.com/courses/kubernetes)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)
- [Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)

### Production Learning Path
1. **CKA (Certified Kubernetes Administrator)** - Operations focus
2. **CKAD (Certified Kubernetes Application Developer)** - Development focus
3. **Cloud Provider Kubernetes** - EKS, GKE, AKS specific training

---

**🎉 Congratulations! You've completed the 4-day DevOps workshop journey from basic Git to production-ready Kubernetes orchestration!**

**Your DevOps Journey:**
- **Day 1**: Git & GitHub fundamentals
- **Day 2**: Docker containerization  
- **Day 3**: CI/CD automation with GitHub Actions
- **Day 4**: Kubernetes container orchestration

**You're now ready to build and deploy modern cloud-native applications! 🚀**

---

## Appendix: Hashing vs Encryption vs Encoding

### Understanding Hashing, Encryption, and Encoding

As DevOps engineers, you'll frequently work with sensitive data like passwords, API keys, and certificates. Understanding the differences between hashing, encryption, and encoding is crucial for proper security implementation.

| Aspect             | **Hashing**                       | **Encryption**              | **Encoding**          |
| ------------------ | --------------------------------- | --------------------------- | --------------------- |
| **Purpose**        | Data integrity & password storage | Data confidentiality        | Data representation   |
| **Reversible**     | ❌ No (one-way function)           | ✅ Yes (with key)            | ✅ Yes (no key needed) |
| **Key Required**   | ❌ No                              | ✅ Yes (secret key)          | ❌ No                  |
| **Security Focus** | Integrity & authentication        | Confidentiality             | Compatibility         |
| **Output Length**  | Fixed (e.g., 32 chars for MD5)    | Variable (depends on input) | Variable              |

### **1. Hashing - One-Way Data Integrity**

**What it does:** Converts input data into a fixed-length string (digest) that cannot be reversed.

**Common Algorithms:** MD5, SHA-256, SHA-512, bcrypt, Argon2

**Examples:**
```bash
# SHA-256 hash example
echo "password123" | sha256sum
# Output: ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f

# Same input always produces same hash
echo "password123" | sha256sum
# Output: ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f

# Different input produces completely different hash  
echo "password124" | sha256sum
# Output: 8bb0cf6eb9b17d0f7d22b456f121257dc1254e1f01665370476383ea776df414
```

**Use Cases:**
- **Password storage** in databases
- **File integrity verification** (checksums)
- **Git commit IDs** (Git uses SHA-1)
- **Docker image layers** identification
- **API token generation**


### **2. Encryption - Reversible Data Protection**

**What it does:** Transforms data using a secret key, making it unreadable without the key.

**Types:**
- **Symmetric:** Same key for encryption and decryption (AES)
- **Asymmetric:** Different keys for encryption and decryption (RSA)

**Examples:**
```bash
# Symmetric encryption with OpenSSL
echo "sensitive data" | openssl enc -aes-256-cbc -a -salt -k "mypassword"
# Output: U2FsdGVkX18rKz... (encrypted data)

# Decrypt the data
echo "U2FsdGVkX18rKz..." | openssl enc -aes-256-cbc -a -d -k "mypassword"  
# Output: sensitive data
```

**Use Cases:**
- **API keys and tokens** in CI/CD pipelines  
- **TLS/SSL certificates** for HTTPS
- **Container image secrets** (Docker secrets)
- **Kubernetes secrets** (encrypted at rest)
- **Encrypted storage volumes**


### **3. Encoding - Data Format Conversion**

**What it does:** Converts data from one format to another for compatibility, not security.

**Common Types:** Base64, URL encoding, ASCII, UTF-8

**Examples:**
```bash
# Base64 encoding (common in Kubernetes)
echo "Hello World" | base64
# Output: SGVsbG8gV29ybGQK

# Base64 decoding
echo "SGVsbG8gV29ybGQK" | base64 -d
# Output: Hello World
```

**DevOps Use Cases:**
- **Kubernetes secrets** (Base64 encoded, not encrypted!)
- **Docker image layers** (tar + gzip encoding)
- **Configuration files** (YAML, JSON formatting)
- **Log file compression** (gzip, zip)
- **Binary data transmission** (Base64 in APIs)

**Example in Practice:**
```yaml
# Kubernetes Secret with Base64 encoding
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
data:
  username: YWRtaW4=        # "admin" in Base64
  password: cGFzc3dvcmQ=    # "password" in Base64
```

### **Security Implications**

| Scenario                 | ❌ Wrong Approach      | ✅ Correct Approach                      |
| ------------------------ | --------------------- | --------------------------------------- |
| **Storing passwords**    | Plain text or Base64  | Hashed with bcrypt/Argon2               |
| **API keys in code**     | Hardcoded strings     | Encrypted secrets/env vars              |
| **Database connections** | Plain text configs    | Encrypted connection strings            |
| **Container secrets**    | Environment variables | Kubernetes secrets + encryption at rest |
| **CI/CD credentials**    | Repository files      | Encrypted pipeline secrets              |

### **Key Takeaways Security**

1. **Use hashing for**: Password storage, file integrity, unique identifiers
2. **Use encryption for**: Sensitive data that needs to be retrieved later
3. **Use encoding for**: Data format compatibility, not security
4. **Never rely on encoding (like Base64) for security** - it's easily reversible
5. **Always encrypt secrets at rest and in transit** in production systems
6. **Use proper key management** - rotate keys regularly, use key vaults
7. **Implement defense in depth** - combine multiple security layers