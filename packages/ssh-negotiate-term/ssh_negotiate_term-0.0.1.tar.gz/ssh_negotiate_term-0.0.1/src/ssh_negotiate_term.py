"""
Wrap ssh(1) commands, parse the options, and check whether the hostname
argument is either an IPv4/IPv6 address or matches any of a set of configured
hostname patterns.  If so, and we're using a TERM type that's not
well-supported on network gear, set a more broadly-compatible TERM type.
"""
import argparse
import configparser
import ipaddress
import os
import re
import sys


class SSHArgumentParserError(Exception):
    """
    Exception for SSHArgumentParser to throw on error.
    """


class SSHArgumentParser(argparse.ArgumentParser):
    """
    Subclass argparse.ArgumentParser just so that errors raise exceptions
    rather than exiting.
    """

    def error(self, message):
        raise SSHArgumentParserError(message)


class SSHNegotiateTerm():
    """
    Using a class, to encapsulate a fair bit of system state that gets injected
    into this.
    """

    # Configuration file path; this gets expanded with os.path.expanduser()
    CONFIG_PATH = '~/.config/ssh_negotiate_term/config'

    # Defaults to set to which a config file replaces/appends
    DEFAULT_PATTERNS = {}
    DEFAULT_SSH = '/usr/bin/ssh'
    DEFAULT_TRANSLATIONS = {
        'putty-256color': 'xterm',
        'screen-256color': 'screen',
        'tmux': 'screen',
        'rxvt-256color': 'rxvt',
        'tmux-256color': 'screen',
        'xterm-256color': 'xterm',
    }

    def __init__(self, term, argv, config=None):

        # Read config file if we weren't passed an already-complete config
        if not config:
            config = configparser.ConfigParser()
            config['patterns'] = self.DEFAULT_PATTERNS
            config['ssh'] = {}
            config['ssh']['path'] = self.DEFAULT_SSH
            config['translations'] = self.DEFAULT_TRANSLATIONS
            config.read(os.path.expanduser(self.CONFIG_PATH))
        self.config = config

        # Replace the first argument (this script) with the real SSH
        ssh = self.config['ssh']['path']
        self.argv = [ssh] + argv[1:]

        # Translate the terminal if a downgrade is required, otherwise take it
        # as provided
        if self.downgrade_required(term):
            self.term = self.config['translations'][term]
        else:
            self.term = term

    # Flags from `man ssh` so we can attempt to parse the command line
    # OpenSSH_9.2p1 Debian-2, OpenSSL 3.0.9 30 May 2023
    SSH_OPTIONS_SWITCHES = list('46AaCfGgKkMNnqsTtVvXxYy')
    SSH_OPTIONS_ARGUMENTS = list('BbcDEeFIiJLlmOopQRSWw')

    def downgrade_required(self, term):
        """
        Given a TERM terminal name, having already set self.config and
        self.argv in the constructor, decide whether it's appropriate to
        downgrade the TERM string before calling SSH.
        """
        # TERM wasn't set at all; do nothing
        if not term:
            return False
        # TERM was set, but there's no translation configured for it; do
        # nothing
        if term not in self.config['translations']:
            return False

        # Parse the SSH command line to try and get the hostname
        parser = SSHArgumentParser()
        for letter in self.SSH_OPTIONS_SWITCHES:
            parser.add_argument('-' + letter, action='store_true')
        for letter in self.SSH_OPTIONS_ARGUMENTS:
            parser.add_argument('-' + letter)
        parser.add_argument('hostname')
        parser.add_argument('command', nargs='*')
        # Don't exit if we can't get the hostname, as ArgumentParser does by
        # default; instead, just give up on the idea of downgrading
        try:
            args = parser.parse_args(self.argv[1:])
            hostname = args.hostname
        except SSHArgumentParserError:
            return False

        # If the hostname looks like an IPv4 or IPv6 address, we'll downgrade
        try:
            ipaddress.ip_address(hostname)
            return True
        except ValueError:
            pass

        # If the hostname looks like one of the configured patterns, we'll
        # downgrade
        for pattern in self.config['patterns']:
            if re.search(self.config['patterns'][pattern], hostname):
                return True

        # We *could* downgrade, but the hostname doesn't look like something we
        # need to downgrade for, so don't
        return False

    def exec(self):
        """
        Convenience function to exec the real ssh(1) program with what we
        decided in the object's constructor.
        """
        os.environ['TERM'] = self.term
        os.execv(self.argv[0], self.argv)

def main():
    """
    Entry point for the command line client.
    """
    snt = SSHNegotiateTerm(os.environ['TERM'], sys.argv)
    snt.exec()

# If called from the command line, create the object with the real terminal and
# arguments to this script, and execute them as it concludes appropriate; the
# separation here is just to make the object testable
if __name__ == '__main__':
    main()
