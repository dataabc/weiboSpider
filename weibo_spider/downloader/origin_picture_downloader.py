from .img_downloader import ImgDownloader


class OriginPictureDownloader(ImgDownloader):
    def __init__(self, file_dir, file_download_timeout):
        super().__init__(file_dir, file_download_timeout)
        self.describe = u'原创微博图片'
        self.key = 'original_pictures'
