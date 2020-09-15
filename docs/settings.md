## 程序设置
**源码下载安装**的用户在weiboSpider目录下运行如下命令，**pip安装**的用户在任意有写权限的目录运行如下命令：
```bash
$ python3 -m weibo_spider
```
第一次运行会生成**config.json**文件，请打开**config.json**文件，你会看到如下内容：
```
{
    "user_id_list": ["1669879400"],
    "filter": 1,
    "since_date": "2018-01-01",
    "end_date": "now",
    "random_wait_pages": [1, 5],
    "random_wait_seconds": [6, 10],
    "global_wait": [[1000, 3600], [500, 2000]],    
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
    },
    "sqlite_config": "weibo.db"
}
```
下面讲解每个参数的含义与设置方法。<br>
**设置user_id_list**<br>
user_id_list是我们要爬取的微博的id，可以是一个，也可以是多个，例如：
```
"user_id_list": ["1223178222", "1669879400", "1729370543"],
```
上述代码代表我们要连续爬取user_id分别为“1223178222”、 “1669879400”、 “1729370543”的三个用户的微博，具体如何获取user_id见[如何获取user_id](https://github.com/dataabc/weiboSpider/blob/master/docs/userid.md)。<br>
user_id_list的值也可以是文件路径，我们可以把要爬的所有微博用户的user_id都写到txt文件里，然后把文件的位置路径赋值给user_id_list，**推荐这种方式**。<br>
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
**since_date是所有user的爬取起始时间，非常不灵活。如果你要爬多个用户，并且想单独为每个用户设置一个since_date，可以使用[定期自动爬取微博](https://github.com/dataabc/weiboSpider/blob/master/docs/automation.md)方法二中的方法，该方法可以为多个用户设置不同的since_date，非常灵活。**<br>
**设置end_date**<br>
end_date值可以是日期，也可以是"now"。如果是日期，代表爬取该日期之前的微博，格式应为“yyyy-mm-dd”；如果是"now"，代表爬取发布日期从since_date到现在的微博。since_date配合end_date，表示爬取发布日期在since_date和end_date之间的微博，包含边界。since_date是起始日期，end_date是结束日期，因此end_date时间应晚于since_date。注意，since_date即可以通过config.json文件的since_date参数设置，也可以通过user_id_list.txt设置；而end_date只能通过config.json文件的end_date参数设置，是全局变量，所有user_id都使用同一个end_date。当end_date值不是"now"时，程序无法获取微博中的视频，如果想要获取视频，请为end_date赋值为"now"。<br>
**设置random_wait_pages**<br>
random_wait_pages值是一个长度为2的整数列表，代表每爬取x页微博暂停一次，x为整数，值在random_wait_pages列表两个整数之间随机获取。默认值为[1, 5]，代表每爬取1到5页暂停一次，如果程序被限制，可以加快暂停频率，即适当减小random_wait_pages内的值。<br>
**设置random_wait_seconds**<br>
random_wait_seconds值是一个长度为2的整数列表，代表每次暂停sleep x 秒，x为整数， 值在random_wait_seconds列表两个整数之间随机获取。默认值为[6, 10]，代表每次暂停sleep 6到10秒，如果程序被限制，可以增加等待时间，即适当增大random_wait_seconds内的值。<br>
**设置global_wait**<br>
global_wait控制全局等待时间，默认值为[[1000, 3600], [500, 2000]]，代表获取1000页微博，程序一次性暂停3600秒；之后获取500页微博，程序再一次性暂停2000秒；之后如果再获取1000页微博，程序一次性暂停3600秒，以此类推。默认的只有前面的两个全局等待时间（[1000, 3600]和[500, 2000]），可以设置多个，如值可以为[[1000, 3600], [500, 3000], [700, 3600]]，程序会根据配置依次等待对应时间，如果配置全部被使用，程序会从第一个配置开始，依次使用，循环往复。<br>
**设置write_mode**<br>
write_mode控制结果文件格式，取值范围是csv、txt、json、mongo、mysql和sqlite，分别代表将结果文件写入csv、txt、json、MongoDB、MySQL和SQLite数据库。write_mode可以同时包含这些取值中的一个或几个，如：
```
"write_mode": ["csv", "txt"],
```
代表将结果信息写入csv文件和txt文件。特别注意，如果你想写入数据库，除了在write_mode添加对应数据库的名字外，还应该安装相关数据库和对应python模块，具体操作见[设置数据库](https://github.com/dataabc/weiboSpider/blob/master/docs/settings.md#设置数据库可选)部分。<br>
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
请按照[如何获取cookie](https://github.com/dataabc/weiboSpider/blob/master/docs/cookie.md)，获取cookie，然后将“your cookie”替换成真实的cookie值。<br>
**设置mysql_config（可选）**<br>
mysql_config控制mysql参数配置。如果你不需要将结果信息写入mysql，这个参数可以忽略，即删除或保留都无所谓；如果你需要写入mysql且config.json文件中mysql_config的配置与你的mysql配置不一样，请将该值改成你自己mysql中的参数配置。<br>
**设置sqlite_config（可选）**<br>
sqlite_config控制SQLite参数配置，代表SQLite数据库的保存路径，可根据自己需求修改。

## 设置数据库（可选）
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
**gender**：存储用户性别；<br>
**location**：存储用户所在地；<br>
**birthday**：存储用户出生日期；<br>
**description**：存储用户简介；<br>
**verified_reason**：存储用户认证；<br>
**talent**：存储用户标签；<br>
**education**：存储用户学习经历；<br>
**work**：存储用户工作经历；<br>
**weibo_num**：存储微博数；<br>
**following**：存储关注数；<br>
**followers**：存储粉丝数。<br>
***
**weibo表**<br>
**id**：存储微博id；<br>
**user_id**：存储微博发布者的用户id，如"1669879400"；<br>
**content**：存储微博正文；<br>
**article_url**：存储微博中头条文章的url，若微博中不存在头条文章，则值为''；<br>
**original_pictures**：存储原创微博的原始图片url和转发微博转发理由中的图片url。若某条微博有多张图片，则存储多个url，以英文逗号分割；若某微博没有图片，则值为"无"；<br>
**retweet_pictures**：存储被转发微博中的原始图片url。当最新微博为原创微博或者为没有图片的转发微博时，则值为"无"，否则为被转发微博的图片url。若有多张图片，则存储多个url，以英文逗号分割；<br>
**publish_place**：存储微博的发布位置。如果某条微博没有位置信息，则值为"无"；<br>
**publish_time**：存储微博的发布时间；<br>
**up_num**：存储微博获得的点赞数；<br>
**retweet_num**：存储微博获得的转发数；<br>
**comment_num**：存储微博获得的评论数；<br>
**publish_tool**：存储微博的发布工具。

</details>
