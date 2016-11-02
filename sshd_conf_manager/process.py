import xmlrpclib


class SupervisordMixin(object):
    """
    A Mixin that can be used to manipulate supervisord processes
    """
    process_name = None
    supervisor_server = None

    def __init__(self):
        self.server = xmlrpclib.Server(self.supervisor_server)

    def reload_settings(self, data):
        if self.is_process_up():
            self.server.supervisor.signalProcess(self.process_name, 'HUP')

    def is_process_up(self):
        return self.server.supervisor.getProcessInfo(
                self.process_name).get('pid')
