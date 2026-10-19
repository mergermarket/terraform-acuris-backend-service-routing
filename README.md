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

### Simple Route53 DNS Names

By default the Route53 record is prefixed with the environment, so a regional live environment such as `live_eu-west-2` gets `live-eu-west-2-name`. Set `simple_dns_name = true` to drop the `live-` part and keep only the region:

```hcl
module "cognito_service" {
    source  = "mergermarket/backend-service-routing/acuris"
    version = "0.0.2"

    env               = var.env  # e.g. "live_eu-west-2"
    component_name    = "cognito-service"
    simple_dns_name   = true
    # ... other variables as above
}
```

Resulting Route53 record name for component `cognito-service` (with `aws_account_alias = "acme"`, `backend_dns = "example.com"`):

| `env`            | `simple_dns_name = false`                          | `simple_dns_name = true`                     |
|------------------|----------------------------------------------------|----------------------------------------------|
| `live`           | `live-cognito.acmeprod.example.com`                | `cognito.acmeprod.example.com`               |
| `live_eu-west-2` | `live-eu-west-2-cognito.acmeprod.example.com`      | `eu-west-2-cognito.acmeprod.example.com`     |
| `live-eu-west-2` | `live-eu-west-2-cognito.acmedev.example.com`       | `eu-west-2-cognito.acmedev.example.com`      |
| `qa`             | `qa-cognito.acmedev.example.com`                   | `qa-cognito.acmedev.example.com`             |

Notes:

- With `env = "live"` and an empty `aws_account_alias`, both modes give `cognito.<backend_dns>`.
- Only `live` and `live_<suffix>` (underscore) select the `<alias>prod.` zone; a hyphenated `live-<suffix>` env resolves to `<alias>dev.`.
- `simple_dns_name` only affects the Route53 record. The ALB listener host-header rule still uses the environment prefix (e.g. `live-eu-west-2-cognito.<dns_domain>`), so add the Route53 name to `extra_listener_host_names` if clients will call the service by it.

Testing
-------

Tests run in Docker with `test/run.sh`. `test/test_naming.py` covers the Route53 naming rules (`modules/route53_name`) without calling AWS.

Architecture
------------

This module is the `backend-service-routing` box in the diagram below:

![Architecture diagram](./docs/backend-routing.png)
