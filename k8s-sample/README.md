# README: Sample Configuration Files

⚠️  **SECURITY WARNING**: These are sample files for learning purposes only!
Never commit real secrets to Git repositories!

## Files in This Directory

### `configmap-sample.yaml`
- **Purpose**: Shows how to store non-sensitive configuration
- **Contains**: Application settings, feature flags, file-based config
- **Safe to commit**: Yes, contains no sensitive information

### `secret-sample.yaml`
- **Purpose**: Shows how to store sensitive data like passwords and API keys
- **Contains**: Sample credentials (base64 encoded)
- **Safe to commit**: ⚠️  NO! This is just for learning - use fake data only

## How to Use ConfigMaps and Secrets

### Step 1: Create Resources
```bash
# Create the ConfigMap
kubectl apply -f configmap-sample.yaml

# Create the Secret (learning only - don't do this in real projects!)
kubectl apply -f secret-sample.yaml

# View created resources
kubectl get configmaps
kubectl get secrets
```

### Step 2: Inspect Resources
```bash
# View ConfigMap contents
kubectl describe configmap app-config

# View Secret metadata (data is hidden for security)
kubectl describe secret app-secrets

# Decode secret values (for learning/debugging only)
kubectl get secret app-secrets -o yaml
```

### Step 3: Use in Deployments
Reference the ConfigMap and Secret in your Pod/Deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      containers:
      - name: app
        image: my-app:latest
        env:
        # Get single value from ConfigMap
        - name: DEBUG_MODE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: DEBUG_MODE
        
        # Get single value from Secret
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DB_PASSWORD
        
        # Load all ConfigMap values as environment variables
        envFrom:
        - configMapRef:
            name: app-config
        
        # Mount ConfigMap as files
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
        
        # Mount Secret as files
        - name: secret-volume
          mountPath: /etc/secrets
      
      volumes:
      # ConfigMap as volume
      - name: config-volume
        configMap:
          name: app-config
      
      # Secret as volume
      - name: secret-volume
        secret:
          secretName: app-secrets
```

## Best Practices for Production

### ConfigMaps
✅ **Do:**
- Store non-sensitive configuration
- Use for application settings, feature flags
- Commit to version control
- Use descriptive names and labels

❌ **Don't:**
- Store passwords or API keys
- Make them too large (1MB limit)

### Secrets
✅ **Do:**
- Store sensitive data only
- Use external secret management (Vault, AWS Secrets Manager)
- Set up RBAC (Role-Based Access Control)
- Use different secrets for different environments

❌ **Don't:**
- Commit to Git repositories
- Log secret values
- Share between environments
- Store in plain text

## Real-World Secret Management

Instead of storing secrets in YAML files, use:

### Option 1: kubectl commands
```bash
# Create secret from command line
kubectl create secret generic app-secrets \
  --from-literal=DB_USERNAME=dbuser \
  --from-literal=DB_PASSWORD=secretpass

# Create secret from files
kubectl create secret generic app-secrets \
  --from-file=db-username.txt \
  --from-file=db-password.txt
```

### Option 2: External Secret Management
- **HashiCorp Vault**
- **AWS Secrets Manager**
- **Azure Key Vault**
- **Google Secret Manager**
- **External Secrets Operator** (recommended for Kubernetes)

### Option 3: Sealed Secrets
- Encrypt secrets in Git
- Only the cluster can decrypt them
- Safe to commit encrypted versions

## Cleanup

```bash
# Remove the sample resources
kubectl delete configmap app-config
kubectl delete secret app-secrets
kubectl delete secret tls-secret
kubectl delete secret docker-registry-secret
```

## Security Reminder

🔒 **Remember**: These samples use fake data for learning. In real projects:
1. Never commit secrets to Git
2. Use external secret management systems
3. Implement proper RBAC
4. Rotate secrets regularly
5. Monitor access to secrets