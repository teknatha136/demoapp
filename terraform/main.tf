# Simple Terraform example to demonstrate Infrastructure as Code
# This creates a basic DigitalOcean VM (Droplet)

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.40"
    }
  }
}

# Configure the DigitalOcean Provider
# Uses doctl authentication automatically
provider "digitalocean" {
}

# Create a simple VM
resource "digitalocean_droplet" "demo_vm" {
  image  = "ubuntu-22-04-x64"
  name   = "terraform-demo-vm"
  region = "sgp1"
  size   = "s-1vcpu-1gb"
  
  tags = ["terraform-demo", "learning"]
}