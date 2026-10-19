// Required Variables

# Target of the Route53 CNAME record, e.g. module.alb.dns_name.
variable "alb_dns_name" {
  description = "The DNS name of the ALB to point the DNS at"
}

# Listener the host-header routing rule is attached to (typically the HTTPS listener).
variable "alb_listener_arn" {
  description = "The ARN of the ALB listener to add the rule to."
}

# Used to build the Route53 zone: "<alias>prod.<backend_dns>" for live envs, "<alias>dev.<backend_dns>" otherwise.
# e.g. "acme" -> acmeprod.example.com / acmedev.example.com. For live envs an empty string uses <backend_dns> directly.
variable "aws_account_alias" {
  description = "The AWS account alias where the router is deployed"
  type        = string
}

# Base domain of the Route53 zone the record is created in, e.g. "example.com".
variable "backend_dns" {
  description = "The domain and top level domain used as the address for the ALB"
  type        = string
}

# Environment name, e.g. "live", "qa", "live_eu-west-2".
# - Non-live envs are prefixed to the DNS name (qa -> "qa-<name>"); underscores become hyphens.
# - "live" (exact) has no ALB host prefix. "live_<region>" drops "live" and keeps the region (live_eu_west_2 -> eu-west-2-<name>).
# - Only "live" and "live_<suffix>" (underscore) select the "<alias>prod." zone; anything else uses "<alias>dev.".
variable "env" {
  description = "The name of the environment (included at the front of the DNS name with a hyphen if not live)"
}

# Unique ALB listener rule priority (1-50000); must not clash with other rules on the same listener.
variable "priority" {
  description = "ALB listener rule priority"
}

# VPC the target group is created in.
variable "vpc_id" {
  description = "The identifier of the VPC in which to create the target group."
  type        = string
}

// Optional Variables

# Set to "true" to adopt an existing Route53 record with the same name instead of failing.
variable "allow_overwrite" {
  description = "Allow creation of this record in Terraform to overwrite an existing record, if any."
  type        = string
  default     = "false"
}

# e.g. "cognito-service" -> DNS name "cognito" (the -service suffix is removed) and a target group named after the env + component.
variable "component_name" {
  type        = string
  description = "The name of the component - used by default for the DNS entry (with the -service suffix removed), as well as to give the target group a meaningful name"
  default     = ""
}

variable "deregistration_delay" {
  description = "The amount time for Elastic Load Balancing to wait before changing the state of a deregistering target from draining to unused. The range is 0-3600 seconds."
  type        = string
  default     = "10"
}

# Domain used for the ALB host-header rule: "<env prefix><name>.<dns_domain>", e.g. "domain.com" -> qa-cognito.domain.com.
variable "dns_domain" {
  description = "The top level domain the service should live under. This will be the host used for the rule to route to a target group"
  default     = ""
}

# Set to "true" for long env/component names so the (32 char limited) target group name stays unique.
variable "hash_target_group_name" {
  description = "Include a hash of the target group name when naming it to avoid collisions"
  type        = string
  default     = "false"
}

variable "health_check_interval" {
  description = "The approximate amount of time, in seconds, between health checks of an individual target. Minimum value 5 seconds, Maximum value 300 seconds."
  type        = string
  default     = "5"
}

variable "health_check_healthy_threshold" {
  description = "The number of consecutive health checks successes required before considering an unhealthy target healthy."
  type        = string
  default     = "2"
}

variable "health_check_matcher" {
  description = "The HTTP codes to use when checking for a successful response from a target. You can specify multiple values (for example, \"200,202\") or a range of values (for example, \"200-299\")."
  type        = string
  default     = "200-299"
}

variable "health_check_path" {
  description = "The destination for the health check request."
  type        = string
  default     = "/internal/healthcheck"
}

variable "health_check_timeout" {
  description = "The amount of time, in seconds, during which no response means a failed health check."
  type        = string
  default     = "4"
}

variable "health_check_unhealthy_threshold" {
  description = "The number of consecutive health check failures required before considering the target unhealthy."
  type        = string
  default     = "2"
}

# Replaces the component-derived name in both the ALB host and the Route53 record, e.g. "auth" -> qa-auth.<domain>.
variable "override_dns_name" {
  type        = string
  description = "The first part of the DNS name without the environment (defaults to component_name with -service suffix removed)"
  default     = ""
}

variable "ttl" {
  description = "Time to live"
  default     = "60"
}

# "instance" for EC2/ECS bridge networking, "ip" for awsvpc/Fargate, "lambda" for Lambda targets.
variable "target_type" {
  description = "The possible values are instance (targets are specified by instance ID) or ip (targets are specified by IP address) or lambda (targets are specified by lambda arn)"
  default     = "instance"
}

# Additional hostnames that should also route to this target group, e.g. ["api.example.com"].
variable "extra_listener_host_names" {
  description = "A list of hostname to be included in the host header for the ALB listener rule"
  type        = list(string)
  default     = []
}

# Extra header conditions on the rule, e.g. [{ http_header_name = "X-Tenant", values = ["acme"] }].
variable "extra_listener_http_header_pairs" {
  description = "A list of HTTP headers to be included in the http header condition for the ALB listener rule"
  type        = list(object({
    http_header_name = string,
    values           = set(string)
  }))
  default     = []
}

# Drops the "live-" prefix from the Route53 record of the primary live env. With component "cognito":
#   env             simple_dns_name=false   simple_dns_name=true
#   live            live-cognito            cognito   (with aws_account_alias set)
#   live_eu_west_2  eu-west-2-cognito       eu-west-2-cognito   (regional live envs never carry "live-")
#   qa              qa-cognito              qa-cognito
# With env "live" and no aws_account_alias both modes give "cognito".
variable "simple_dns_name" {
  description = "simplify the name of route53 dns in live env"
  type = bool
  default = false
}