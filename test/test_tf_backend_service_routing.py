import unittest
from subprocess import check_call, check_output


class TestTFBackendRouter(unittest.TestCase):

    def setUp(self):
        check_call(['terraform', 'init', 'test/infra'])

    def test_create_alb_listener_rule_number_of_resources_to_add(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
Plan: 2 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_create_alb_listener_rule(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        print(output)

        # Then
        assert """
  # module.backend_service_routing.aws_alb_listener_rule.rule will be created
  + resource "aws_alb_listener_rule" "rule" {
      + arn          = (known after apply)
      + id           = (known after apply)
      + listener_arn = "arn:aws:alb:eu-west-1:123456789123:alb:listener"
      + priority     = 10
      + region       = "eu-west-1"
      + tags_all     = (known after apply)

      + action {
          + order            = (known after apply)
          + target_group_arn = (known after apply)
          + type             = "forward"
        }

      + condition {
          + host_header {
              + regex_values = []
              + values       = [
                  + "dev-cognito.domain.com",
                ]
            }
        }
      + condition {

          + path_pattern {
              + regex_values = []
              + values       = [
                  + "*",
                ]
            }
        }
    } 
        """.strip() in output

    def test_create_alb_listener_rule_live(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=live',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        print(output)

        # Then
        assert """
  # module.backend_service_routing.aws_alb_listener_rule.rule will be created
  + resource "aws_alb_listener_rule" "rule" {
      + arn          = (known after apply)
      + id           = (known after apply)
      + listener_arn = "arn:aws:alb:eu-west-1:123456789123:alb:listener"
      + priority     = 10
      + region       = "eu-west-1"
      + tags_all     = (known after apply)

      + action {
          + order            = (known after apply)
          + target_group_arn = (known after apply)
          + type             = "forward"
        }

      + condition {
          + host_header {
              + regex_values = []
              + values       = [
                  + "cognito.domain.com",
                ]
            }
        }
      + condition {

          + path_pattern {
              + regex_values = []
              + values       = [
                  + "*",
                ]
            }
        }
    }
        """.strip() in output

    def test_create_alb_listener_rule_extrahosts(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=live',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var', 'extra_listener_host_names=["test.com","example.com"]',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        print(output)

        # Then
        assert """
  # module.backend_service_routing.aws_alb_listener_rule.rule will be created
  + resource "aws_alb_listener_rule" "rule" {
      + arn          = (known after apply)
      + id           = (known after apply)
      + listener_arn = "arn:aws:alb:eu-west-1:123456789123:alb:listener"
      + priority     = 10
      + region       = "eu-west-1"
      + tags_all     = (known after apply)

      + action {
          + order            = (known after apply)
          + target_group_arn = (known after apply)
          + type             = "forward"
        }

      + condition {
          + host_header {
              + regex_values = []
              + values       = [
                  + "cognito.domain.com",
                  + "example.com",
                  + "test.com",
                ]
            }
        }
      + condition {

          + path_pattern {
              + regex_values = []
              + values       = [
                  + "*",
                ]
            }
        }
    }    """.strip() in output

    def test_create_alb_listener_rule_extra_headers(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=live',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var', 'extra_listener_http_header_pairs=[{"http_header_name":"osh_was","values":["here"]}]',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        print(output)

        # Then
        assert """
  # module.backend_service_routing.aws_alb_listener_rule.rule will be created
  + resource "aws_alb_listener_rule" "rule" {
      + arn          = (known after apply)
      + id           = (known after apply)
      + listener_arn = "arn:aws:alb:eu-west-1:123456789123:alb:listener"
      + priority     = 10
      + region       = "eu-west-1"
      + tags_all     = (known after apply)

      + action {
          + order            = (known after apply)
          + target_group_arn = (known after apply)
          + type             = "forward"
        }

      + condition {
          + host_header {
              + regex_values = []
              + values       = [
                  + "cognito.domain.com",
                ]
            }
        }
      + condition {

          + http_header {
              + http_header_name = "osh_was"
              + regex_values     = []
              + values           = [
                  + "here",
                ]
            }
        }
      + condition {

          + path_pattern {
              + regex_values = []
              + values       = [
                  + "*",
                ]
            }
        }
    }    """.strip() in output

    def test_create_aws_alb_target_group(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        print(output)

        # Then
        assert """
  # module.backend_service_routing.aws_alb_target_group.target_group will be created
  + resource "aws_alb_target_group" "target_group" {
      + arn                                = (known after apply)
      + arn_suffix                         = (known after apply)
      + connection_termination             = (known after apply)
      + deregistration_delay               = "10"
      + id                                 = (known after apply)
      + ip_address_type                    = (known after apply)
      + lambda_multi_value_headers_enabled = false
      + load_balancer_arns                 = (known after apply)
      + load_balancing_algorithm_type      = (known after apply)
      + load_balancing_anomaly_mitigation  = (known after apply)
      + load_balancing_cross_zone_enabled  = (known after apply)
      + name                               = "dev-cognito-service"
      + name_prefix                        = (known after apply)
      + port                               = 31337
      + preserve_client_ip                 = (known after apply)
      + protocol                           = "HTTP"
      + protocol_version                   = (known after apply)
      + proxy_protocol_v2                  = false
      + region                             = "eu-west-1"
      + slow_start                         = 0
      + tags                               = {
          + "component" = "cognito-service"
          + "env"       = "dev"
          + "service"   = "dev-cognito-service"
        }
      + tags_all                           = {
          + "component" = "cognito-service"
          + "env"       = "dev"
          + "service"   = "dev-cognito-service"
        }
      + target_type                        = "instance"
      + vpc_id                             = "vpc-12345678"

      + health_check {
          + enabled             = true
          + healthy_threshold   = 2
          + interval            = 5
          + matcher             = "200-299"
          + path                = "/internal/healthcheck"
          + port                = "traffic-port"
          + protocol            = "HTTP"
          + timeout             = 4
          + unhealthy_threshold = 2
        }

      + stickiness {
          + cookie_duration = (known after apply)
          + cookie_name     = (known after apply)
          + enabled         = (known after apply)
          + type            = (known after apply)
        }

      + target_failover {
          + on_deregistration = (known after apply)
          + on_unhealthy      = (known after apply)
        }

      + target_group_health {
          + dns_failover {
              + minimum_healthy_targets_count      = (known after apply)
              + minimum_healthy_targets_percentage = (known after apply)
            }

          + unhealthy_state_routing {
              + minimum_healthy_targets_count      = (known after apply)
              + minimum_healthy_targets_percentage = (known after apply)
            }
        }

      + target_health_state {
          + enable_unhealthy_connection_termination = (known after apply)
          + unhealthy_draining_interval             = (known after apply)
        }
    }    """.strip() in output
