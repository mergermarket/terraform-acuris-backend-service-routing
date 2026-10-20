import unittest
from subprocess import check_call, check_output

# env -> (simple_dns_name=true record, simple_dns_name=false record)
CASES = {
    'live': ('cognito.awsaccountprod.testbackend.com', 'live-cognito.awsaccountprod.testbackend.com'),
    'live_eu-west-2': ('eu-west-2-cognito.awsaccountprod.testbackend.com', 'live-eu-west-2-cognito.awsaccountprod.testbackend.com'),
    # hyphenated env is not matched by the account-zone regex (^live(_.+)?$), so it resolves to the dev zone
    'live-eu-west-2': ('eu-west-2-cognito.awsaccountdev.testbackend.com', 'live-eu-west-2-cognito.awsaccountdev.testbackend.com'),
    'live_us-east-1': ('us-east-1-cognito.awsaccountprod.testbackend.com', 'live-us-east-1-cognito.awsaccountprod.testbackend.com'),
    'qa': ('qa-cognito.awsaccountdev.testbackend.com', 'qa-cognito.awsaccountdev.testbackend.com'),
}


class TestRoute53Naming(unittest.TestCase):

    def setUp(self):
        check_call(['terraform', 'init', 'test/naming'])

    def record_name(self, env, simple, alias='awsaccount'):
        out = check_output([
            'terraform', 'apply', '-auto-approve', '-no-color',
            '-state=/tmp/naming.tfstate',
            '-var', 'env=%s' % env,
            '-var', 'aws_account_alias=%s' % alias,
            '-var', 'simple_dns_name=%s' % str(simple).lower(),
            'test/naming'
        ]).decode('utf-8')
        return [l.split('=', 1)[1].strip().strip('"') for l in out.splitlines() if l.startswith('record_name =')][0]

    def test_simple_dns_name_true(self):
        for env, (simple, _) in CASES.items():
            with self.subTest(env=env):
                assert self.record_name(env, True) == simple

    def test_simple_dns_name_false(self):
        for env, (_, full) in CASES.items():
            with self.subTest(env=env):
                assert self.record_name(env, False) == full

    def test_simple_dns_name_never_contains_live_prefix(self):
        for env in ['live', 'live_eu-west-2', 'live-eu-west-2']:
            with self.subTest(env=env):
                assert not self.record_name(env, True).startswith('live-')
