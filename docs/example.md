## 实例
以爬取迪丽热巴的微博为例，我们需要修改**config.json**文件，文件内容如下：
```
{
    "user_id_list": ["1669879400"],
    "filter": 1,
    "since_date": "1900-01-01",
    "end_date": "now",
    "write_mode": ["csv", "txt", "json"],
    "pic_download": 1,
    "video_download": 1,
    "cookie": "your cookie"
}
```

对于上述参数的含义以及取值范围，这里仅作简单介绍，详细信息见[程序设置](https://github.com/dataabc/weiboSpider/blob/master/docs/settings.md)。
>**user_id_list**代表我们要爬取的微博用户的user_id，可以是一个或多个，也可以是文件路径，微博用户Dear-迪丽热巴的user_id为1669879400，具体如何获取user_id见[如何获取user_id](https://github.com/dataabc/weiboSpider/blob/master/docs/userid.md)；<br>**filter**的值为1代表爬取全部原创微博，值为0代表爬取全部微博（原创+转发）；<br>**since_date**代表我们要爬取since_date日期之后发布的微博，因为我要爬迪丽热巴的全部原创微博，所以since_date设置了一个非常早的值；<br>**end_date**代表我们要爬取end_date日期之前发布的微博，since_date配合end_date，表示我们要爬取发布日期在since_date和end_date之间的微博，包含边界，如果end_date值为"now"，表示爬取发布日期从since_date到现在的微博；<br>**write_mode**代表结果文件的保存类型，我想要把结果写入txt文件、csv文件和json文件，所以它的值为["csv", "txt", "json"]，如果你想写入数据库，具体设置见[设置数据库](https://github.com/dataabc/weiboSpider/blob/master/docs/settings.md#设置数据库可选)；<br>**pic_download**值为1代表下载微博中的图片，值为0代表不下载；<br>**video_download**值为1代表下载微博中的视频，值为0代表不下载；<br>**cookie**是爬虫微博的cookie，具体如何获取cookie见[cookie文档](https://github.com/dataabc/weiboSpider/blob/master/docs/cookie.md)，获取cookie后把"your cookie"替换成真实的cookie值即可。<br>

cookie修改完成后在weiboSpider目录下运行如下命令：
```bash
$ python3 -m weibo_spider
```
程序会自动生成一个weibo文件夹，我们以后爬取的所有微博都被存储在这里。然后程序在该文件夹下生成一个名为"Dear-迪丽热巴"的文件夹，迪丽热巴的所有微博爬取结果都在这里。"Dear-迪丽热巴"文件夹里包含一个csv文件、一个txt文件、一个json文件、一个img文件夹和一个video文件夹，img文件夹用来存储下载到的图片，video文件夹用来存储下载到的视频。如果你设置了保存数据库功能，这些信息也会保存在数据库里，数据库设置见[设置数据库](https://github.com/dataabc/weiboSpider/blob/master/docs/settings.md#设置数据库可选)部分。<br>
<br>
**csv结果文件如下所示：**
![](https://picture.cognize.me/cognize/github/weibospider/weibo_csv.png)*1669879400.csv*<br>
<br>
**txt结果文件如下所示：**
![](https://picture.cognize.me/cognize/github/weibospider/weibo_txt.png)*1669879400.txt*<br>
<br>
json文件包含迪丽热巴的用户信息和上千条微博信息，内容较多。为了表达清晰，这里仅展示两条微博。<br>
**json结果文件如下所示：**
```
{
    "user": {
        "id": "1669879400",
        "nickname": "Dear-迪丽热巴",
        "gender": "女",
        "location": "上海",
        "birthday": "双子座",
        "description": "一只喜欢默默表演的小透明。工作联系jaywalk@jaywalk.com.cn 🍒",
        "verified_reason": "嘉行传媒签约演员",
        "talent": "",
        "education": "上海戏剧学院",
        "work": "嘉行传媒 ",
        "weibo_num": 1121,
        "following": 250,
        "followers": 66395910
    },
    "weibo": [
        {
            "id": "IonM9ryMy",
            "content": "2019#微博之夜#盛典即将开启，以微博之力，让世界更美。1月11日，不见不散@微博之夜  原图 ",
            "original_pictures": "http://wx1.sinaimg.cn/large/63885668ly1gao0a01kfzj20ku112k98.jpg",
            "video_url": "无",
            "publish_place": "无",
            "publish_time": "2020-01-07 14:59",
            "publish_tool": "无",
            "up_num": 239242,
            "retweet_num": 71914,
            "comment_num": 55916
        },
        {
            "id": "InB4Df73X",
            "content": "#happyNEOyear#都到了2020，还不换点新pose配新装[來] 穿上@adidasneo 迪士尼联名款，让#生来好动#的我们一起玩“新”大发、自拍不重样🤳http://t.cn/AiF7nREj adidasneo的微博视频  ",
            "original_pictures": "无",
            "video_url": "http://f.video.weibocdn.com/000pYrGmlx07zPTskBQQ010412008AOY0E010.mp4?label=mp4_hd&template=852x480.25.0&trans_finger=62b30a3f061b162e421008955c73f536&Expires=1578569162&ssig=IV3JEbh3Zu&KID=unistore,video",
            "publish_place": "无",
            "publish_time": "2020-01-02 11:00",
            "publish_tool": "无",
            "up_num": 275419,
            "retweet_num": 376734,
            "comment_num": 131069
        }
    ]
}
```
*1669879400.json*<br>
<br>
**下载的图片如下所示：**
![](https://picture.cognize.me/cognize/github/weibospider/img.png)*img文件夹*<br>
本次下载了793张图片，大小一共1.21GB，包括她原创微博中的图片和转发微博转发理由中的图片。图片名为yyyymmdd+微博id的形式，若某条微博存在多张图片，则图片名中还会包括它在微博图片中的序号。若某张图片因为网络等原因下载失败，程序则会以“weibo_id:pic_url”的形式将出错微博id和图片url写入同文件夹下的not_downloaded.txt里；<br>
<br>
**下载的视频如下所示：**
![](https://picture.cognize.me/cognize/github/weibospider/video.png)*video文件夹*<br>
本次下载了70个视频，是她原创微博中的视频，视频名为yyyymmdd+微博id的形式。其中有一个视频因为网络原因下载失败，程序将它的微博id和视频url以“weibo_id:video_url”的形式写到了同文件夹下的not_downloaded.txt里。<br>
因为我本地没有安装MySQL数据库和MongoDB数据库，所以暂时设置成不写入数据库。如果你想要将爬取结果写入数据库，只需要先安装数据库（MySQL或MongoDB），再安装对应包（pymysql或pymongo），然后将mysql_write或mongodb_write值设置为1即可。写入MySQL需要用户名、密码等配置信息，这些配置如何设置见[设置数据库](https://github.com/dataabc/weiboSpider/blob/master/docs/settings.md#设置数据库可选)部分。
