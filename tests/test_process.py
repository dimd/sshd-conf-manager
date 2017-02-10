import mock
import unittest

from sshd_conf_manager.process import SupervisordMixin


@mock.patch('sshd_conf_manager.process.xmlrpclib', auto_spec=True)
class ProcessMixinTest(unittest.TestCase):
    def test_initialization(self, xmlrpclib_mock):
        SupervisordMixin()

        xmlrpclib_mock.Server.assert_called_with(None)

    def test_reload_settings(self, xmlrpclib_mock):
        supervisord_mixin = SupervisordMixin()
        supervisor_mock = supervisord_mixin.server.supervisor
        supervisor_mock.getProcessInfo.return_value.get.return_value = True

        supervisord_mixin.process_name = 'test_process'

        supervisord_mixin.reload_settings(None)

        supervisord_mixin.server.supervisor.signalProcess.assert_called_with(
                'test_process',
                'HUP')

    def test_reload_settings_start_process(self, xmlrpclib_mock):
        supervisord_mixin = SupervisordMixin()
        supervisor_mock = supervisord_mixin.server.supervisor
        supervisor_mock.getProcessInfo.return_value.get.return_value = False

        supervisord_mixin.process_name = 'test_process'

        supervisord_mixin.reload_settings(None)

        supervisord_mixin.server.supervisor.startProcess.assert_called_with(
                'test_process')

    def test_is_process_up(self, xmlrpclib_mock):
        supervisord_mixin = SupervisordMixin()
        supervisord_mixin.process_name = 'test_process'

        supervisord_mixin.is_process_up()

        supervisor_mock = supervisord_mixin.server.supervisor
        supervisor_mock.getProcessInfo.assert_called_with('test_process')
        supervisor_mock.getProcessInfo.return_value.get.assert_called_with(
                'pid')
