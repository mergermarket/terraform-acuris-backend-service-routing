# fixture: exercises only the Route53 naming logic (no AWS calls)
module "route53_name" {
  source = "../../modules/route53_name"

  env               = var.env
  aws_account_alias = var.aws_account_alias
  backend_dns       = "testbackend.com"
  base_service_name = "cognito"
  simple_dns_name   = var.simple_dns_name
}

variable "env" {}

variable "aws_account_alias" {
  default = "awsaccount"
}

variable "simple_dns_name" {
  type = bool
}

output "record_name" {
  value = module.route53_name.record_name
}
