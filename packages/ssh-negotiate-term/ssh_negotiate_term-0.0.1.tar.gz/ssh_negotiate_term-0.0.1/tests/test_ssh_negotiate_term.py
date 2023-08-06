import configparser
import unittest

from ssh_negotiate_term import SSHNegotiateTerm


class TestSSHNegotiateTerm(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config['patterns'] = SSHNegotiateTerm.DEFAULT_PATTERNS
        config['ssh'] = {}
        config['ssh']['path'] = SSHNegotiateTerm.DEFAULT_SSH
        config['translations'] = SSHNegotiateTerm.DEFAULT_TRANSLATIONS
        self.snt_config = config

    def test_instantiate(self):
        snt = SSHNegotiateTerm('foo', [], self.snt_config)
        self.assertIsInstance(snt, SSHNegotiateTerm)

    def test_hostname(self):
        snt = SSHNegotiateTerm(
            'screen-256color', ['ssh', 'examplehost'], self.snt_config)
        self.assertEqual(snt.term, 'screen-256color')

    def test_fqdn(self):
        snt = SSHNegotiateTerm(
            'screen-256color', ['ssh', 'host.example.net.'], self.snt_config)
        self.assertEqual(snt.term, 'screen-256color')

    def test_ipv4(self):
        snt = SSHNegotiateTerm(
            'screen-256color', ['ssh', '192.0.2.1'], self.snt_config)
        self.assertEqual(snt.term, 'screen')

    def test_ipv6(self):
        snt = SSHNegotiateTerm(
            'screen-256color', ['ssh', '2001:0db8::1'], self.snt_config)
        self.assertEqual(snt.term, 'screen')

    def test_complex_command_line(self):
        snt = SSHNegotiateTerm('screen-256color',
                               ['ssh',
                                '-4',
                                '-NfoSetEnv=FOO=BAR',
                                '-NtT',
                                '--',
                                '192.0.2.1',
                                'runcmd'],
                               self.snt_config)
        self.assertEqual(snt.term, 'screen')
        snt = SSHNegotiateTerm('screen-256color',
                               ['ssh',
                                '-4',
                                '-NfoSetEnv=FOO=BAR',
                                '-NtT',
                                '--',
                                'examplehost',
                                'runcmd'],
                               self.snt_config)
        self.assertEqual(snt.term, 'screen-256color')

    def test_null_term(self):
        snt = SSHNegotiateTerm(None, ['ssh', '192.0.2.1'], self.snt_config)
        self.assertEqual(snt.term, None)

    def test_unknown_term(self):
        snt = SSHNegotiateTerm(
            'qwyjibo', [
                'ssh', '192.0.2.1'], self.snt_config)
        self.assertEqual(snt.term, 'qwyjibo')

    def test_untranslated_term(self):
        snt = SSHNegotiateTerm('screen', ['ssh', '192.0.2.1'], self.snt_config)
        self.assertEqual(snt.term, 'screen')

    def test_patterns_simple(self):
        self.snt_config['patterns']['examplehost'] = '^examplehost$'
        snt = SSHNegotiateTerm(
            'screen-256color', ['ssh', 'examplehost'], self.snt_config)
        self.assertEqual(snt.term, 'screen')
        snt = SSHNegotiateTerm(
            'screen-256color', ['ssh', 'examplehost2'], self.snt_config)
        self.assertEqual(snt.term, 'screen-256color')

    def test_pattern_complex(self):
        self.snt_config['patterns']['complexhost'] = '^[a-z]{3}-[a-z]{2,}-[a-z]{2,}-[0-9]'
        snt = SSHNegotiateTerm(
            'screen-256color', ['ssh', 'abc-example-ar-1'], self.snt_config)
        self.assertEqual(snt.term, 'screen')
        snt = SSHNegotiateTerm(
            'screen-256color', ['ssh', 'abc-example-ar-a1'], self.snt_config)
        self.assertEqual(snt.term, 'screen-256color')

    def test_translations(self):
        for outer in self.snt_config['translations']:
            snt = SSHNegotiateTerm(
                outer, ['ssh', '192.0.2.1'], self.snt_config)
            inner = self.snt_config['translations'][outer]
            self.assertEqual(snt.term, inner)


if __name__ == '__main__':
    unittest.main()
