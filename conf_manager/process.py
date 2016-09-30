import xmlrpclib
import supervisor.xmlrpc


class SupervisordMixin(object):
    """
    A Mixin that can be used to manipulate supervisord processes
    """
    process_name = None
    supervisor_xmlrpc_username = None
    supervisor_xmlrpc_password = None
    supervisor_xmlrpc_unix_socket = None

    def __init__(self):
        supervisor_transport = supervisor.xmlrpc.SupervisorTransport(
                    username=self.supervisor_xmlrpc_username,
                    password=self.supervisor_xmlrpc_password,
                    serverurl='unix://{}'.format(
                        self.supervisor_xmlrpc_unix_socket)
                    )
        self.server = xmlrpclib.ServerProxy('http://localhost',
                                            transport=supervisor_transport)

    def reload_settings(self, data):
        if self.is_process_up():
            self.server.supervisor.signalProcess(self.process_name, 'HUP')

    def is_process_up(self):
        return self.server.supervisor.getProcessInfo(
                self.process_name).get('pid')
