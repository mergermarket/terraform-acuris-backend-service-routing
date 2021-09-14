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
            '-var', 'aws_region=eu-west-1',
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
            '-var', 'aws_region=eu-west-1',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_service_routing.aws_alb_listener_rule.rule
      id:                                                   <computed>
      action.#:                                             "1"
      action.0.order:                                       <computed>
      action.0.target_group_arn:                            "${aws_alb_target_group.target_group.arn}"
      action.0.type:                                        "forward"
      arn:                                                  <computed>
      condition.#:                                          "2"
      condition.1322904213.field:                           <computed>
      condition.1322904213.host_header.#:                   <computed>
      condition.1322904213.http_header.#:                   "0"
      condition.1322904213.http_request_method.#:           "0"
      condition.1322904213.path_pattern.#:                  "1"
      condition.1322904213.path_pattern.0.values.#:         "1"
      condition.1322904213.path_pattern.0.values.163128923: "*"
      condition.1322904213.query_string.#:                  "0"
      condition.1322904213.source_ip.#:                     "0"
      condition.1322904213.values.#:                        <computed>
      condition.3843014500.field:                           <computed>
      condition.3843014500.host_header.#:                   "1"
      condition.3843014500.host_header.0.values.#:          "1"
      condition.3843014500.host_header.0.values.3895622771: "dev-cognito.domain.com"
      condition.3843014500.http_header.#:                   "0"
      condition.3843014500.http_request_method.#:           "0"
      condition.3843014500.path_pattern.#:                  <computed>
      condition.3843014500.query_string.#:                  "0"
      condition.3843014500.source_ip.#:                     "0"
      condition.3843014500.values.#:                        <computed>
      listener_arn:                                         "alb:listener"
      priority:                                             "10"
        """.strip() in output

    def test_create_alb_listener_rule_live(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=live',
            '-var', 'aws_region=eu-west-1',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
+ module.backend_service_routing.aws_alb_listener_rule.rule
      id:                                                   <computed>
      action.#:                                             "1"
      action.0.order:                                       <computed>
      action.0.target_group_arn:                            "${aws_alb_target_group.target_group.arn}"
      action.0.type:                                        "forward"
      arn:                                                  <computed>
      condition.#:                                          "2"
      condition.1322904213.field:                           <computed>
      condition.1322904213.host_header.#:                   <computed>
      condition.1322904213.http_header.#:                   "0"
      condition.1322904213.http_request_method.#:           "0"
      condition.1322904213.path_pattern.#:                  "1"
      condition.1322904213.path_pattern.0.values.#:         "1"
      condition.1322904213.path_pattern.0.values.163128923: "*"
      condition.1322904213.query_string.#:                  "0"
      condition.1322904213.source_ip.#:                     "0"
      condition.1322904213.values.#:                        <computed>
      condition.4207679377.field:                           <computed>
      condition.4207679377.host_header.#:                   "1"
      condition.4207679377.host_header.0.values.#:          "1"
      condition.4207679377.host_header.0.values.2369056528: "cognito.domain.com"
      condition.4207679377.http_header.#:                   "0"
      condition.4207679377.http_request_method.#:           "0"
      condition.4207679377.path_pattern.#:                  <computed>
      condition.4207679377.query_string.#:                  "0"
      condition.4207679377.source_ip.#:                     "0"
      condition.4207679377.values.#:                        <computed>
      listener_arn:                                         "alb:listener"
      priority:                                             "10"
        """.strip() in output

    def test_create_aws_alb_target_group(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'env=dev',
            '-var', 'aws_region=eu-west-1',
            '-var', 'aws_account_alias=awsaccount',
            '-var', 'backend_dns=testbackend.com',
            '-var-file=test/platform-config/eu-west-1.json',
            '-target=module.backend_service_routing.aws_alb_listener_rule.rule',
            '-no-color',
            'test/infra'
        ]).decode('utf-8')

        # Then
        assert """
  + module.backend_service_routing.aws_alb_target_group.target_group
      id:                                                   <computed>
      arn:                                                  <computed>
      arn_suffix:                                           <computed>
      deregistration_delay:                                 "10"
      health_check.#:                                       "1"
      health_check.0.enabled:                               "true"
      health_check.0.healthy_threshold:                     "2"
      health_check.0.interval:                              "5"
      health_check.0.matcher:                               "200-299"
      health_check.0.path:                                  "/internal/healthcheck"
      health_check.0.port:                                  "traffic-port"
      health_check.0.protocol:                              "HTTP"
      health_check.0.timeout:                               "4"
      health_check.0.unhealthy_threshold:                   "2"
      lambda_multi_value_headers_enabled:                   "false"
      load_balancing_algorithm_type:                        <computed>
      name:                                                 "dev-cognito-service"
      port:                                                 "31337"
      protocol:                                             "HTTP"
      proxy_protocol_v2:                                    "false"
      slow_start:                                           "0"
      stickiness.#:                                         <computed>
      tags.%:                                               "3"
      tags.component:                                       "cognito-service"
      tags.env:                                             "dev"
      tags.service:                                         "dev-cognito-service"
      target_type:                                          "instance"
      vpc_id:                                               "vpc-12345678"
        """.strip() in output

