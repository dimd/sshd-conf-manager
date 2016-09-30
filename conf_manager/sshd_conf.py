"""SSH Daemon Configuration Manager

Usage:
    sshd-conf-manager [--redis-host <redis_host>]
                      [--redis-port <redis_port>]
                      [--redis-section <redis_section]
                      [--sshd-conf-file <sshd_conf_file>]
                      [--process-name <process_name>]
                      [--supervisor-username <supervisor_username>]
                      [--supervisor-password <supervisor_password>]
                      [--supervisor-socket <supervisor_socket>]

    sshd-conf-manager (-h | --help)

Options:
    --redis-host <redis_host>                    Redis hostname/ip [default: 127.0.0.1]
    --redis-port <redis_port>                    Redis port [default: 6379]
    --redis-section <redis_section>              Redis section to subscribe for events [default: sshd]
    --sshd-conf-file <sshd_conf_file>            Path to the sshd configuration file [default: /etc/ssh/sshd_config]
    --process-name <process_name>                Supervisord process name of the sshd instance running [default: sshd]
    --supervisor-username <supervisor_username>  Supervisor xmlrpc service username [default: dummy]
    --supervisor-password <supervisor_password>  Supervisor xmlrpc service password [default: dummy]
    --supervisor-socket <supervisor_socket>      Supervisor xmlrpc service socket [default: /var/run/supervisor/supervisor.sock]
    -h, --help                                   Show this
"""

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
        self.supervisor_xmlrpc_username = arguments.get(
                '--supervisor-username')
        self.supervisor_xmlrpc_password = arguments.get(
                '--supervisor-password')
        self.supervisor_xmlrpc_unix_socket = arguments.get(
                '--supervisor-socket')

        self.redis_callbacks.extend([
                self.apply_conf,
                self.reload_settings
        ])

        super(SshdConf, self).__init__()


def main():
    SshdConf(docopt(__doc__)).start()
