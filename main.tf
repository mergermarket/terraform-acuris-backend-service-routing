module "naming" {
  source = "./modules/naming"

  env               = var.env
  component_name    = var.component_name
  override_dns_name = var.override_dns_name
  dns_domain        = var.dns_domain
  aws_account_alias = var.aws_account_alias
  backend_dns       = var.backend_dns
  simple_dns_name   = var.simple_dns_name
}

locals {
  host_header_host_names = concat([module.naming.target_host_name], var.extra_listener_host_names)
}

resource "aws_alb_listener_rule" "rule" {
  listener_arn = var.alb_listener_arn
  priority     = var.priority

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.target_group.arn
  }

  condition {
    host_header {
      values = local.host_header_host_names
    }
  }

  condition {
    path_pattern {
      values = ["*"]
    }
  }

  dynamic "condition" {
    for_each = var.extra_listener_http_header_pairs
    content {
      http_header {
        http_header_name = condition.value.http_header_name
        values           = condition.value.values
      }
    }
  }
}

locals {
  simplified_env = can(split("_", var.env)) ? split("_", var.env)[0] : var.env

  old_target_group_name = "${replace(replace(replace("${local.simplified_env}-${var.component_name}", "/(.{0,32}).*/", "$1"), "/^-+|-+$/", ""),"_","-")}"

  target_group_name_hash    = "${base64encode(base64sha256("${local.simplified_env}-${var.component_name}"))}"
  target_group_name_postfix = "${replace(replace(replace("${local.target_group_name_hash}", "/(.{0,12}).*/", "$1"), "/^-+|-+$/", ""),"_","-")}"
  target_group_name_prefix  = "${replace(replace(replace("${local.simplified_env}-${var.component_name}", "/(.{0,20}).*/", "$1"), "/^-+|-+$/", ""),"_","-")}"
  target_group_name         = "${local.target_group_name_prefix}${local.target_group_name_postfix}"
  
}

resource "aws_alb_target_group" "target_group" {
  name = var.hash_target_group_name ? local.target_group_name : local.old_target_group_name

  # port will be set dynamically, but for some reason AWS requires a value
  port                 = "31337"
  protocol             = "HTTP"
  vpc_id               = var.vpc_id
  deregistration_delay = var.deregistration_delay
  target_type          = var.target_type

  health_check {
    interval            = var.health_check_interval
    path                = var.health_check_path
    timeout             = var.health_check_timeout
    healthy_threshold   = var.health_check_healthy_threshold
    unhealthy_threshold = var.health_check_unhealthy_threshold
    matcher             = var.health_check_matcher
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    component = var.component_name
    env       = var.env
    service   = "${var.env}-${var.component_name}"
  }
}

data "aws_route53_zone" "dns_domain" {
  name = module.naming.backend_dns_domain
}

resource "aws_route53_record" "dns_record" {
  zone_id = data.aws_route53_zone.dns_domain.zone_id
  name    = module.naming.dns_record_name

  type            = "CNAME"
  records         = [var.alb_dns_name]
  ttl             = var.ttl
  allow_overwrite = var.allow_overwrite

  depends_on = [aws_alb_listener_rule.rule]
}
