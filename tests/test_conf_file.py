import collections
import tempfile
import unittest

import mock

from sshd_conf_manager.conf_file import SSHConfFileMixin


class SSHConfFileMixinTest(unittest.TestCase):

    def setUp(self):
        self.ssh_conf_file_mixin = SSHConfFileMixin()

    def test_read_conf(self):
        temp_file = tempfile.NamedTemporaryFile()

        data = ['#bitter and then some\n',
                '\n',
                ' thaw \n',
                'jane doe\n',
                'Match Group converge\n'
                '  distance and meaning\n']

        with temp_file.file as f:
            for line in data:
                f.write(line)
            f.flush()

            self.ssh_conf_file_mixin.conf_file = temp_file.name
            self.ssh_conf_file_mixin.read_conf()

            self.assertEqual(
                self.ssh_conf_file_mixin.conf.global_settings,
                {'jane': ['doe\n']}
            )
            self.assertEqual(
                list(self.ssh_conf_file_mixin.conf.match_sections),
                ['Match Group converge\n',
                 '  distance and meaning\n']
            )

    def test_update_conf(self):
        data = {'timers.ssh-based-interface-timer': 60,
                'timers.common-interface-timer': 15}

        self.ssh_conf_file_mixin.conf.global_settings = {}

        self.ssh_conf_file_mixin.update_conf(data)

        self.assertDictEqual(
                self.ssh_conf_file_mixin.conf.global_settings,
                {'LoginGraceTime': ['60\n'],
                 'ClientAliveInterval': ['15\n'],
                 'ListenAddress': ['0.0.0.0\n']
                 })

    def test_write_conf(self):
        self.ssh_conf_file_mixin.conf = collections.namedtuple(
            'ssh_config', 'global_settings, match_sections')
        self.ssh_conf_file_mixin.conf.global_settings = {
                'hello': ['goodbye\n'],
                'penny': ['lane\n']
            }
        self.ssh_conf_file_mixin.conf.match_sections = ['1\n', 'a\n']

        temp_file = tempfile.NamedTemporaryFile()
        self.ssh_conf_file_mixin.conf_file = temp_file.name

        with temp_file.file as f:
            self.ssh_conf_file_mixin.write_conf()
            self.assertItemsEqual(
                f.readlines(),
                ['hello goodbye\n', 'penny lane\n', '1\n', 'a\n']
            )

    @mock.patch.multiple('sshd_conf_manager.conf_file.SSHConfFileMixin',
                         read_conf=mock.DEFAULT,
                         write_conf=mock.DEFAULT,
                         update_conf=mock.DEFAULT)
    def test_apply_conf(self,
                        read_conf, write_conf, update_conf):
        self.ssh_conf_file_mixin.apply_conf('dummy_data')

        read_conf.assert_called_once()
        update_conf.assert_called_once_with('dummy_data')
        write_conf.assert_called_once()
