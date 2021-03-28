import os

from .img_downloader import ImgDownloader


class RetweetPictureDownloader(ImgDownloader):
    def __init__(self, file_dir, file_download_timeout):
        super().__init__(file_dir, file_download_timeout)
        self.key = 'retweet_pictures'
