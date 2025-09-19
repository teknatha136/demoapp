# README: Kubernetes Introduction Files

This directory contains simple Kubernetes files to learn basic concepts.

## Files

### `hello-pod.yaml`
- **Purpose**: Learn what a Pod is and basic Kubernetes syntax
- **Contains**: A simple nginx Pod with detailed comments explaining each section

## How to Use

### Step 1: Deploy the Pod
```bash
# Apply the Pod configuration
kubectl apply -f hello-pod.yaml

# Check if the Pod is running
kubectl get pods

# Expected output:
# NAME        READY   STATUS    RESTARTS   AGE
# hello-pod   1/1     Running   0          30s
```

### Step 2: Inspect the Pod
```bash
# Get detailed information about the Pod
kubectl describe pod hello-pod

# Check the logs from the container
kubectl logs hello-pod

# See the Pod's IP address and other details
kubectl get pod hello-pod -o wide
```

### Step 3: Access the Pod
```bash
# Forward a local port to the Pod's port
kubectl port-forward hello-pod 8080:80

# In another terminal or browser, visit:
# http://localhost:8080
# You should see the nginx welcome page
```

### Step 4: Explore the Pod
```bash
# Execute a command inside the running container
kubectl exec hello-pod -- ls /usr/share/nginx/html

# Get an interactive shell inside the container
kubectl exec -it hello-pod -- /bin/sh
# Now you're inside the container! Try:
# - ls /
# - ps aux
# - env | grep WELCOME
# - exit (to leave the container)
```

### Step 5: Clean Up
```bash
# Delete the Pod
kubectl delete pod hello-pod

# Verify it's gone
kubectl get pods
```

## Key Learning Points

1. **Pods are temporary**: When you delete a Pod, it's gone forever
2. **Containers share networking**: All containers in a Pod share the same IP
3. **Labels are important**: They're used to organize and select resources
4. **Resource management**: Always set requests and limits for containers
5. **YAML structure**: Every Kubernetes resource has apiVersion, kind, metadata, and spec

## What's Next?

After understanding Pods, you'll learn about:
- **Deployments**: Manage multiple Pods and handle updates
- **Services**: Provide stable networking to Pods
- **ConfigMaps & Secrets**: Manage configuration and sensitive data

The main `k8s/` directory contains the complete application deployment files.