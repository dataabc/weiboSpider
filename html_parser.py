# -*- coding: UTF-8 -*-
import re
import sys
import traceback
from collections import OrderedDict
from datetime import datetime, timedelta

import requests
from lxml import etree


class Parser:
    def __init__(self, config):
        self.config = config

    def deal_html(self, url, cookie):
        """处理html"""
        print("url:", url)
        html = requests.get(url, cookies=cookie).content
        selector = etree.HTML(html)
        return selector

    def deal_garbled(self, info):
        """处理乱码"""
        info = (info.xpath('string(.)').replace(u'\u200b', '').encode(
            sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding))
        return info

    def extract_picture_urls(self, info, weibo_id):
        """提取微博原始图片url"""
        try:
            a_list = info.xpath('div/a/@href')
            first_pic = 'https://weibo.cn/mblog/pic/' + weibo_id + '?rl=0'
            all_pic = 'https://weibo.cn/mblog/picAll/' + weibo_id + '?rl=1'
            if first_pic in a_list:
                if all_pic in a_list:
                    selector = self.deal_html(all_pic, self.config['cookie'])
                    preview_picture_list = selector.xpath('//img/@src')
                    picture_list = [
                        p.replace('/thumb180/', '/large/')
                        for p in preview_picture_list
                    ]
                    picture_urls = ','.join(picture_list)
                else:
                    if info.xpath('.//img/@src'):
                        preview_picture = info.xpath('.//img/@src')[-1]
                        picture_urls = preview_picture.replace(
                            '/wap180/', '/large/')
                    else:
                        sys.exit(
                            u"爬虫微博可能被设置成了'不显示图片'，请前往"
                            u"'https://weibo.cn/account/customize/pic'，修改为'显示'"
                        )
            else:
                picture_urls = u'无'
            return picture_urls
        except Exception:
            return u'无'

    def get_picture_urls(self, info, is_original):
        """获取微博原始图片url"""
        try:
            weibo_id = info.xpath('@id')[0][2:]
            picture_urls = {}
            if is_original:
                original_pictures = self.extract_picture_urls(info, weibo_id)
                picture_urls['original_pictures'] = original_pictures
                if not self.config['filter']:
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
            print('Error: ', e)
            traceback.print_exc()

    def get_video_url(self, info, is_original):
        """获取微博视频url"""
        try:
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
                    wb_info = requests.get(
                        video_link, cookies=self.config['cookie']).json()
                    video_url = wb_info['data']['object']['stream'].get(
                        'hd_url')
                    if not video_url:
                        video_url = wb_info['data']['object']['stream']['url']
                        if not video_url:  # 说明该视频为直播
                            video_url = u'无'
            else:
                video_url = u'无'
            return video_url
        except Exception:
            return u'无'

    def get_page_num(self, selector):
        """获取微博总页数"""

        if selector.xpath("//input[@name='mp']") == []:
            page_num = 1
        else:
            page_num = (int)(
                selector.xpath("//input[@name='mp']")[0].attrib['value'])
        return page_num

    def get_long_weibo(self, weibo_link):
        """获取长原创微博"""

        selector = self.deal_html(weibo_link, self.config['cookie'])
        info = selector.xpath("//div[@class='c']")[1]
        wb_content = self.deal_garbled(info)
        wb_time = info.xpath("//span[@class='ct']/text()")[0]
        weibo_content = wb_content[wb_content.find(':') +
                                   1:wb_content.rfind(wb_time)]
        return weibo_content

    def get_original_weibo(self, info, weibo_id):
        """获取原创微博"""

        weibo_content = self.deal_garbled(info)
        weibo_content = weibo_content[:weibo_content.rfind(u'赞')]
        a_text = info.xpath('div//a/text()')
        if u'全文' in a_text:
            weibo_link = 'https://weibo.cn/comment/' + weibo_id
            wb_content = self.get_long_weibo(weibo_link)
            if wb_content:
                weibo_content = wb_content
        return weibo_content

    def get_long_retweet(self, weibo_link):
        """获取长转发微博"""
        wb_content = self.get_long_weibo(weibo_link)
        weibo_content = wb_content[:wb_content.rfind(u'原文转发')]
        return weibo_content

    def get_retweet(self, info, weibo_id):
        """获取转发微博"""
        wb_content = self.deal_garbled(info)
        wb_content = wb_content[wb_content.find(':') +
                                1:wb_content.rfind(u'赞')]
        wb_content = wb_content[:wb_content.rfind(u'赞')]
        a_text = info.xpath('div//a/text()')
        if u'全文' in a_text:
            weibo_link = 'https://weibo.cn/comment/' + weibo_id
            weibo_content = self.get_long_retweet(weibo_link)
            if weibo_content:
                wb_content = weibo_content
        retweet_reason = self.deal_garbled(info.xpath('div')[-1])
        retweet_reason = retweet_reason[:retweet_reason.rindex(u'赞')]
        original_user = info.xpath("div/span[@class='cmt']/a/text()")
        if original_user:
            original_user = original_user[0]
            wb_content = (retweet_reason + '\n' + u'原始用户: ' + original_user +
                          '\n' + u'转发内容: ' + wb_content)
        else:
            wb_content = retweet_reason + '\n' + u'转发内容: ' + wb_content
        return wb_content

    def is_original(self, info):
        """判断微博是否为原创微博"""
        is_original = info.xpath("div/span[@class='cmt']")
        if len(is_original) > 3:
            return False
        else:
            return True

    def get_weibo_content(self, info, is_original):
        """获取微博内容"""
        weibo_id = info.xpath('@id')[0][2:]
        if is_original:
            weibo_content = self.get_original_weibo(info, weibo_id)
        else:
            weibo_content = self.get_retweet(info, weibo_id)
        return weibo_content

    def get_publish_place(self, info):
        """获取微博发布位置"""
        div_first = info.xpath('div')[0]
        a_list = div_first.xpath('a')
        publish_place = u'无'
        for a in a_list:
            if ('place.weibo.com' in a.xpath('@href')[0]
                    and a.xpath('text()')[0] == u'显示地图'):
                weibo_a = div_first.xpath("span[@class='ctt']/a")
                if len(weibo_a) >= 1:
                    publish_place = weibo_a[-1]
                    if (u'视频' == div_first.xpath("span[@class='ctt']/a/text()")
                        [-1][-2:]):
                        if len(weibo_a) >= 2:
                            publish_place = weibo_a[-2]
                        else:
                            publish_place = u'无'
                    publish_place = self.deal_garbled(publish_place)
                    break
        return publish_place

    def get_publish_time(self, info):
        """获取微博发布时间"""
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = self.deal_garbled(str_time[0])
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
            print('Error: ', e)
            traceback.print_exc()

    def get_publish_tool(self, info):
        """获取微博发布工具"""
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = self.deal_garbled(str_time[0])
            if len(str_time.split(u'来自')) > 1:
                publish_tool = str_time.split(u'来自')[1]
            else:
                publish_tool = u'无'
            return publish_tool
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_weibo_footer(self, info):
        """获取微博点赞数、转发数、评论数"""
        try:
            footer = {}
            pattern = r'\d+'
            str_footer = info.xpath('div')[-1]
            str_footer = self.deal_garbled(str_footer)
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
            print('Error: ', e)
            traceback.print_exc()

    def get_one_weibo(self, info):
        """获取一条微博的全部信息"""
        try:
            weibo = OrderedDict()
            is_original = self.is_original(info)
            if (not self.config['filter']) or is_original:
                weibo['id'] = info.xpath('@id')[0][2:]
                weibo['content'] = self.get_weibo_content(info,
                                                          is_original)  # 微博内容
                weibo['publish_place'] = self.get_publish_place(info)  # 微博发布位置
                weibo['publish_time'] = self.get_publish_time(info)  # 微博发布时间
                weibo['publish_tool'] = self.get_publish_tool(info)  # 微博发布工具
                footer = self.get_weibo_footer(info)
                weibo['up_num'] = footer['up_num']  # 微博点赞数
                weibo['retweet_num'] = footer['retweet_num']  # 转发数
                weibo['comment_num'] = footer['comment_num']  # 评论数

                picture_urls = self.get_picture_urls(info, is_original)
                weibo['original_pictures'] = picture_urls[
                    'original_pictures']  # 原创图片url
                if not self.config['filter']:
                    weibo['retweet_pictures'] = picture_urls[
                        'retweet_pictures']  # 转发图片url
                    weibo['original'] = is_original  # 是否原创微博
                weibo['video_url'] = self.get_video_url(info,
                                                        is_original)  # 微博视频url
            else:
                weibo = None
            return weibo
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def is_pinned_weibo(self, info):
        """判断微博是否为置顶微博"""
        kt = info.xpath(".//span[@class='kt']/text()")
        if kt and kt[0] == u'置顶':
            return True
        else:
            return False
