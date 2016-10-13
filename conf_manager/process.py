import xmlrpclib


class SupervisordMixin(object):
    """
    A Mixin that can be used to manipulate supervisord processes
    """
    process_name = None
    supervisor_xmlrpc_username = None
    supervisor_xmlrpc_password = None
    supervisor_xmlrpc_unix_socket = None

    def __init__(self):
        self.server = xmlrpclib.Server('http://localhost:9001/RPC2')

    def reload_settings(self, data):
        if self.is_process_up():
            self.server.supervisor.signalProcess(self.process_name, 'HUP')

    def is_process_up(self):
        return self.server.supervisor.getProcessInfo(
                self.process_name).get('pid')
