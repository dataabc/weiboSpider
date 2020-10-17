import json
import logging
import re
import sys
from datetime import datetime, timedelta

import requests

from .. import datetime_util
from ..weibo import Weibo
from .comment_parser import CommentParser
from .mblog_picAll_parser import MblogPicAllParser
from .parser import Parser
from .util import handle_garbled, handle_html

logger = logging.getLogger('spider.page_parser')


class PageParser(Parser):
    def __init__(self, cookie, user_config, page, filter):
        self.cookie = cookie
        self.user_uri = user_config['user_uri']
        self.since_date = user_config['since_date']
        self.end_date = user_config['end_date']
        self.page = page
        self.url = 'https://weibo.cn/%s?page=%d' % (self.user_uri, page)
        if self.end_date != 'now':
            since_date = self.since_date.split(' ')[0].split('-')
            end_date = self.end_date.split(' ')[0].split('-')
            for date in [since_date, end_date]:
                for i in [1, 2]:
                    if len(date[i]) == 1:
                        date[i] = '0' + date[i]
            starttime = ''.join(since_date)
            endtime = ''.join(end_date)
            self.url = 'https://weibo.cn/%s/profile?starttime=%s&endtime=%s&advancedfilter=1&page=%d' % (
                self.user_uri, starttime, endtime, page)
        self.selector = handle_html(self.cookie, self.url)
        self.filter = filter

    def get_one_page(self, weibo_id_list):
        """获取第page页的全部微博"""
        try:
            info = self.selector.xpath("//div[@class='c']")
            is_exist = info[0].xpath("div/span[@class='ctt']")
            weibos = []
            if is_exist:
                since_date = datetime_util.str_to_time(self.since_date)
                for i in range(0, len(info) - 2):
                    weibo = self.get_one_weibo(info[i])
                    if weibo:
                        if weibo.id in weibo_id_list:
                            continue
                        publish_time = datetime_util.str_to_time(
                            weibo.publish_time)

                        if publish_time < since_date:
                            if self.is_pinned_weibo(info[i]):
                                continue
                            else:
                                return weibos, weibo_id_list, False
                        logger.info(weibo)
                        logger.info('-' * 100)
                        weibos.append(weibo)
                        weibo_id_list.append(weibo.id)
            return weibos, weibo_id_list, True
        except Exception as e:
            logger.exception(e)

    def is_original(self, info):
        """判断微博是否为原创微博"""
        is_original = info.xpath("div/span[@class='cmt']")
        if len(is_original) > 3:
            return False
        else:
            return True

    def get_original_weibo(self, info, weibo_id):
        """获取原创微博"""
        try:
            weibo_content = handle_garbled(info)
            weibo_content = weibo_content[:weibo_content.rfind(u'赞')]
            a_text = info.xpath('div//a/text()')
            if u'全文' in a_text:
                wb_content = CommentParser(self.cookie,
                                           weibo_id).get_long_weibo()
                if wb_content:
                    weibo_content = wb_content
            return weibo_content
        except Exception as e:
            logger.exception(e)

    def get_retweet(self, info, weibo_id):
        """获取转发微博"""
        try:
            weibo_content = handle_garbled(info)
            weibo_content = weibo_content[weibo_content.find(':') +
                                          1:weibo_content.rfind(u'赞')]
            weibo_content = weibo_content[:weibo_content.rfind(u'赞')]
            a_text = info.xpath('div//a/text()')
            if u'全文' in a_text:
                wb_content = CommentParser(self.cookie,
                                           weibo_id).get_long_retweet()
                if wb_content:
                    weibo_content = wb_content
            retweet_reason = handle_garbled(info.xpath('div')[-1])
            retweet_reason = retweet_reason[:retweet_reason.rindex(u'赞')]
            original_user = info.xpath("div/span[@class='cmt']/a/text()")
            if original_user:
                original_user = original_user[0]
                weibo_content = (retweet_reason + '\n' + u'原始用户: ' +
                                 original_user + '\n' + u'转发内容: ' +
                                 weibo_content)
            else:
                weibo_content = (retweet_reason + '\n' + u'转发内容: ' +
                                 weibo_content)
            return weibo_content
        except Exception as e:
            logger.exception(e)

    def get_weibo_content(self, info, is_original):
        """获取微博内容"""
        try:
            weibo_id = info.xpath('@id')[0][2:]
            if is_original:
                weibo_content = self.get_original_weibo(info, weibo_id)
            else:
                weibo_content = self.get_retweet(info, weibo_id)
            return weibo_content
        except Exception as e:
            logger.exception(e)

    def get_article_url(self, info):
        """获取微博头条文章的url"""
        article_url = ''
        text = handle_garbled(info)
        if text.startswith(u'发布了头条文章'):
            url = info.xpath('.//a/@href')
            if url and url[0].startswith('https://weibo.cn/sinaurl'):
                article_url = url[0]
        return article_url

    def get_publish_place(self, info):
        """获取微博发布位置"""
        try:
            div_first = info.xpath('div')[0]
            a_list = div_first.xpath('a')
            publish_place = u'无'
            for a in a_list:
                if ('place.weibo.com' in a.xpath('@href')[0]
                        and a.xpath('text()')[0] == u'显示地图'):
                    weibo_a = div_first.xpath("span[@class='ctt']/a")
                    if len(weibo_a) >= 1:
                        publish_place = weibo_a[-1]
                        if (u'视频' == div_first.xpath(
                                "span[@class='ctt']/a/text()")[-1][-2:]):
                            if len(weibo_a) >= 2:
                                publish_place = weibo_a[-2]
                            else:
                                publish_place = u'无'
                        publish_place = handle_garbled(publish_place)
                        break
            return publish_place
        except Exception as e:
            logger.exception(e)

    def get_publish_time(self, info):
        """获取微博发布时间"""
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = handle_garbled(str_time[0])
            publish_time = str_time.split(u'来自')[0]
            if u'刚刚' in publish_time:
                publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            elif u'分钟' in publish_time:
                minute = publish_time[:publish_time.find(u'分钟')]
                minute = timedelta(minutes=int(minute))
                publish_time = (datetime.now() -
                                minute).strftime('%Y-%m-%d %H:%M')
            elif u'今天' in publish_time:
                today = datetime.now().strftime('%Y-%m-%d')
                time = publish_time[3:]
                publish_time = today + ' ' + time
                if len(publish_time) > 16:
                    publish_time = publish_time[:16]
            elif u'月' in publish_time:
                year = datetime.now().strftime('%Y')
                month = publish_time[0:2]
                day = publish_time[3:5]
                time = publish_time[7:12]
                publish_time = year + '-' + month + '-' + day + ' ' + time
            else:
                publish_time = publish_time[:16]
            return publish_time
        except Exception as e:
            logger.exception(e)

    def get_publish_tool(self, info):
        """获取微博发布工具"""
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = handle_garbled(str_time[0])
            if len(str_time.split(u'来自')) > 1:
                publish_tool = str_time.split(u'来自')[1]
            else:
                publish_tool = u'无'
            return publish_tool
        except Exception as e:
            logger.exception(e)

    def get_weibo_footer(self, info):
        """获取微博点赞数、转发数、评论数"""
        try:
            footer = {}
            pattern = r'\d+'
            str_footer = info.xpath('div')[-1]
            str_footer = handle_garbled(str_footer)
            str_footer = str_footer[str_footer.rfind(u'赞'):]
            weibo_footer = re.findall(pattern, str_footer, re.M)

            up_num = int(weibo_footer[0])
            footer['up_num'] = up_num

            retweet_num = int(weibo_footer[1])
            footer['retweet_num'] = retweet_num

            comment_num = int(weibo_footer[2])
            footer['comment_num'] = comment_num
            return footer
        except Exception as e:
            logger.exception(e)

    def get_picture_urls(self, info, is_original):
        """获取微博原始图片url"""
        try:
            weibo_id = info.xpath('@id')[0][2:]
            picture_urls = {}
            if is_original:
                original_pictures = self.extract_picture_urls(info, weibo_id)
                picture_urls['original_pictures'] = original_pictures
                if not self.filter:
                    picture_urls['retweet_pictures'] = u'无'
            else:
                retweet_url = info.xpath("div/a[@class='cc']/@href")[0]
                retweet_id = retweet_url.split('/')[-1].split('?')[0]
                retweet_pictures = self.extract_picture_urls(info, retweet_id)
                picture_urls['retweet_pictures'] = retweet_pictures
                a_list = info.xpath('div[last()]/a/@href')
                original_picture = u'无'
                for a in a_list:
                    if a.endswith(('.gif', '.jpeg', '.jpg', '.png')):
                        original_picture = a
                        break
                picture_urls['original_pictures'] = original_picture
            return picture_urls
        except Exception as e:
            logger.exception(e)

    def get_video_url(self, info, is_original):
        """获取微博视频url"""
        try:
            video_url = u'无'
            if is_original:
                div_first = info.xpath('div')[0]
                a_list = div_first.xpath('.//a')
                video_link = u'无'
                for a in a_list:
                    if 'm.weibo.cn/s/video/show?object_id=' in a.xpath(
                            '@href')[0]:
                        video_link = a.xpath('@href')[0]
                        break
                if video_link != u'无':
                    video_link = video_link.replace(
                        'm.weibo.cn/s/video/show', 'm.weibo.cn/s/video/object')
                    try:
                        wb_info = requests.get(video_link,
                                               cookies=self.cookie).json()
                        video_url = wb_info['data']['object']['stream'].get(
                            'hd_url')
                        if not video_url:
                            video_url = wb_info['data']['object']['stream'][
                                'url']
                            if not video_url:  # 说明该视频为直播
                                video_url = u'无'
                    except json.decoder.JSONDecodeError:
                        logger.warning(u'当前账号没有浏览该视频的权限')
            return video_url
        except Exception as e:
            logger.exception(e)
            return u'无'

    def is_pinned_weibo(self, info):
        """判断微博是否为置顶微博"""
        kt = info.xpath(".//span[@class='kt']/text()")
        if kt and kt[0] == u'置顶':
            return True
        else:
            return False

    def get_one_weibo(self, info):
        """获取一条微博的全部信息"""
        try:
            weibo = Weibo()
            is_original = self.is_original(info)
            if (not self.filter) or is_original:
                weibo.id = info.xpath('@id')[0][2:]
                weibo.content = self.get_weibo_content(info,
                                                       is_original)  # 微博内容
                weibo.article_url = self.get_article_url(info)  # 头条文章url
                picture_urls = self.get_picture_urls(info, is_original)
                weibo.original_pictures = picture_urls[
                    'original_pictures']  # 原创图片url
                if not self.filter:
                    weibo.retweet_pictures = picture_urls[
                        'retweet_pictures']  # 转发图片url
                    weibo.original = is_original  # 是否原创微博
                weibo.video_url = self.get_video_url(info,
                                                     is_original)  # 微博视频url
                weibo.publish_place = self.get_publish_place(info)  # 微博发布位置
                weibo.publish_time = self.get_publish_time(info)  # 微博发布时间
                weibo.publish_tool = self.get_publish_tool(info)  # 微博发布工具
                footer = self.get_weibo_footer(info)
                weibo.up_num = footer['up_num']  # 微博点赞数
                weibo.retweet_num = footer['retweet_num']  # 转发数
                weibo.comment_num = footer['comment_num']  # 评论数
            else:
                weibo = None
                logger.info(u'正在过滤转发微博')
            return weibo
        except Exception as e:
            logger.exception(e)

    def extract_picture_urls(self, info, weibo_id):
        """提取微博原始图片url"""
        try:
            a_list = info.xpath('div/a/@href')
            first_pic = 'https://weibo.cn/mblog/pic/' + weibo_id
            all_pic = 'https://weibo.cn/mblog/picAll/' + weibo_id
            picture_urls = u'无'
            if first_pic in ''.join(a_list):
                if all_pic in ''.join(a_list):
                    preview_picture_list = MblogPicAllParser(
                        self.cookie, weibo_id).extract_preview_picture_list()
                    picture_list = [
                        p.replace('/thumb180/', '/large/')
                        for p in preview_picture_list
                    ]
                    picture_urls = ','.join(picture_list)
                else:
                    if info.xpath('.//img/@src'):
                        for link in info.xpath('div/a'):
                            if len(link.xpath('@href')) > 0:
                                if first_pic in link.xpath('@href')[0]:
                                    if len(link.xpath('img/@src')) > 0:
                                        preview_picture = link.xpath(
                                            'img/@src')[0]
                                        picture_urls = preview_picture.replace(
                                            '/wap180/', '/large/')
                                        break
                    else:
                        logger.warning(
                            u'爬虫微博可能被设置成了"不显示图片"，请前往'
                            u'"https://weibo.cn/account/customize/pic"，修改为"显示"'
                        )
                        sys.exit()
            return picture_urls
        except Exception as e:
            logger.exception(e)
            return u'无'
