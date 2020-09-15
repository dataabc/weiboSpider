[![Build Status](https://github.com/dataabc/weiboSpider/workflows/Python%20application/badge.svg)](https://badge.fury.io/py/weibo-spider)
[![Python](https://img.shields.io/pypi/pyversions/weibo-spider)](https://badge.fury.io/py/weibo-spider)
[![PyPI](https://badge.fury.io/py/weibo-spider.svg)](https://badge.fury.io/py/weibo-spider)

# Weibo Spider

本程序可以连续爬取**一个**或**多个**新浪微博用户（如[胡歌](https://weibo.cn/u/1223178222)、[迪丽热巴](https://weibo.cn/u/1669879400)、[郭碧婷](https://weibo.cn/u/1729370543)）的数据，并将结果信息写入**文件**或**数据库**。写入信息几乎包括用户微博的所有数据，包括**用户信息**和**微博信息**两大类。因为内容太多，这里不再赘述，详细内容见[获取到的字段](#获取到的字段)。如果只需要用户信息，可以通过设置实现只爬取微博用户信息的功能。本程序需设置cookie来获取微博访问权限，后面会讲解[如何获取cookie](#如何获取cookie)。如果不想设置cookie，可以使用[免cookie版](https://github.com/dataabc/weibo-crawler)，二者功能类似。

具体的写入文件类型如下：

- 写入**txt文件**（默认）
- 写入**csv文件**（默认）
- 写入**json文件**（可选）
- 写入**MySQL数据库**（可选）
- 写入**MongoDB数据库**（可选）
- 写入**SQLite数据库**（可选）
- 下载用户**原创**微博中的原始**图片**（可选）
- 下载用户**转发**微博中的原始**图片**（[免cookie版](https://github.com/dataabc/weibo-crawler)特有）
- 下载用户**原创**微博中的**视频**（可选）
- 下载用户**转发**微博中的**视频**（[免cookie版](https://github.com/dataabc/weibo-crawler)特有）
- 下载用户**原创**微博**Live Photo**中的**视频**（[免cookie版](https://github.com/dataabc/weibo-crawler)特有）
- 下载用户**转发**微博**Live Photo**中的**视频**（[免cookie版](https://github.com/dataabc/weibo-crawler)特有）

## 内容列表

- [Weibo Spider](#weibo-spider)
  - [内容列表](#内容列表)
  - [获取到的字段](#获取到的字段)
  - [示例](#示例)
  - [运行环境](#运行环境)
  - [使用说明](#使用说明)
    - [0.版本](#0版本)
    - [1.安装程序](#1安装程序)
      - [源码安装](#源码安装)
      - [pip安装](#pip安装)
    - [2.程序设置](#2程序设置)
    - [3.运行程序](#3运行程序)
  - [个性化定制程序（可选）](#个性化定制程序可选)
  - [定期自动爬取微博（可选）](#定期自动爬取微博可选)
  - [如何获取cookie](#如何获取cookie)
  - [如何获取user_id](#如何获取user_id)
  - [常见问题](#常见问题)
  - [相关项目](#相关项目)
  - [贡献](#贡献)
  - [贡献者](#贡献者)
  - [注意事项](#注意事项)

## 获取到的字段

本部分为爬取到的字段信息说明，为了与[免cookie版](https://github.com/dataabc/weibo-crawler)区分，下面将两者爬取到的信息都列出来。如果是免cookie版所特有的信息，会有免cookie标注，没有标注的为二者共有的信息。

**用户信息**

- 用户id：微博用户id，如"1669879400"，其实这个字段本来就是已知字段
- 昵称：用户昵称，如"Dear-迪丽热巴"
- 性别：微博用户性别
- 生日：用户出生日期
- 所在地：用户所在地
- 学习经历：用户上学时学校的名字和时间
- 工作经历：用户所属公司名字和时间
- 阳光信用（免cookie版）：用户的阳光信用
- 微博注册时间（免cookie版）：用户微博注册日期
- 微博数：用户的全部微博数（转发微博+原创微博）
- 关注数：用户关注的微博数量
- 粉丝数：用户的粉丝数
- 简介：用户简介
- 主页地址（免cookie版）：微博移动版主页url
- 头像url（免cookie版）：用户头像url
- 高清头像url（免cookie版）：用户高清头像url
- 微博等级（免cookie版）：用户微博等级
- 会员等级（免cookie版）：微博会员用户等级，普通用户该等级为0
- 是否认证（免cookie版）：用户是否认证，为布尔类型
- 认证类型（免cookie版）：用户认证类型，如个人认证、企业认证、政府认证等
- 认证信息：为认证用户特有，用户信息栏显示的认证信息

***

**微博信息**

- 微博id：微博唯一标志
- 微博内容：微博正文
- 头条文章url：微博中头条文章的url，若微博中不存在头条文章，则值为''
- 原始图片url：原创微博图片和转发微博转发理由中图片的url，若某条微博存在多张图片，每个url以英文逗号分隔，若没有图片则值为"无"
- 视频url: 微博中的视频url，若微博中没有视频，则值为"无"
- 微博发布位置：位置微博中的发布位置
- 微博发布时间：微博发布时的时间，精确到分
- 点赞数：微博被赞的数量
- 转发数：微博被转发的数量
- 评论数：微博被评论的数量
- 微博发布工具：微博的发布工具，如iPhone客户端、HUAWEI Mate 20 Pro等
- 结果文件：保存在当前目录weibo文件夹下以用户昵称为名的文件夹里，名字为"user_id.csv"和"user_id.txt"的形式
- 微博图片：原创微博中的图片和转发微博转发理由中的图片，保存在以用户昵称为名的文件夹下的img文件夹里
- 微博视频：原创微博中的视频，保存在以用户昵称为名的文件夹下的video文件夹里
- 微博bid（免cookie版）：为[免cookie版](https://github.com/dataabc/weibo-crawler)所特有，与本程序中的微博id是同一个值
- 话题（免cookie版）：微博话题，即两个#中的内容，若存在多个话题，每个url以英文逗号分隔，若没有则值为''
- @用户（免cookie版）：微博@的用户，若存在多个@用户，每个url以英文逗号分隔，若没有则值为''
- 原始微博（免cookie版）：为转发微博所特有，是转发微博中那条被转发的微博，存储为字典形式，包含了上述微博信息中的所有内容，如微博id、微博内容等等

## 示例

如果想要知道程序的具体运行结果，可以查看[示例文档](https://github.com/dataabc/weiboSpider/blob/master/docs/example.md)，该文档介绍了爬取[迪丽热巴微博](https://weibo.cn/u/1669879400)的例子，并附有部分结果文件截图。

## 运行环境

- 开发语言：python2/python3
- 系统： Windows/Linux/macOS

## 使用说明

### 0.版本

本程序有两个版本，你现在看到的是python3版，另一个是python2版，python2版位于[python2分支](https://github.com/dataabc/weiboSpider/tree/python2)。目前主力开发python3版，包括新功能开发和bug修复；python2版仅支持bug修复。推荐python3用户使用当前版本，推荐python2用户使用[python2版](https://github.com/dataabc/weiboSpider/tree/python2)，本使用说明是python3版的使用说明。

### 1.安装程序

本程序提供两种安装方式，一种是**源码安装**，另一种是**pip安装**，二者功能完全相同。如果你需要修改源码，建议使用第一种方式，否则选哪种安装方式都可以。

#### 源码安装

```bash
$ git clone https://github.com/dataabc/weiboSpider.git
$ cd weiboSpider
$ pip install -r requirements.txt
```

#### pip安装

```bash
$ python3 -m pip install weibo-spider
```

### 2.程序设置

要了解程序设置，请查看[程序设置文档](https://github.com/dataabc/weiboSpider/blob/master/docs/settings.md)。

### 3.运行程序

**源码安装**的用户可以在weiboSpider目录运行如下命令，**pip安装**的用户可以在任意有写权限的目录运行如下命令

```bash
$ python3 -m weibo_spider
```

第一次执行，会自动在当前目录创建config.json配置文件，配置好后执行同样的命令就可以获取微博了。

如果你已经有config.json文件了，也可以通过config_path参数配置config.json路径，运行程序，命令行如下：

```bash
$ python3 -m weibo_spider --config_path="config.json"
```

如果你想指定文件（csv、txt、json、图片、视频）保存路径，可以通过output_dir参数设定。假如你想把文件保存到/home/weibo/目录，可以运行如下命令：
```
$ python3 -m weibo_spider --output_dir="/home/weibo/"
```
如果你想通过命令行输入user_id，可以使用参数u，可以输入一个或多个user_id，每个user_id以英文逗号分开，如果这些user_id中有重复的user_id，程序会自动去重。命令行如下：
```
$ python3 -m weibo_spider --u="1669879400,1223178222"
```
程序会获取user_id分别为1669879400和1223178222的微博用户的微博，后面会讲[如何获取user_id](#如何获取user_id)。该方式的所有user_id使用config.json中的since_date和end_date设置，通过修改它们的值可以控制爬取的时间范围。若config.json中的user_id_list是文件路径，每个命令行中的user_id都会自动保存到该文件内，且自动更新since_date；若不是路径，user_id会保存在当前目录的user_id_list.txt内，且自动更新since_date，若当前目录下不存在user_id_list.txt，程序会自动创建它。

## 个性化定制程序（可选）

本部分为可选部分，如果不需要个性化定制程序或添加新功能，可以忽略此部分。

本程序主体代码位于weibo_spider.py文件，程序主体是一个 Spider 类，上述所有功能都是通过在main函数调用 Spider 类实现的，默认的调用代码如下：

```python
        config = get_config()
        wb = Spider(config)
        wb.start()  # 爬取微博信息
```

用户可以按照自己的需求调用或修改 Spider 类。通过执行本程序，我们可以得到很多信息。

<details>

<summary>点击查看详情</summary>

- wb.user['nickname']：用户昵称；
- wb.user['gender']：用户性别；
- wb.user['location']：用户所在地；
- wb.user['birthday']：用户出生日期；
- wb.user['description']：用户简介；
- wb.user['verified_reason']：用户认证；
- wb.user['talent']：用户标签；
- wb.user['education']：用户学习经历；
- wb.user['work']：用户工作经历；
- wb.user['weibo_num']：微博数；
- wb.user['following']：关注数；
- wb.user['followers']：粉丝数；
</details>

**wb.weibo**：除不包含上述信息外，wb.weibo包含爬取到的所有微博信息，如**微博id**、**微博正文**、**原始图片url**、**发布位置**、**发布时间**、**发布工具**、**点赞数**、**转发数**、**评论数**等。如果爬的是全部微博(原创+转发)，除上述信息之外，还包含被**转发微博原始图片url**、**是否为原创微博**等。wb.weibo是一个列表，包含了爬取的所有微博信息。wb.weibo[0]为爬取的第一条微博，wb.weibo[1]为爬取的第二条微博，以此类推。当filter=1时，wb.weibo[0]为爬取的第一条**原创**微博，以此类推。wb.weibo[0]['id']为第一条微博的id，wb.weibo[0]['content']为第一条微博的正文，wb.weibo[0]['publish_time']为第一条微博的发布时间，还有其它很多信息不在赘述，大家可以点击下面的"详情"查看具体用法。

<details>
  
<summary>详情</summary>

若目标微博用户存在微博，则：

- id：存储微博id。如wb.weibo[0]['id']为最新一条微博的id；
- content：存储微博正文。如wb.weibo[0]['content']为最新一条微博的正文；
- article_url：存储微博中头条文章的url。如wb.weibo[0]['article_url']为最新一条微博的头条文章url，若微博中不存在头条文章，则值为''；
- original_pictures：存储原创微博的原始图片url和转发微博转发理由中的图片url。如wb.weibo[0]['original_pictures']为最新一条微博的原始图片url，若该条微博有多张图片，则存储多个url，以英文逗号分割；若该微博没有图片，则值为"无"；
- retweet_pictures：存储被转发微博中的原始图片url。当最新微博为原创微博或者为没有图片的转发微博时，则值为"无"，否则为被转发微博的图片url。若有多张图片，则存储多个url，以英文逗号分割；
- publish_place：存储微博的发布位置。如wb.weibo[0]['publish_place']为最新一条微博的发布位置，如果该条微博没有位置信息，则值为"无"；
- publish_time：存储微博的发布时间。如wb.weibo[0]['publish_time']为最新一条微博的发布时间；
- up_num：存储微博获得的点赞数。如wb.weibo[0]['up_num']为最新一条微博获得的点赞数；
- retweet_num：存储微博获得的转发数。如wb.weibo[0]['retweet_num']为最新一条微博获得的转发数；
- comment_num：存储微博获得的评论数。如wb.weibo[0]['comment_num']为最新一条微博获得的评论数；
- publish_tool：存储微博的发布工具。如wb.weibo[0]['publish_tool']为最新一条微博的发布工具。

</details>

## 定期自动爬取微博（可选）

要想让程序每个一段时间自动爬取，且爬取的内容为新增加的内容（不包括已经获取的微博），请查看[定期自动爬取微博](https://github.com/dataabc/weiboSpider/blob/master/docs/automation.md)。

## 如何获取cookie

要了解获取cookie方法，请查看[cookie文档](https://github.com/dataabc/weiboSpider/blob/master/docs/cookie.md)。

## 如何获取user_id

要了解获取user_id方法，请查看[user_id文档](https://github.com/dataabc/weiboSpider/blob/master/docs/userid.md)，该文档介绍了如何获取一个及多个微博用户user_id的方法。

## 常见问题

如果运行程序的过程中出现错误，可以查看[常见问题](https://github.com/dataabc/weiboSpider/blob/master/docs/FAQ.md)页面，里面包含了最常见的问题及解决方法。如果出现的错误不在常见问题里，您可以通过[发issue](https://github.com/dataabc/weiboSpider/issues/new/choose)寻求帮助，我们会很乐意为您解答。

## 相关项目

- [weibo-crawler](https://github.com/dataabc/weibo-crawler) - 功能和本项目完全一样，可以不添加cookie，获取的微博属性更多；
- [weibo-search](https://github.com/dataabc/weibo-search) - 可以连续获取一个或多个**微博关键词搜索**结果，并将结果写入文件（可选）、数据库（可选）等。所谓微博关键词搜索即：**搜索正文中包含指定关键词的微博**，可以指定搜索的时间范围。对于非常热门的关键词，一天的时间范围，可以获得**1000万**以上的搜索结果，N天的时间范围就可以获得1000万 X N搜索结果。对于大多数关键词，一天产生的相应微博数量应该在1000万条以下，因此可以说该程序可以获得大部分关键词的全部或近似全部的搜索结果。而且该程序可以获得搜索结果的所有信息，本程序获得的微博信息该程序都能获得。

## 贡献

欢迎为本项目贡献力量。贡献可以是提交代码，可以是通过issue提建议（如新功能、改进方案等），也可以是通过issue告知我们项目存在哪些bug、缺点等，具体贡献方式见[为本项目做贡献](https://github.com/dataabc/weiboSpider/blob/master/CONTRIBUTING.md)。

## 贡献者

感谢所有为本项目贡献力量的朋友，贡献者详情见[贡献者](https://github.com/dataabc/weiboSpider/blob/master/docs/contributors.md)页面。

## 注意事项

1.user_id不能为爬虫微博的user_id。因为要爬微博信息，必须先登录到某个微博账号，此账号我们姑且称为爬虫微博。爬虫微博访问自己的页面和访问其他用户的页面，得到的网页格式不同，所以无法爬取自己的微博信息；如果想要爬取爬虫微博内容，可以参考[获取自身微博信息](https://github.com/dataabc/weiboSpider/issues/113)；

2.cookie有期限限制，大约三个月。若提示cookie错误或已过期，需要重新更新cookie。
