Description
===========

[![Test](https://github.com/mergermarket/terraform-acuris-backend-service-routing/actions/workflows/test.yml/badge.svg)](https://github.com/mergermarket/terraform-acuris-backend-service-routing/actions/workflows/test.yml)

This module creates the DNS and routing rule for a backend service. It's an opinionated module that forms the DNS name from the `env` (environment name), `name` (short name for the service - typically with the "-service" suffix removed) and `domain`.

For the live environment this will be:

```plain
    name.domain
```

For the non-live environments this will be:

```plain
    env-name.domain
```

This is intended for use in a backend router component e.g. one using <https://github.com/mergermarket/terraform-acuris-backend-router>.

Usage
-----

Add this to the bottom of the `infra/main.tf` file in your backend router for each service:

```hcl
module "cognito_service" {
    source  = "mergermarket/backend-service-routing/acuris"
    version = "0.0.2"

    env              = var.env
    component_name   = "cognito-service"
    dns_domain       = var.dns_domain
    priority         = "10"
    alb_listener_arn = module.backend_router.alb_listener_arn
    alb_dns_name     = module.backend_router.alb_dns_name
    vpc_id           = var.platform_config["vpc"]
    aws_account_alias = var.aws_account_alias
    backend_dns      = var.backend_dns
}
```

Then put the ARN for the target group of your service in each environment into `config/qa.json`, `config/aslive.json`, ...:

```json
    {
        "target_groups": {
            "notifications-profile-matching-service": "arn:of:the:qa:notifications-profile-matching-service:target:group"
        }
    }
```

### Overriding DNS Names

If you need to customize the DNS name (for example, to use a different name than the component name), you can use the `override_dns_name` variable:

```hcl
module "cognito_service" {
    source  = "mergermarket/backend-service-routing/acuris"
    version = "0.0.2"

    env              = var.env
    component_name   = "cognito-service"
    override_dns_name = "custom-name"  # Will use this instead of "cognito" in DNS
    dns_domain       = var.dns_domain
    priority         = "10"
    alb_listener_arn = module.backend_router.alb_listener_arn
    alb_dns_name     = module.backend_router.alb_dns_name
    vpc_id           = var.platform_config["vpc"]
    aws_account_alias = var.aws_account_alias
    backend_dns      = var.backend_dns
}
```

This will be used consistently for both the ALB listener host header and the Route53 DNS record.

### Regional live environments and `simple_dns_name`

Secondary live regions (`live_<region>`, e.g. `live_eu_west_2`) drop the `live` part from both the ALB host header and the Route53 record, leaving the region. Underscores become hyphens.

`simple_dns_name = true` removes the remaining `live-` prefix from the Route53 record of the primary `live` environment. The ALB host header and Route53 record always use the same name for regional envs.

Examples for component `cognito-service` (`aws_account_alias = "acme"`, `backend_dns = "example.com"`):

| `env`            | ALB host (`dns_domain`) | Route53 record, `simple_dns_name = false` | Route53 record, `simple_dns_name = true` |
|------------------|-------------------------|-------------------------------------------|------------------------------------------|
| `live`           | `cognito`               | `live-cognito.acmeprod.example.com`       | `cognito.acmeprod.example.com`           |
| `live_eu_west_2` | `eu-west-2-cognito`     | `eu-west-2-cognito.acmeprod.example.com`  | `eu-west-2-cognito.acmeprod.example.com` |
| `qa`             | `qa-cognito`            | `qa-cognito.acmedev.example.com`          | `qa-cognito.acmedev.example.com`         |

Notes:

- With `env = "live"` and an empty `aws_account_alias`, both modes give `cognito.<backend_dns>`.
- Only `live` and `live_<suffix>` (underscore) are treated as live; they select the `<alias>prod.` zone. A hyphenated env such as `live-eu-west-2` is not treated as live.
- The ALB host uses `dns_domain` while the record lives under `backend_dns`.

Testing
-------

Tests run in Docker with `test/run.sh`. `test/test_naming.py` covers the host and Route53 naming rules (`modules/naming`) without calling AWS.

Architecture
------------

This module is the `backend-service-routing` box in the diagram below:

![Architecture diagram](./docs/backend-routing.png)
