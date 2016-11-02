"""SSH Daemon Configuration Manager

Usage:
    sshd-conf-manager [--redis-host <redis_host>]
                      [--redis-port <redis_port>]
                      [--redis-section <redis_section]
                      [--sshd-conf-file <sshd_conf_file>]
                      [--process-name <process_name>]
                      [--supervisor-server <server_url>]

    sshd-conf-manager (-h | --help)

Options:
    --redis-host <redis_host>          Redis hostname/ip [default: 127.0.0.1]
    --redis-port <redis_port>          Redis port [default: 6379]
    --redis-section <redis_section>    Redis section to subscribe for events [default: sshd]
    --sshd-conf-file <sshd_conf_file>  Path to the sshd configuration file [default: /etc/ssh/sshd_config]
    --process-name <process_name>      Supervisord process name of the sshd instance running [default: sshd]
    --supervisor-server <server_url>   Supervisord server url [default: http://localhost:9001/RPC2]
    -h, --help                         Show this
"""

import logging.config
import sys
import yaml
from docopt import docopt

from redis_subscriber import RedisSubscriber
from conf_file import SSHConfFileMixin
from process import SupervisordMixin


class SshdConf(SupervisordMixin, SSHConfFileMixin, RedisSubscriber):

    def __init__(self, arguments):
        self.redis_host = arguments.get('--redis-host')
        self.redis_port = arguments.get('--redis-port')
        self.redis_section = arguments.get('--redis-section')
        self.conf_file = arguments.get('--sshd-conf-file')
        self.process_name = arguments.get('--process-name')
        self.supervisor_server = arguments.get('--supervisor-server')

        self.redis_callbacks.extend([
                self.apply_conf,
                self.reload_settings
        ])

        with open('/'.join([sys.prefix, 'conf', 'logging_config.yaml'])) as f:
            logging.config.dictConfig(yaml.load(f))

        super(SshdConf, self).__init__()


def main():
    SshdConf(docopt(__doc__)).start()
