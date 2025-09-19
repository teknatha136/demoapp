# Output the VM's public IP address
output "vm_ip_address" {
  description = "Public IP address of the demo VM"
  value       = digitalocean_droplet.demo_vm.ipv4_address
}

# Output the VM name
output "vm_name" {
  description = "Name of the created VM"
  value       = digitalocean_droplet.demo_vm.name
}

# Output SSH connection command
output "ssh_connection" {
  description = "SSH connection command"
  value       = "ssh root@${digitalocean_droplet.demo_vm.ipv4_address}"
}