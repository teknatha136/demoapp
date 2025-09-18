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
- Deploy your Task Manager application to Kubernetes
- Understand basic Kubernetes concepts (Pods, Services, Deployments)
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

| Aspect | Docker | Docker Compose | Kubernetes |
|--------|--------|----------------|------------|
| **Scope** | Single container | Multiple containers (one machine) | Multiple containers (multiple machines) |
| **Use Case** | Development/Testing | Local development | Production at scale |
| **High Availability** | No | No | Yes |
| **Auto-scaling** | No | No | Yes |
| **Self-healing** | No | Limited | Yes |
| **Load Balancing** | Manual | Basic | Advanced |
| **Complexity** | Simple | Medium | Complex |

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

### Exercise 1: Setting Up Local Kubernetes

#### Option A: minikube (Recommended for beginners)
```bash
# Install minikube (macOS)
brew install minikube

# Start your local Kubernetes cluster
minikube start

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

#### Option B: kind (Kubernetes in Docker)
```bash
# Install kind
brew install kind

# Create a cluster
kind create cluster --name workshop

# Verify
kubectl cluster-info --context kind-workshop
```

#### Option C: Docker Desktop (If you have it)
```bash
# Enable Kubernetes in Docker Desktop settings
# Then verify:
kubectl cluster-info
```

#### Verify Your Setup
```bash
# Check cluster status
kubectl get nodes

# Expected output:
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   1m    v1.28.3

# Check available resources
kubectl get all --all-namespaces
```

---

## Part 2: Hands-on Kubernetes

### Exercise 2: Your First Pod

Let's start with a simple example before deploying our Task Manager app.

#### Step 1: Create a Simple Pod
Create `k8s/01-hello-pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-kubernetes
  labels:
    app: hello
spec:
  containers:
  - name: hello-container
    image: nginx:alpine
    ports:
    - containerPort: 80
    env:
    - name: MESSAGE
      value: "Hello from Kubernetes!"
```

#### Step 2: Deploy the Pod
```bash
# Create the pod
kubectl apply -f k8s/01-hello-pod.yaml

# Check if it's running
kubectl get pods

# Expected output:
NAME               READY   STATUS    RESTARTS   AGE
hello-kubernetes   1/1     Running   0          30s

# Get more details
kubectl describe pod hello-kubernetes

# Check logs
kubectl logs hello-kubernetes
```

#### Step 3: Access the Pod
```bash
# Forward port to access the pod
kubectl port-forward hello-kubernetes 8080:80

# In another terminal or browser, visit:
# http://localhost:8080
```

#### Step 4: Clean up
```bash
kubectl delete pod hello-kubernetes
```

### Exercise 3: Deploying Task Manager to Kubernetes

Now let's deploy our actual Task Manager application that we've been working with.

#### Step 1: Create Kubernetes Manifests Directory
```bash
mkdir -p k8s
cd k8s
```

#### Step 2: PostgreSQL Database Deployment
Create `k8s/02-postgres.yaml`:
```yaml
# PostgreSQL Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: taskmanager
        - name: POSTGRES_USER
          value: dbuser
        - name: POSTGRES_PASSWORD
          value: dbpass123
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        emptyDir: {}
---
# PostgreSQL Service
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
```

#### Step 3: Task Manager Application Deployment
Create `k8s/03-taskmanager.yaml`:
```yaml
# Task Manager Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taskmanager-deployment
spec:
  replicas: 2  # Run 2 instances for load balancing
  selector:
    matchLabels:
      app: taskmanager
  template:
    metadata:
      labels:
        app: taskmanager
    spec:
      containers:
      - name: taskmanager
        # Use the image from your CI/CD pipeline (Day 3)
        image: your-dockerhub-username/task-manager:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: "postgresql://dbuser:dbpass123@postgres-service:5432/taskmanager"
        - name: SECRET_KEY
          value: "kubernetes-secret-key"
---
# Task Manager Service
apiVersion: v1
kind: Service
metadata:
  name: taskmanager-service
spec:
  selector:
    app: taskmanager
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer  # Exposes the service externally
```

#### Step 4: Deploy to Kubernetes
```bash
# Deploy PostgreSQL first
kubectl apply -f k8s/02-postgres.yaml

# Wait for PostgreSQL to be ready
kubectl get pods -l app=postgres

# Deploy Task Manager
kubectl apply -f k8s/03-taskmanager.yaml

# Check all resources
kubectl get all

# Expected output shows deployments, pods, services
NAME                                         READY   STATUS    RESTARTS   AGE
pod/postgres-deployment-xxx                  1/1     Running   0          2m
pod/taskmanager-deployment-xxx               1/1     Running   0          1m
pod/taskmanager-deployment-yyy               1/1     Running   0          1m

NAME                           TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/postgres-service       ClusterIP      10.96.158.31    <none>        5432/TCP       2m
service/taskmanager-service    LoadBalancer   10.96.241.45    <pending>     80:32000/TCP   1m
```

#### Step 5: Access Your Application
```bash
# For minikube, get the service URL
minikube service taskmanager-service --url

