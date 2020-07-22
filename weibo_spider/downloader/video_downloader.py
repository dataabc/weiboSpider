import os

from .downloader import Downloader


class VideoDownloader(Downloader):
    def __init__(self, file_dir):
        self.file_dir = file_dir
        self.describe = u'视频'
        self.key = 'video_url'

    def handle_download(self, urls, w):
        """处理下载相关操作"""
        file_prefix = w.publish_time[:11].replace('-', '') + '_' + w.id
        file_suffix = '.mp4'
        file_name = file_prefix + file_suffix
        file_path = self.file_dir + os.sep + file_name
        self.download_one_file(urls, file_path, w.id)
