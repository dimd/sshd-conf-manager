class BannerFileMixin(object):
    banner_file = None

    def get_banner_text(self, data):
        for k, v in data.iteritems():
            if k == 'banner-text':
                return v

    def update_banner_file(self, data):
        with open(self.banner_file, 'w') as f:
            f.write(self.get_banner_text(data))
