* [功能](#功能)
* [输出](#输出)
* [实例](#实例)
* [运行环境](#运行环境)
* [使用说明](#使用说明)
  * [版本](#0版本)
  * [下载脚本](#1下载脚本)
  * [安装依赖](#2安装依赖)
  * [程序设置](#3程序设置)
  * [设置数据库（可选）](#4设置数据库可选)
  * [运行脚本](#5运行脚本)
  * [按需求修改脚本（可选）](#6按需求修改脚本可选)
* [如何获取cookie](#如何获取cookie)
* [如何获取user_id](#如何获取user_id)
* [注意事项](#注意事项)

## 功能
连续爬取**一个**或**多个**新浪微博用户（如[胡歌](https://weibo.cn/u/1223178222)、[迪丽热巴](https://weibo.cn/u/1669879400)、[郭碧婷](https://weibo.cn/u/1729370543)）的数据，并将结果信息写入**文件**或**数据库**。写入信息几乎包括了用户微博的所有数据，主要有**用户信息**和**微博信息**两大类，前者包含用户昵称、关注数、粉丝数、微博数等等；后者包含微博正文、发布时间、发布工具、评论数等等，因为内容太多，这里不再赘述，详细内容见[输出](#输出)部分。<br>
具体的写入文件类型如下：
- 写入**txt文件**（默认）
- 写入**csv文件**（默认）
- 写入**MySQL数据库**（可选）
- 写入**MongoDB数据库**（可选）
- 下载用户**原创**微博中的原始**图片**（可选）
- 下载用户**转发**微博中的原始**图片**（[免cookie版](https://github.com/dataabc/weibo-crawler)特有）
- 下载用户**原创**微博中的**视频**（可选）
- 下载用户**转发**微博中的**视频**（[免cookie版](https://github.com/dataabc/weibo-crawler)特有）<br>

当然，如果你只对用户信息感兴趣，而不需要爬用户的微博，也可以通过设置实现只爬取微博用户信息的功能。<br>
程序也可以实现**爬取结果自动更新**，即：现在爬取了目标用户的微博，几天之后，目标用户可能又发新微博了。通过设置，可以实现每隔几天增量爬取用户这几天发的新微博。<br>
本程序需要设置用户cookie，以获取微博访问权限，后面会讲解如何获取cookie。如需[免cookie版](https://github.com/dataabc/weibo-crawler)，大家可以访问<https://github.com/dataabc/weibo-crawler>，二者功能类似，免cookie版获取的信息更多，用法更简单，而且不需要cookie。<br>
## 输出
本部分为爬取到的字段信息说明，为了与[免cookie版](https://github.com/dataabc/weibo-crawler)区分，下面将两者爬取到的信息都列出来。如果是免cookie版所特有的信息，会有免cookie标注，没有标注的为二者共有的信息。<br>
**用户信息**
- 用户id：微博用户id，如"1669879400"，其实这个字段本来就是已知字段
- 昵称：用户昵称，如"Dear-迪丽热巴"
- 微博数：用户的全部微博数（转发微博+原创微博）
- 关注数：用户关注的微博数量
- 粉丝数：用户的粉丝数
- 性别（免cookie版）：微博用户性别
- 简介（免cookie版）：用户简介
- 主页地址（免cookie版）：微博移动版主页url，如<https://m.weibo.cn/u/1669879400?uid=1669879400&luicode=10000011&lfid=1005051669879400>
- 头像url（免cookie版）：用户头像url
- 高清头像url（免cookie版）：用户高清头像url
- 微博等级（免cookie版）：用户微博等级
- 会员等级（免cookie版）：微博会员用户等级，普通用户该等级为0
- 是否认证（免cookie版）：用户是否认证，为布尔类型
- 认证类型（免cookie版）：用户认证类型，如个人认证、企业认证、政府认证等
- 认证信息（免cookie版）：为认证用户特有，用户信息栏显示的认证信息
***
**微博信息**
- 微博id：微博唯一标志
- 微博内容：微博正文
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
<br>

## 实例
以爬取迪丽热巴的微博为例，我们需要修改**config.json**文件，文件内容如下：
```
{
    "user_id_list": ["1669879400"],
    "filter": 1,
    "since_date": "1900-01-01",
    "write_mode": ["csv", "txt"],
    "pic_download": 1,
    "video_download": 1,
    "cookie": "your cookie"
}
```

对于上述参数的含义以及取值范围，这里仅作简单介绍，详细信息见[程序设置](#3程序设置)。
>**user_id_list**代表我们要爬取的微博用户的user_id，可以是一个或多个，也可以是文件路径，微博用户Dear-迪丽热巴的user_id为1669879400，具体如何获取user_id见[如何获取user_id](#如何获取user_id)；<br>**filter**的值为1代表爬取全部原创微博，值为0代表爬取全部微博（原创+转发）；<br>**since_date**代表我们要爬取since_date日期之后发布的微博，因为我要爬迪丽热巴的全部原创微博，所以since_date设置了一个非常早的值；<br>**write_mode**代表结果文件的保存类型，我想要把结果写入txt文件和csv文件，所以它的值为["csv", "txt"]，如果你想写入数据库，具体设置见[设置数据库](#4设置数据库可选)；<br>**pic_download**值为1代表下载微博中的图片，值为0代表不下载；<br>**video_download**值为1代表下载微博中的视频，值为0代表不下载；<br>**cookie**是爬虫微博的cookie，具体如何获取cookie见[如何获取cookie](#如何获取cookie)，获取cookie后把"your cookie"替换成真实的cookie值即可。<br>

cookie修改完成后运行程序：
```bash
$ python weibospider.py
```
程序会自动生成一个weibo文件夹，我们以后爬取的所有微博都被存储在这里。然后程序在该文件夹下生成一个名为"Dear-迪丽热巴"的文件夹，迪丽热巴的所有微博爬取结果都在这里。"Dear-迪丽热巴"文件夹里包含一个csv文件、一个txt文件、一个img文件夹和一个video文件夹，img文件夹用来存储下载到的图片，video文件夹用来存储下载到的视频。如果你设置了保存数据库功能，这些信息也会保存在数据库里，数据库设置见[设置数据库](#4设置数据库可选)部分。<br>
<br>
csv文件结果如下所示：
![](https://picture.cognize.me/cognize/github/weibospider/weibo_csv.png)*1669879400.csv*<br>
<br>
txt文件结果如下所示：
![](https://picture.cognize.me/cognize/github/weibospider/weibo_txt.png)*1669879400.txt*<br>
<br>
下载的图片如下所示：
![](https://picture.cognize.me/cognize/github/weibospider/img.png)*img文件夹*<br>
本次下载了793张图片，大小一共1.21GB，包括她原创微博中的图片和转发微博转发理由中的图片。图片名为yyyymmdd+微博id的形式，若某条微博存在多张图片，则图片名中还会包括它在微博图片中的序号。若某张图片因为网络等原因下载失败，程序则会以“weibo_id:pic_url”的形式将出错微博id和图片url写入同文件夹下的not_downloaded.txt里；<br>
<br>
下载的视频如下所示：
![](https://picture.cognize.me/cognize/github/weibospider/video.png)*video文件夹*<br>
本次下载了70个视频，是她原创微博中的视频，视频名为yyyymmdd+微博id的形式。其中有一个视频因为网络原因下载失败，程序将它的微博id和视频url以“weibo_id:video_url”的形式写到了同文件夹下的not_downloaded.txt里。<br>
因为我本地没有安装MySQL数据库和MongoDB数据库，所以暂时设置成不写入数据库。如果你想要将爬取结果写入数据库，只需要先安装数据库（MySQL或MongoDB），再安装对应包（pymysql或pymongo），然后将mysql_write或mongodb_write值设置为1即可。写入MySQL需要用户名、密码等配置信息，这些配置如何设置见[设置数据库](#4设置数据库可选)部分。
## 运行环境
- 开发语言：python2/python3
- 系统： Windows/Linux/macOS

## 使用说明
### 0.版本
本程序有两个版本，**功能完成一样**。你现在看到的是单文件版，另一个是多文件版，[多文件版](https://github.com/dataabc/weiboSpider/tree/multi-file)位于multi-file分支。<br>
二者的区别在于：
>单文件版是所有代码都写到一个文件里，即[weiboSpider.py](https://github.com/dataabc/weiboSpider/blob/master/weiboSpider.py)。多文件版重构了单文件版，按照代码功能分成了几个文件，代码更清晰，更易读。如果你仅仅想使用程序，这两个版本用哪一个都一样；如果你不仅想使用，还想开发新功能，多文件版可能更容易。

多文件版由[songzy12](https://github.com/songzy12)重构。songzy12非常认真负责，对于我发现的问题都很耐心地修复了，而且效率非常高，在此感谢。<br>
本使用说明是单文件版的使用说明。
### 1.下载脚本
```bash
$ git clone https://github.com/dataabc/weibospider.git
```
运行上述命令，将本项目下载到当前目录，如果下载成功当前目录会出现一个名为"weibospider"的文件夹；
### 2.安装依赖
```bash
$ pip install -r requirements.txt
```
### 3.程序设置
打开**config.json**文件，你会看到如下内容：
```
{
    "user_id_list": ["1669879400"],
    "filter": 1,
    "since_date": "2018-01-01",
    "write_mode": ["csv", "txt"],
    "pic_download": 1,
    "video_download": 1,
    "cookie": "your cookie",
    "mysql_config": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "charset": "utf8mb4"
    }
}
```
下面讲解每个参数的含义与设置方法。<br>
**设置user_id_list**<br>
user_id_list是我们要爬取的微博的id，可以是一个，也可以是多个，例如：
```
"user_id_list": ["1223178222", "1669879400", "1729370543"],
```
上述代码代表我们要连续爬取user_id分别为“1223178222”、 “1669879400”、 “1729370543”的三个用户的微博，具体如何获取user_id见[如何获取user_id](#如何获取user_id)。<br>
user_id_list的值也可以是文件路径，我们可以把要爬的所有微博用户的user_id都写到txt文件里，然后把文件的位置路径赋值给user_id_list。<br>
在txt文件中，每个user_id占一行，也可以在user_id后面加注释（可选），如用户昵称等信息，user_id和注释之间必需要有空格，文件名任意，类型为txt，位置位于本程序的同目录下，文件内容示例如下：
```
1223178222 胡歌
1669879400 迪丽热巴
1729370543 郭碧婷
```
假如文件叫user_id_list.txt，则user_id_list设置代码为：
```
"user_id_list": "user_id_list.txt",
```
**设置filter**<br>
filter控制爬取范围，值为1代表爬取全部原创微博，值为0代表爬取全部微博（原创+转发）。例如，如果要爬全部原创微博，请使用如下代码：
```
"filter": 1,
```
**设置since_date**<br>
since_date值可以是日期，也可以是整数。如果是日期，代表爬取该日期之后的微博，格式应为“yyyy-mm-dd”，如：
```
"since_date": "2018-01-01",
```
代表爬取从2018年1月1日到现在的微博。<br>
如果是整数，代表爬取最近n天的微博，如:
```
"since_date": 10,
```
代表爬取最近10天的微博，这个说法不是特别准确，准确说是爬取发布时间从**10天前到本程序开始执行时**之间的微博。<br>
**设置write_mode**<br>
write_mode控制结果文件格式，取值范围是csv、txt、mongo和mysql，分别代表将结果文件写入csv、txt、MongoDB和MySQL数据库。write_mode可以同时包含这些取值中的一个或几个，如：
```
"write_mode": ["csv", "txt"],
```
代表将结果信息写入csv文件和txt文件。特别注意，如果你想写入数据库，除了在write_mode添加对应数据库的名字外，还应该安装相关数据库和对应python模块，具体操作见[设置数据库](#4设置数据库可选)部分。<br>
**设置pic_download**<br>
pic_download控制是否下载微博中的图片，值为1代表下载，值为0代表不下载，如
```
"pic_download": 1,
```
代表下载微博中的图片。<br>
**设置video_download**<br>
video_download控制是否下载微博中的视频，值为1代表下载，值为0代表不下载，如
```
"video_download": 1,
```
代表下载微博中的视频。<br>
**设置cookie**<br>
请按照[如何获取cookie](#如何获取cookie)，获取cookie，然后将“your cookie”替换成真实的cookie值。<br>
**设置mysql_config（可选）**<br>
mysql_config控制mysql参数配置。如果你不需要将结果信息写入mysql，这个参数可以忽略，即删除或保留都无所谓；如果你需要写入mysql且config.json文件中mysql_config的配置与你的mysql配置不一样，请将该值改成你自己mysql中的参数配置。

### 4.设置数据库（可选）
本部分是可选部分，如果不需要将爬取信息写入数据库，可跳过这一步。本程序目前支持MySQL数据库和MongoDB数据库，如果你需要写入其它数据库，可以参考这两个数据库的写法自己编写。<br>
**MySQL数据库写入**<br>
要想将爬取信息写入MySQL，请根据自己的系统环境安装MySQL，然后命令行执行：
```bash
$ pip install pymysql
```
**MongoDB数据库写入**<br>
要想将爬取信息写入MongoDB，请根据自己的系统环境安装MongoDB，然后命令行执行：
```bash
$ pip install pymongo
```
MySQL和MongDB数据库的写入内容一样。程序首先会创建一个名为"weibo"的数据库，然后再创建"user"表和"weibo"表，包含爬取的所有内容。爬取到的微博**用户信息**或插入或更新，都会存储到user表里；爬取到的**微博信息**或插入或更新，都会存储到weibo表里，两个表通过user_id关联。如果想了解两个表的具体字段，请点击"详情"。
<details>
<summary>详情</summary>
 
**user表**<br>
**id**：存储用户id，如"1669879400"；<br>
**nickname**：存储用户昵称，如"Dear-迪丽热巴"；<br>
**weibo_num**：存储微博数；<br>
**following**：存储关注数；<br>
**followers**：存储粉丝数。<br>
***
**weibo表**<br>
**id**：存储微博id；<br>
**user_id**：存储微博发布者的用户id，如"1669879400"；<br>
**content**：存储微博正文；<br>
**original_pictures**：存储原创微博的原始图片url和转发微博转发理由中的图片url。若某条微博有多张图片，则存储多个url，以英文逗号分割；若某微博没有图片，则值为"无"；<br>
**retweet_pictures**：存储被转发微博中的原始图片url。当最新微博为原创微博或者为没有图片的转发微博时，则值为"无"，否则为被转发微博的图片url。若有多张图片，则存储多个url，以英文逗号分割；<br>
**publish_place**：存储微博的发布位置。如果某条微博没有位置信息，则值为"无"；<br>
**publish_time**：存储微博的发布时间；<br>
**up_num**：存储微博获得的点赞数；<br>
**retweet_num**：存储微博获得的转发数；<br>
**comment_num**：存储微博获得的评论数；<br>
**publish_tool**：存储微博的发布工具。

</details>

### 5.运行脚本
大家可以根据自己的运行环境选择运行方式，Linux可以通过
```bash
$ python weibospider.py
```
运行;
### 6.按需求修改脚本（可选）
本部分为可选部分，如果你不需要自己修改代码或添加新功能，可以忽略此部分。<br>
本程序所有代码都位于weiboSpider.py文件，程序主体是一个Weibo类，上述所有功能都是通过在main函数调用Weibo类实现的，默认的调用代码如下：
```python
        config_path = os.path.split(
            os.path.realpath(__file__))[0] + os.sep + 'config.json'
        if not os.path.isfile(config_path):
            sys.exit(u'当前路径：%s 不存在配置文件config.json' %
                     (os.path.split(os.path.realpath(__file__))[0] + os.sep))
        with open(config_path) as f:
            config = json.loads(f.read())
        wb = Weibo(config)
        wb.start()  # 爬取微博信息
```
用户可以按照自己的需求调用或修改Weibo类。<br>
通过执行本程序，我们可以得到很多信息：<br>
**wb.nickname**：用户昵称；<br>
**wb.weibo_num**：微博数；<br>
**wb.following**：关注数；<br>
**wb.followers**：粉丝数；<br>
**wb.weibo**：除不包含上述信息外，wb.weibo包含爬取到的所有微博信息，如**微博id**、**微博正文**、**原始图片url**、**发布位置**、**发布时间**、**发布工具**、**点赞数**、**转发数**、**评论数**等。如果爬的是全部微博(原创+转发)，除上述信息之外，还包含被**转发微博原始图片url**、**是否为原创微博**等。wb.weibo是一个列表，包含了爬取的所有微博信息。wb.weibo[0]为爬取的第一条微博，wb.weibo[1]为爬取的第二条微博，以此类推。当filter=1时，wb.weibo[0]为爬取的第一条**原创**微博，以此类推。wb.weibo[0]['id']为第一条微博的id，wb.weibo[0]['content']为第一条微博的正文，wb.weibo[0]['publish_time']为第一条微博的发布时间，还有其它很多信息不在赘述，大家可以点击下面的"详情"查看具体用法。
<details>
  
<summary>详情</summary>

若目标微博用户存在微博，则：<br>
**id**：存储微博id。如wb.weibo[0]['id']为最新一条微博的id；<br>
**content**：存储微博正文。如wb.weibo[0]['content']为最新一条微博的正文；<br>
**original_pictures**：存储原创微博的原始图片url和转发微博转发理由中的图片url。如wb.weibo[0]['original_pictures']为最新一条微博的原始图片url，若该条微博有多张图片，则存储多个url，以英文逗号分割；若该微博没有图片，则值为"无"；<br>
**retweet_pictures**：存储被转发微博中的原始图片url。当最新微博为原创微博或者为没有图片的转发微博时，则值为"无"，否则为被转发微博的图片url。若有多张图片，则存储多个url，以英文逗号分割；<br>
**publish_place**：存储微博的发布位置。如wb.weibo[0]['publish_place']为最新一条微博的发布位置，如果该条微博没有位置信息，则值为"无"；<br>
**publish_time**：存储微博的发布时间。如wb.weibo[0]['publish_time']为最新一条微博的发布时间；<br>
**up_num**：存储微博获得的点赞数。如wb.weibo[0]['up_num']为最新一条微博获得的点赞数；<br>
**retweet_num**：存储微博获得的转发数。如wb.weibo[0]['retweet_num']为最新一条微博获得的转发数；<br>
**comment_num**：存储微博获得的评论数。如wb.weibo[0]['comment_num']为最新一条微博获得的评论数；<br>
**publish_tool**：存储微博的发布工具。如wb.weibo[0]['publish_tool']为最新一条微博的发布工具。

</details>

## 如何获取cookie
1.用Chrome打开<https://passport.weibo.cn/signin/login>；<br>
2.输入微博的用户名、密码，登录，如图所示：
![](https://picture.cognize.me/cognize/github/weibospider/cookie1.png)
登录成功后会跳转到<https://m.weibo.cn>;<br>
3.按F12键打开Chrome开发者工具，在地址栏输入并跳转到<https://weibo.cn>，跳转后会显示如下类似界面:
![](https://picture.cognize.me/cognize/github/weibospider/cookie2.png)
4.依此点击Chrome开发者工具中的Network->Name中的weibo.cn->Headers->Request Headers，"Cookie:"后的值即为我们要找的cookie值，复制即可，如图所示：
![](https://picture.cognize.me/cognize/github/weibospider/cookie3.png)

## 如何获取user_id
1.打开网址<https://weibo.cn>，搜索我们要找的人，如"迪丽热巴"，进入她的主页；<br>
![](https://picture.cognize.me/cognize/github/weibospider/user_home.png)
2.按照上图箭头所指，点击"资料"链接，跳转到用户资料页面；<br>
![](https://picture.cognize.me/cognize/github/weibospider/user_info.png)
如上图所示，迪丽热巴微博资料页的地址为"<https://weibo.cn/1669879400/info>"，其中的"1669879400"即为此微博的user_id。<br>
事实上，此微博的user_id也包含在用户主页(<https://weibo.cn/u/1669879400?f=search_0>)中，之所以我们还要点击主页中的"资料"来获取user_id，是因为很多用户的主页不是"<https://weibo.cn/user_id?f=search_0>"的形式，而是"<https://weibo.cn/个性域名?f=search_0>"或"<https://weibo.cn/微号?f=search_0>"的形式。其中"微号"和user_id都是一串数字，如果仅仅通过主页地址提取user_id，很容易将"微号"误认为user_id。

## 注意事项
1.user_id不能为爬虫微博的user_id。因为要爬微博信息，必须先登录到某个微博账号，此账号我们姑且称为爬虫微博。爬虫微博访问自己的页面和访问其他用户的页面，得到的网页格式不同，所以无法爬取自己的微博信息；<br>
2.cookie有期限限制，超过有效期需重新更新cookie。
