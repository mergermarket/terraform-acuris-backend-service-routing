import json
import os
from subprocess import check_call, check_output

import pytest

NAMING_DIR = os.path.join(os.path.dirname(__file__), 'naming')


@pytest.fixture(scope='module', autouse=True)
def init():
    check_call(['terraform', 'init', '-no-color'], cwd=NAMING_DIR)


def names(tmp_path, **tf_vars):
    state = str(tmp_path / 'terraform.tfstate')
    args = []
    for key, value in tf_vars.items():
        if isinstance(value, bool):
            value = str(value).lower()
        args += ['-var', '{}={}'.format(key, value)]

    check_call(
        ['terraform', 'apply', '-auto-approve', '-no-color',
         '-state={}'.format(state)] + args,
        cwd=NAMING_DIR,
    )
    output = json.loads(check_output(
        ['terraform', 'output', '-json', '-state={}'.format(state)],
        cwd=NAMING_DIR,
    ).decode('utf-8'))
    return {key: value['value'] for key, value in output.items()}


@pytest.mark.parametrize('tf_vars, expected', [
    # primary live region
    (
        dict(env='live'),
        dict(
            target_host_name='cognito.domain.com',
            backend_dns_domain='awsaccountprod.testbackend.com',
            dns_record_name='live-cognito.awsaccountprod.testbackend.com',
        ),
    ),
    (
        dict(env='live', simple_dns_name=True),
        dict(
            target_host_name='cognito.domain.com',
            backend_dns_domain='awsaccountprod.testbackend.com',
            dns_record_name='cognito.awsaccountprod.testbackend.com',
        ),
    ),
    (
        dict(env='live', aws_account_alias=''),
        dict(
            target_host_name='cognito.domain.com',
            backend_dns_domain='testbackend.com',
            dns_record_name='cognito.testbackend.com',
        ),
    ),
    (
        dict(env='live', aws_account_alias='', simple_dns_name=True),
        dict(
            target_host_name='cognito.domain.com',
            backend_dns_domain='testbackend.com',
            dns_record_name='cognito.testbackend.com',
        ),
    ),
    # secondary live region - "live" is omitted, leaving the region
    (
        dict(env='live_eu_west_2'),
        dict(
            target_host_name='eu-west-2-cognito.domain.com',
            backend_dns_domain='awsaccountprod.testbackend.com',
            dns_record_name='eu-west-2-cognito.awsaccountprod.testbackend.com',
        ),
    ),
    (
        dict(env='live_eu_west_2', simple_dns_name=True),
        dict(
            target_host_name='eu-west-2-cognito.domain.com',
            backend_dns_domain='awsaccountprod.testbackend.com',
            dns_record_name='eu-west-2-cognito.awsaccountprod.testbackend.com',
        ),
    ),
    (
        dict(env='live_eu_west_2', aws_account_alias=''),
        dict(
            target_host_name='eu-west-2-cognito.domain.com',
            backend_dns_domain='testbackend.com',
            dns_record_name='eu-west-2-cognito.testbackend.com',
        ),
    ),
    (
        dict(env='live_eu_west_2', aws_account_alias='', simple_dns_name=True),
        dict(
            target_host_name='eu-west-2-cognito.domain.com',
            backend_dns_domain='testbackend.com',
            dns_record_name='eu-west-2-cognito.testbackend.com',
        ),
    ),
    (
        dict(env='live_us_east_1', override_dns_name='myservice'),
        dict(
            target_host_name='us-east-1-myservice.domain.com',
            backend_dns_domain='awsaccountprod.testbackend.com',
            dns_record_name='us-east-1-myservice.awsaccountprod.testbackend.com',
        ),
    ),
    # non-live environments
    (
        dict(env='dev'),
        dict(
            target_host_name='dev-cognito.domain.com',
            backend_dns_domain='awsaccountdev.testbackend.com',
            dns_record_name='dev-cognito.awsaccountdev.testbackend.com',
        ),
    ),
    (
        dict(env='dev', simple_dns_name=True),
        dict(
            target_host_name='dev-cognito.domain.com',
            backend_dns_domain='awsaccountdev.testbackend.com',
            dns_record_name='dev-cognito.awsaccountdev.testbackend.com',
        ),
    ),
    (
        dict(env='dev', aws_account_alias=''),
        dict(
            target_host_name='dev-cognito.domain.com',
            backend_dns_domain='dev.testbackend.com',
            dns_record_name='dev-cognito.dev.testbackend.com',
        ),
    ),
    (
        dict(env='ci_test'),
        dict(
            target_host_name='ci-test-cognito.domain.com',
            backend_dns_domain='awsaccountdev.testbackend.com',
            dns_record_name='ci-test-cognito.awsaccountdev.testbackend.com',
        ),
    ),
    # envs merely containing "live" are not treated as live
    (
        dict(env='aslive'),
        dict(
            target_host_name='aslive-cognito.domain.com',
            backend_dns_domain='awsaccountdev.testbackend.com',
            dns_record_name='aslive-cognito.awsaccountdev.testbackend.com',
        ),
    ),
    (
        dict(env='aslive_eu_west_2'),
        dict(
            target_host_name='aslive-eu-west-2-cognito.domain.com',
            backend_dns_domain='awsaccountdev.testbackend.com',
            dns_record_name='aslive-eu-west-2-cognito.awsaccountdev.testbackend.com',
        ),
    ),
    # service name handling
    (
        dict(env='dev', override_dns_name='myservice'),
        dict(
            target_host_name='dev-myservice.domain.com',
            backend_dns_domain='awsaccountdev.testbackend.com',
            dns_record_name='dev-myservice.awsaccountdev.testbackend.com',
        ),
    ),
    (
        dict(env='dev', component_name='cognito'),
        dict(
            target_host_name='dev-cognito.domain.com',
            backend_dns_domain='awsaccountdev.testbackend.com',
            dns_record_name='dev-cognito.awsaccountdev.testbackend.com',
        ),
    ),
    (
        dict(env='dev', component_name='service-router-service'),
        dict(
            target_host_name='dev-service-router.domain.com',
            backend_dns_domain='awsaccountdev.testbackend.com',
            dns_record_name='dev-service-router.awsaccountdev.testbackend.com',
        ),
    ),
])
def test_naming(tmp_path, tf_vars, expected):
    assert names(tmp_path, **tf_vars) == expected
