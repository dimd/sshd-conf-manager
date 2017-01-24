from collections import defaultdict, namedtuple
from itertools import dropwhile, takewhile

from utils import (get_listen_address,
                   get_sshd_conf,
                   not_match_section,
                   split_on_first_whitespace)


class SSHConfFileMixin(object):
    '''
    Mixin that handles the sshd_config update from cm

    The apply_conf method can be used as a callback when cm db data are
    received
    '''

    listening_interface = ''
    conf_file = None
    conf = namedtuple('sshd_config', 'global_settings, match_sections')

    # https://confluence.int.net.nokia.com/display/VTAS/UTAS+17+UM+-+Requirements#UTAS17UM-Requirements-FN02078.FC014020.38ConfigurationofUMtimers
    translation_dict = {
        'timers.ssh-based-interface-timer': 'LoginGraceTime',
        'timers.common-interface-timer': 'ClientAliveInterval'
    }

    def _translate_data_to_sshd_conf(self, data):
        '''
        Data from cm need to be translated to sshd config parameters

        This function applies the translation dict to data dict
        '''
        translated_data = {}
        for key, value in data.iteritems():
            if key in self.translation_dict:
                translated_data.update({
                    self.translation_dict[key]: value
                })

        return translated_data

    def read_conf(self):
        self.conf.global_settings = defaultdict(list)

        with open(self.conf_file, 'r') as f:
            sshd_config_raw = get_sshd_conf(list(f))

        global_settings = takewhile(
                not_match_section,
                sshd_config_raw
            )

        for k, v in map(split_on_first_whitespace,
                        global_settings):
            self.conf.global_settings[k].append(v)

        self.conf.match_sections = dropwhile(
                not_match_section,
                sshd_config_raw
            )

    def update_conf(self, data):
        data = self._translate_data_to_sshd_conf(data)

        data.update({
            'ListenAddress': get_listen_address(self.listening_interface)
        })

        # Add newline to data dict's values
        data.update({k: ['{0}\n'.format(v)] for k, v in data.iteritems()})

        self.conf.global_settings.update(data)

    def write_conf(self):
        with open(self.conf_file, 'w') as f:
            for key, values in self.conf.global_settings.iteritems():
                for value in values:
                    f.write('{0} {1}'.format(key, value))

            for line in self.conf.match_sections:
                f.write(line)

    def apply_conf(self, data):
        self.read_conf()

        self.update_conf(data)

        self.write_conf()
