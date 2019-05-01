# fixture
module "backend_service_routing" {
  source = "../.."

  env              = "${var.env}"
  component_name   = "cognito-service"
  dns_domain       = "domain.com"
  priority         = "10"
  alb_listener_arn = "alb:listener"
  alb_dns_name     = "alb.dns.name.com"
  vpc_id           = "${var.platform_config["vpc"]}" # optional
  aws_account_alias = "${var.aws_account_alias}"
  backend_dns       = "${var.backend_dns}"
}

# configure provider to not try too hard talking to AWS API
provider "aws" {
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_get_ec2_platforms      = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
  max_retries                 = 1
  access_key                  = "a"
  secret_key                  = "a"
  region                      = "eu-west-1"
}

# variables
variable "env" {}

variable "platform_config" {
  type = "map"
}

variable "aws_account_alias" {}

variable "backend_dns" {}
