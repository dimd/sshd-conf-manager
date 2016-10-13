import mock
import unittest

from conf_manager.process import SupervisordMixin


@mock.patch('conf_manager.process.xmlrpclib', auto_spec=True)
class ProcessMixiTest(unittest.TestCase):
    def test_initialization(self, xmlrpclib_mock):
        SupervisordMixin()

        xmlrpclib_mock.Server.assert_called_with('http://localhost:9001/RPC2')

    def test_reload_settings(self, xmlrpclib_mock):
        supervisord_mixin = SupervisordMixin()
        supervisor_mock = supervisord_mixin.server.supervisor
        supervisor_mock.getProcessInfo.return_value.get.return_value = True

        supervisord_mixin.process_name = 'test_process'

        supervisord_mixin.reload_settings(None)

        supervisord_mixin.server.supervisor.signalProcess.assert_called_with(
                'test_process',
                'HUP')

    def test_is_process_up(self, xmlrpclib_mock):
        supervisord_mixin = SupervisordMixin()
        supervisord_mixin.process_name = 'test_process'

        supervisord_mixin.is_process_up()

        supervisor_mock = supervisord_mixin.server.supervisor
        supervisor_mock.getProcessInfo.assert_called_with('test_process')
        supervisor_mock.getProcessInfo.return_value.get.assert_called_with(
                'pid')