# Or use port forwarding
kubectl port-forward service/taskmanager-service 8080:80

# Visit http://localhost:8080 in your browser
```

### Exercise 4: Scaling and Updates

#### Scaling Your Application
```bash
# Scale up to 5 replicas
kubectl scale deployment taskmanager-deployment --replicas=5

# Check the scaling
kubectl get pods -l app=taskmanager

# Scale back down
kubectl scale deployment taskmanager-deployment --replicas=2
```

#### Rolling Updates
```bash
# Update to a new image version (from your CI/CD pipeline)
kubectl set image deployment/taskmanager-deployment taskmanager=your-username/task-manager:new-version

# Watch the rolling update
kubectl rollout status deployment/taskmanager-deployment

# Check rollout history
kubectl rollout history deployment/taskmanager-deployment

# Rollback if needed
kubectl rollout undo deployment/taskmanager-deployment
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

**Issue 3: Service not accessible**
```bash
# Check if service endpoints exist
kubectl get endpoints

# Test connectivity from inside cluster
kubectl run test-pod --image=busybox --rm -it --restart=Never -- wget -qO- http://taskmanager-service
```

---

## Part 3: Integration & Advanced Topics

### ConfigMaps and Secrets (Better Configuration Management)

Instead of hardcoding environment variables, use Kubernetes native configuration:

#### Step 1: Create ConfigMap for Application Settings
Create `k8s/04-configmap.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: taskmanager-config
data:
  # Non-sensitive configuration
  DEBUG: "False"
  LOG_LEVEL: "INFO"
  MAX_CONNECTIONS: "100"
```

#### Step 2: Create Secret for Sensitive Data
Create `k8s/05-secrets.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: taskmanager-secrets
type: Opaque
data:
  # Base64 encoded values
  SECRET_KEY: a3ViZXJuZXRlcy1zZWNyZXQta2V5  # "kubernetes-secret-key"
  DB_PASSWORD: ZGJwYXNzMTIz                     # "dbpass123"
```

#### Step 3: Update Deployment to Use ConfigMap and Secrets
```yaml
# Update k8s/03-taskmanager.yaml
spec:
  containers:
  - name: taskmanager
    image: your-username/task-manager:latest
    env:
    - name: DATABASE_URL
      value: "postgresql://dbuser:$(DB_PASSWORD)@postgres-service:5432/taskmanager"
    - name: SECRET_KEY
      valueFrom:
        secretKeyRef:
          name: taskmanager-secrets
          key: SECRET_KEY
    - name: DEBUG
      valueFrom:
        configMapKeyRef:
          name: taskmanager-config
          key: DEBUG
    envFrom:
    - configMapRef:
        name: taskmanager-config
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
- [ ] Deployed the Task Manager application to Kubernetes
- [ ] Scaled the application up and down
- [ ] Understood the relationship between Pods, Deployments, and Services
- [ ] Troubleshot at least one common Kubernetes issue
- [ ] Understood how Kubernetes integrates with CI/CD (if covered)

### Key Takeaways
1. **Kubernetes orchestrates containers at scale** - Beyond single-machine Docker
2. **Declarative configuration** - Describe desired state, Kubernetes makes it happen
3. **Self-healing and scaling** - Automatically handles failures and load
4. **Production readiness** - Foundation for running applications at enterprise scale
5. **CI/CD integration** - Natural extension of automated deployment pipelines

### Real-World Applications
- **High availability** - Applications run across multiple servers
- **Zero-downtime deployments** - Update applications without service interruption
- **Auto-scaling** - Handle traffic spikes automatically
- **Resource efficiency** - Better utilization of infrastructure
- **Portability** - Run anywhere Kubernetes runs (cloud, on-premise)

---

## Complete Kubernetes Manifests

### All-in-One Deployment File
Create `k8s/complete-app.yaml`:
```yaml
# PostgreSQL Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: taskmanager
        - name: POSTGRES_USER
          value: dbuser
        - name: POSTGRES_PASSWORD
          value: dbpass123
        ports:
        - containerPort: 5432
---
# PostgreSQL Service
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
  type: ClusterIP
---
# Task Manager Deployment
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
          value: "postgresql://dbuser:dbpass123@postgres:5432/taskmanager"
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
---
# Task Manager Service
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
  type: LoadBalancer
```

### Quick Deploy Commands
```bash
# Deploy everything
kubectl apply -f k8s/complete-app.yaml

# Check status
kubectl get all

# Access application
minikube service taskmanager --url
# or
kubectl port-forward service/taskmanager 8080:80

# Scale application
kubectl scale deployment taskmanager --replicas=5

# Update application
kubectl set image deployment/taskmanager app=your-username/task-manager:new-version

# Clean up
kubectl delete -f k8s/complete-app.yaml
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