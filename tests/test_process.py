import mock
import supervisor.rpcinterface
import unittest
import xmlrpclib

from conf_manager.process import SupervisordMixin


@mock.patch('conf_manager.process.supervisor.xmlrpc', auto_spec=True)
@mock.patch('conf_manager.process.xmlrpclib', auto_spec=True)
class ProcessMixiTest(unittest.TestCase):
    def test_initialization(self, xmlrpclib_mock, supervisor_xmlrpc_mock):
        supervisor_xmlrpc_mock.SupervisorTransport.return_value = (
            mock.sentinel.supervisor_transport)
        SupervisordMixin()

        supervisor_xmlrpc_mock.SupervisorTransport.assert_called_with(
                username=None,
                password=None,
                serverurl='unix://None')
        xmlrpclib_mock.ServerProxy.assert_called_with(
                'http://localhost',
                transport=mock.sentinel.supervisor_transport)

    def test_reload_settings(self, xmlrpclib_mock, supervisor_xmlrpc_mock):
        xmlrpclib_mock.ServerProxy.return_value = mock.Mock(
                spec=xmlrpclib.ServerProxy,
                auto_spec=True)
        xmlrpclib_mock.ServerProxy.return_value.supervisor = mock.Mock(
                spec=supervisor.rpcinterface.SupervisorNamespaceRPCInterface,
                auto_spec=True)

        supervisord_mixin = SupervisordMixin()
        supervisor_mock = supervisord_mixin.server.supervisor
        supervisor_mock.getProcessInfo.return_value.get.return_value = True

        supervisord_mixin.process_name = 'test_process'

        supervisord_mixin.reload_settings(None)

        supervisord_mixin.server.supervisor.signalProcess.assert_called_with(
                'test_process',
                'HUP')

    def test_is_process_up(self, xmlrpclib_mock, supervisor_xmlrpc_mock):
        supervisord_mixin = SupervisordMixin()
        supervisord_mixin.process_name = 'test_process'

        supervisord_mixin.is_process_up()

        supervisor_mock = supervisord_mixin.server.supervisor
        supervisor_mock.getProcessInfo.assert_called_with('test_process')
        supervisor_mock.getProcessInfo.return_value.get.assert_called_with(
                'pid')
