import fcntl
import re
import socket
import struct

from collections import defaultdict, OrderedDict


def get_listen_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    except IOError:
        return '0.0.0.0'


def not_match_section(line):
    return not line.startswith('Match')


def split_on_first_whitespace(line):
    return line.split(None, 1)


def get_sshd_conf(iterable):
    no_comments_and_empty_lines = re.compile(r'[ \t]*[\w/\.]+(?:\s+)[\w/\.]+')
    return filter(
            no_comments_and_empty_lines.match,
            iterable)


class OrderedDefaultDict(OrderedDict, defaultdict):
    # http://stackoverflow.com/a/35968897/7515745
    def __init__(self, default_factory=None, *args, **kwargs):
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory
