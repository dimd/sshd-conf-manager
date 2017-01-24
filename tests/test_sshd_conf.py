import mock
import unittest

from sshd_conf_manager import sshd_conf as sshd_conf_lib, __version__


class SshdConfTest(unittest.TestCase):

    @mock.patch('sshd_conf_manager.process.xmlrpclib', auto_spec=True)
    def test_SshdConf_initialization(self, xmlrpclib_mock):
        sshd_conf = sshd_conf_lib.SshdConf({
                '--redis-host': 'host',
                '--redis-port': '1',
                '--redis-section': 'asection',
                '--sshd-conf-file': 'sshd',
                '--process-name': 'sshd',
                '--supervisor-server': 'localhost'
            })

        self.assertEqual(sshd_conf.redis_host, 'host')
        self.assertEqual(sshd_conf.redis_port, '1')
        self.assertEqual(sshd_conf.redis_section, 'asection')
        self.assertEqual(sshd_conf.conf_file, 'sshd')
        self.assertEqual(sshd_conf.process_name, 'sshd')
        self.assertListEqual(
                sshd_conf.redis_callbacks,
                [sshd_conf.update_banner_file,
                 sshd_conf.apply_conf,
                 sshd_conf.reload_settings]
                )

    @mock.patch('sshd_conf_manager.sshd_conf.SshdConf', auto_spec=True)
    @mock.patch('sshd_conf_manager.sshd_conf.docopt', auto_spec=True)
    def test_main(self, docopt_mock, sshd_conf_mock):
        sshd_conf_lib.main()

        docopt_mock.assert_called_with(sshd_conf_lib.__doc__,
                                       version=__version__)
        sshd_conf_mock.assert_called_with(docopt_mock())
        sshd_conf_mock.return_value.start.assert_called()
