import os

from .img_downloader import ImgDownloader


class AvatarPictureDownloader(ImgDownloader):
    def __init__(self, file_dir, file_download_timeout):
        super().__init__(file_dir, file_download_timeout)
        self.describe = u'头像图片'
        self.key = 'avatar_pictures'

    def handle_download(self, urls):
        """处理下载相关操作"""
        file_dir = self.file_dir + os.sep + self.describe
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)

        for i, url in enumerate(urls):
            index = url.rfind('/')
            file_name = url[index:]
            file_path = file_dir + os.sep + file_name
            self.download_one_file(url, file_path, 'xxx')