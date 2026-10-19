output "target_host_name" {
  value       = local.target_host_name
  description = "The host name used in the ALB listener rule host header"
}

output "backend_dns_domain" {
  value       = local.backend_dns_domain
  description = "The Route53 zone the DNS record is created in"
}

output "dns_record_name" {
  value       = var.simple_dns_name ? local.simple_backend_dns_record : local.backend_dns_record
  description = "The Route53 record name"
}
