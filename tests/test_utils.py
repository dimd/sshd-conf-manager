import unittest
from sshd_conf_manager import utils


class UtilsTest(unittest.TestCase):

    def test_split_line_on_first_whitespace(self):
        test_line = 'This is a trick'
        result = utils.split_on_first_whitespace(test_line)

        self.assertListEqual(result, ['This', 'is a trick'])

    def test_get_sshd_conf(self):
        test_iterable = [
                '#Comment will be removed',
                '\n',
                '   \n',
                '   #Hey',
                ' I am in',
                'I will stay']

        self.assertItemsEqual(
                list(utils.get_sshd_conf(test_iterable)),
                [' I am in', 'I will stay'])
