import mock
import unittest

from conf_manager import sshd_conf as sshd_conf_lib


class SshdConfTest(unittest.TestCase):

    def test_SshdConf_initialization(self):
        sshd_conf = sshd_conf_lib.SshdConf({
                '--redis-host': 'host',
                '--redis-port': '1',
                '--redis-section': 'asection',
                '--sshd-conf-file': 'sshd',
                '--process-name': 'sshd',
                '--supervisor-username': 'dummy',
                '--supervisor-password': 'dummy',
                '--supervisor-socket': 'path'
            })

        self.assertEqual(sshd_conf.redis_host, 'host')
        self.assertEqual(sshd_conf.redis_port, '1')
        self.assertEqual(sshd_conf.redis_section, 'asection')
        self.assertEqual(sshd_conf.conf_file, 'sshd')
        self.assertEqual(sshd_conf.process_name, 'sshd')
        self.assertEqual(sshd_conf.supervisor_xmlrpc_username, 'dummy')
        self.assertEqual(sshd_conf.supervisor_xmlrpc_password, 'dummy')
        self.assertEqual(sshd_conf.supervisor_xmlrpc_unix_socket, 'path')
        self.assertListEqual(
                sshd_conf.redis_callbacks,
                [sshd_conf.apply_conf,
                 sshd_conf.reload_settings]
                )

    @mock.patch('conf_manager.sshd_conf.SshdConf', auto_spec=True)
    @mock.patch('conf_manager.sshd_conf.docopt', auto_spec=True)
    def test_main(self, docopt_mock, sshd_conf_mock):
        sshd_conf_lib.main()

        docopt_mock.assert_called_with(sshd_conf_lib.__doc__)
        sshd_conf_mock.assert_called_with(docopt_mock())
        sshd_conf_mock.return_value.start.assert_called()
