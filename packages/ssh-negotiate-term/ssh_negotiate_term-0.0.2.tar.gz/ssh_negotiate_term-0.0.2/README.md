ssh\_negotiate\_term
====================

Wrap ssh(1) commands, parse the options, and check whether the hostname
argument is either an IPv4/IPv6 address or matches any of a set of configured
hostname patterns.  If so, and we're using a TERM type that's not
well-supported on network gear, set a more broadly-compatible TERM type.
