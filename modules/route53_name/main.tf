variable "env" {}

variable "aws_account_alias" {}

variable "backend_dns" {}

variable "base_service_name" {}

variable "simple_dns_name" {
  type    = bool
  default = false
}

locals {
  fixed_env_name = replace(var.env, "_", "-")
  env_prefix     = var.env == "live" ? "" : "${local.fixed_env_name}-"

  logical_service_name = var.env == "live" && var.aws_account_alias == "" ? var.base_service_name : "${local.fixed_env_name}-${var.base_service_name}"

  full_account_name  = can(regex("^live(_.+)?$", var.env)) ? (var.aws_account_alias == "" ? "" : "${var.aws_account_alias}prod.") : "${var.aws_account_alias}dev."
  backend_dns_domain = "${local.full_account_name}${var.backend_dns}"

  # simple name: live -> no prefix, live_<region>/live-<region> -> "<region>-" (drops "live-"), others keep env prefix
  live_region       = try(regex("^live[_-](.+)$", var.env)[0], "")
  simple_env_prefix = local.live_region != "" ? "${replace(local.live_region, "_", "-")}-" : local.env_prefix

  backend_dns_record        = "${local.logical_service_name}.${local.backend_dns_domain}"
  simple_backend_dns_record = "${local.simple_env_prefix}${var.base_service_name}.${local.backend_dns_domain}"
}

output "backend_dns_domain" {
  value = local.backend_dns_domain
}

output "record_name" {
  value = var.simple_dns_name ? local.simple_backend_dns_record : local.backend_dns_record
}
