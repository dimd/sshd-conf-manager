import tempfile
import unittest

from sshd_conf_manager.banner_file import BannerFileMixin


class BannerFileMixinTest(unittest.TestCase):

    def setUp(self):
        self.banner_file_mixin = BannerFileMixin()

    def get_banner_text_test(self):
        test_dict = {'banner-text': 'Test'}

        self.assertEqual(
                self.banner_file_mixin.get_banner_text(test_dict),
                'Test')

    def test_update_banner_file(self):
        temp_file = tempfile.NamedTemporaryFile()
        self.banner_file_mixin.banner_file = temp_file.name

        with temp_file.file as f:

            self.banner_file_mixin.update_banner_file(
                    {'banner-text': 'My banner'})
            self.assertEqual(f.read(), 'My banner')
