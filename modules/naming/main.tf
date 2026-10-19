# Pure naming logic (no providers) so it can be tested without AWS access
locals {
  # Base service name - computed once, respects override_dns_name
  base_service_name = var.override_dns_name != "" ? var.override_dns_name : replace(var.component_name, "/-service$/", "")

  # Environment handling
  # Secondary live regions (e.g. live_eu_west_2) drop the "live" part, leaving the region (eu-west-2)
  fixed_env_name = replace(replace(var.env, "/^live_(.+)$/", "$1"), "_", "-")
  env_prefix     = var.env == "live" ? "" : "${local.fixed_env_name}-"

  # ALB listener host name
  target_host_name = "${local.env_prefix}${local.base_service_name}.${var.dns_domain}"

  # Route53 DNS name - reuses base_service_name to respect override_dns_name
  logical_service_name = var.env == "live" && var.aws_account_alias == "" ? local.base_service_name : "${local.fixed_env_name}-${local.base_service_name}"

  full_account_name         = can(regex("^live(_.+)?$", var.env)) ? (var.aws_account_alias == "" ? "" : "${var.aws_account_alias}prod.") : "${var.aws_account_alias}dev."
  backend_dns_domain        = "${local.full_account_name}${var.backend_dns}"
  backend_dns_record        = "${local.logical_service_name}.${local.backend_dns_domain}"
  simple_backend_dns_record = "${local.env_prefix}${local.base_service_name}.${local.backend_dns_domain}"
}
