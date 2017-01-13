from collections import OrderedDict
from itertools import imap

from utils import cleaned_up_conf, split_on_first_whitespace


class SSHConfFileMixin(object):
    conf_file = None
    conf = {}
    translation_dict = {
        'timers.ssh-based-interface-timer': 'LoginGraceTime',
        'timers.common-interface-timer': 'ClientAliveInterval'
    }

    def translate_data_to_sshd_conf(self, data):
        translated_data = {}
        for key, value in data.iteritems():
            if key in self.translation_dict:
                translated_data.update({
                    self.translation_dict[key]: value
                })

        return translated_data

    def read_conf(self):
        with open(self.conf_file, 'r') as f:
            self.conf = OrderedDict(
                imap(split_on_first_whitespace, cleaned_up_conf(f)))

    def update_conf(self, data):
        data = self.translate_data_to_sshd_conf(data)
        # Add newline to data dict's values
        data.update({k: '{0}\n'.format(v) for k, v in data.iteritems()})

        self.conf.update(data)

    def write_conf(self):
        with open(self.conf_file, 'w') as f:
            for key, value in self.conf.iteritems():
                f.write('{0} {1}'.format(key, value))

    def apply_conf(self, data):
        self.read_conf()

        self.update_conf(data)

        self.write_conf()
