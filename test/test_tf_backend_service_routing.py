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

        # Then
        assert """
  # module.backend_service_routing.aws_alb_listener_rule.rule will be created
  + resource "aws_alb_listener_rule" "rule" {
      + arn          = (known after apply)
      + id           = (known after apply)
      + listener_arn = "arn:aws:alb:eu-west-1:123456789123:alb:listener"
      + priority     = 10
      + tags_all     = (known after apply)

      + action {
          + order            = (known after apply)
          + target_group_arn = (known after apply)
          + type             = "forward"
        }

      + condition {
          + host_header {
              + values = [
                  + "dev-cognito.domain.com",
                ]
            }
        }
      + condition {

          + path_pattern {
              + values = [
                  + "*",
                ]
            }
        }
    }       """.strip() in output

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

        # Then
        assert """
  # module.backend_service_routing.aws_alb_listener_rule.rule will be created
  + resource "aws_alb_listener_rule" "rule" {
      + arn          = (known after apply)
      + id           = (known after apply)
      + listener_arn = "arn:aws:alb:eu-west-1:123456789123:alb:listener"
      + priority     = 10
      + tags_all     = (known after apply)

      + action {
          + order            = (known after apply)
          + target_group_arn = (known after apply)
          + type             = "forward"
        }

      + condition {
          + host_header {
              + values = [
                  + "cognito.domain.com",
                ]
            }
        }
      + condition {

          + path_pattern {
              + values = [
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

        # Then
        assert """# module.backend_service_routing.aws_alb_target_group.target_group will be created
  + resource "aws_alb_target_group" "target_group" {
      + arn                                = (known after apply)
      + arn_suffix                         = (known after apply)
      + deregistration_delay               = 10
      + id                                 = (known after apply)
      + lambda_multi_value_headers_enabled = false
      + load_balancing_algorithm_type      = (known after apply)
      + name                               = "dev-cognito-service"
      + port                               = 31337
      + preserve_client_ip                 = (known after apply)
      + protocol                           = "HTTP"
      + protocol_version                   = (known after apply)
      + proxy_protocol_v2                  = false
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
    }   """.strip() in output
