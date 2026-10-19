# fixture - exercises the naming logic only, no AWS provider required
module "naming" {
  source = "../../modules/naming"

  env               = var.env
  component_name    = var.component_name
  override_dns_name = var.override_dns_name
  dns_domain        = "domain.com"
  aws_account_alias = var.aws_account_alias
  backend_dns       = "testbackend.com"
  simple_dns_name   = var.simple_dns_name
}

output "target_host_name" {
  value = module.naming.target_host_name
}

output "backend_dns_domain" {
  value = module.naming.backend_dns_domain
}

output "dns_record_name" {
  value = module.naming.dns_record_name
}

# variables
variable "env" {}

variable "component_name" {
  default = "cognito-service"
}

variable "override_dns_name" {
  default = ""
}

variable "aws_account_alias" {
  default = "awsaccount"
}

variable "simple_dns_name" {
  type    = bool
  default = false
}
