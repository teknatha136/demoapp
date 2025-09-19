# Simple variables for the Terraform demo

# Optional: Customize the VM name
variable "vm_name" {
  description = "Name for the demo VM"
  type        = string
  default     = "terraform-demo-vm"
}

# Optional: Choose region
variable "region" {
  description = "DigitalOcean region"
  type        = string
  default     = "sgp1"
}