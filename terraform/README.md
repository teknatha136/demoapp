# Terraform Demo - Infrastructure as Code

This is a simple demonstration of how to create cloud infrastructure using code instead of clicking buttons in a web console.

## 🎯 Learning Goal
Show students that cloud resources (VMs, networks, databases, etc.) can be created, modified, and destroyed using **code** instead of manual point-and-click operations.

## 🚀 Quick Demo

Since we're already authenticated with `doctl`, this is super simple:

```bash
# Initialize Terraform (first time only)
terraform init

# See what will be created
terraform plan

# Create the VM
terraform apply
# Type 'yes' when prompted

# Get the VM's IP address
terraform output vm_ip_address

# Destroy the VM when done
terraform destroy
# Type 'yes' when prompted
```

## 📋 What This Creates

- **One Ubuntu VM** in DigitalOcean (Singapore region)
- **Basic size**: 1 vCPU, 1GB RAM (~$6/month)
- **Tagged**: `terraform-demo`, `learning`

## 🔍 Key Concepts to Highlight

### Infrastructure as Code (IaC)
- **Declarative**: You describe what you want, not how to build it
- **Version Control**: Infrastructure changes can be tracked in git
- **Reproducible**: Same code = same infrastructure every time
- **Collaborative**: Teams can review infrastructure changes

### Terraform Workflow
1. **Write** configuration (`.tf` files)
2. **Plan** changes (`terraform plan`)
3. **Apply** changes (`terraform apply`)
4. **Manage** state (Terraform tracks what exists)

## 💡 Discussion Points for Students

**Traditional Way (Manual)**:
- Log into DigitalOcean web console
- Click "Create Droplet"
- Select image, size, region
- Configure settings
- Click "Create"
- Repeat for each environment...

**IaC Way (Terraform)**:
- Write configuration once
- Run `terraform apply`
- Same result, every time
- Easy to modify, version, and share

## 🔧 Simple Modifications to Show

Students can try changing values in `main.tf`:

```hcl
# Change the VM size
size = "s-2vcpu-2gb"  # More powerful

# Change the region  
region = "fra1"       # Move to Frankfurt

# Change the name
name = "my-custom-vm"
```

Then run `terraform plan` to see what would change, and `terraform apply` to make the changes.

## 🧹 Important: Cleanup

```bash
# Always destroy demo resources to avoid charges
terraform destroy
```

## 🎓 Key Takeaways

- **Infrastructure as Code** makes cloud management predictable and repeatable
- **Terraform** is cloud-agnostic (works with AWS, Azure, GCP, etc.)
- **Version control** your infrastructure just like your application code
- **Automation** reduces human errors and saves time
- **Collaboration** becomes easier with shared configuration files

---

**Time needed**: 5-10 minutes for basic demo
**Cost**: ~$0.01 for a quick demo (if you destroy immediately)