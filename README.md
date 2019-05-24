# 功能
爬取新浪微博信息，并写入csv/txt文件，文件名为目标用户id加".csv"和".txt"的形式。<br>
<br>
csv文件结果如下所示:
![](https://picture.cognize.me/cognize/github/weibospider/weibo_csv.png)*1669879400.csv*

txt文件结果如下所示：
![](https://picture.cognize.me/cognize/github/weibospider/weibotxt.png)*1669879400.txt*

# 输入
用户id，例如新浪微博昵称为“Dear-迪丽热巴”的id为“1669879400”

# 输出
- 用户名：用户昵称，如"Dear-迪丽热巴"
- 微博数：用户的全部微博数（转发微博+原创微博）
- 关注数：用户关注的微博账号数量
- 粉丝数：用户的粉丝数
- 微博内容：以list的形式存储了用户所有微博内容
- 微博位置：以list的形式存储了用户所有微博的发布位置
- 微博发布时间：以list的形式存储了用户所有微博的发布时间
- 微博对应的点赞数：以list的形式存储了用户所有微博对应的点赞数
- 微博对应的转发数：以list的形式存储了用户所有微博对应的转发数
- 微博对应的评论数：以list的形式存储了用户所有微博对应的评论数
- 微博发布工具：以list的形式存储了用户所有微博的发布工具,如iPhone客户端、HUAWEI Mate 20 Pro等
- 结果文件：保存在当前目录的weibo文件夹里，名字为"user_id.csv"和"user_id.txt"的形式

# 运行环境
- 开发语言：python2/python3
- 系统： Windows/Linux

# 使用说明
## 1.下载脚本
```bash
$ git clone https://github.com/dataabc/weibospider.git
```
运行上述命令，将本项目下载到当前目录，如果下载成功当前目录会出现一个名为"weibospider"的文件夹；
## 2.设置cookie和user_id
打开weibospider文件夹下的"**weibospider.py**"文件,将“**your cookie**”替换成爬虫微博的cookie，后面会详细讲解如何获取cookie；将**user_id**替换成想要爬取的微博的user_id，后面会详细讲解如何获取user_id;
## 3.运行脚本
大家可以根据自己的运行环境选择运行方式,Linux可以通过
```bash
$ python weibospider.py
```
运行;
## 4.按需求修改脚本（可选）
本脚本是一个Weibo类，用户可以按照自己的需求调用Weibo类。
例如用户可以直接在"weibospider.py"文件中调用Weibo类，具体调用代码示例如下：
```python
user_id = 1669879400
filter = 1
wb = Weibo(user_id,filter) #调用Weibo类，创建微博实例wb
wb.start()  #爬取微博信息
```
user_id可以改成任意合法的用户id（爬虫的微博id除外）；filter默认值为0，表示爬取所有微博信息（转发微博+原创微博），为1表示只爬取用户的所有原创微博；wb是Weibo类的一个实例，也可以是其它名字，只要符合python的命名规范即可；通过执行wb.start() 完成了微博的爬取工作。在上述代码执行后，我们可以得到很多信息：<br>
**wb.username**：用户名；<br>
**wb.weibo_num**：微博数；<br>
**wb.following**：关注数；<br>
**wb.followers**：粉丝数；<br>
**wb.weibo_content**：存储用户的所有微博，为list形式，若filter=1， wb.weibo_content[0]为最新一条**原创**微博，filter=0为最新一条微博，wb.weibo_content[1]、wb.weibo_content[2]分别表示第二新和第三新的微博，以此类推。当然如果用户没有发过微博，则wb.weibo_content为[]；<br>
**wb.weibo_place**: 存储微博的发布位置，为list形式，如wb.weibo_place[0]为最新一条微博的发布位置，与wb.weibo_content[0]对应，如果该条微博没有位置信息，则weibo_place内容为无,其它用法同wb.weibo_content；<br>
**wb.publish_time**: 存储微博的发布时间，为list形式，如wb.publish_time[0]为最新一条微博的发布时间，与wb.weibo_content[0]对应，其它用法同wb.weibo_content；<br>
**wb.up_num**：存储微博获得的点赞数，为list形式，如wb.up_num[0]为最新一条微博获得的点赞数，与wb.weibo_content[0]对应，其它用法同wb.weibo_content；<br>
**wb.retweet_num**：存储微博获得的转发数，为list形式，如wb.retweet_num[0]为最新一条微博获得的转发数，与wb.weibo_content[0]对应，其它用法同wb.weibo_content；<br>
**wb.comment_num**：存储微博获得的评论数，为list形式，如wb.comment_num[0]为最新一条微博获得的评论数，与wb.weibo_content[0]对应，其它用法同wb.weibo_content；<br>
**wb.publish_tool**：存储微博的发布工具，为list形式，如wb.publish_tool[0]为最新一条微博的发布工具，与wb.weibo_content[0]对应，其它用法同wb.weibo_content。

# 如何获取cookie
1.用Chrome打开<https://passport.weibo.cn/signin/login>；<br>
2.输入微博的用户名、密码，登录，如图所示：
![](https://picture.cognize.me/cognize/github/weibospider/cookie1.png)
登录成功后会跳转到<https://m.weibo.cn>;<br>
3.按F12键打开Chrome开发者工具,在地址栏输入并跳转到<https://weibo.cn>,跳转后会显示如下类似界面:
![](https://picture.cognize.me/cognize/github/weibospider/cookie2.png)
4.点击Chrome开发者工具“Name"列表中的"weibo.cn",点击"Headers"，其中"Request Headers"下，"Cookie"后的值即为我们要找的cookie值，复制即可，如图所示：
![](https://picture.cognize.me/cognize/github/weibospider/cookie3.png)

# 如何获取user_id
1.打开网址<https://weibo.cn>，搜索我们要找的人，如”迪丽热巴“，进入她的主页；<br>
![](https://picture.cognize.me/cognize/github/weibospider/user_home.png)
2.按照上图箭头所指，点击"资料"链接，跳转到用户资料页面；<br>
![](https://picture.cognize.me/cognize/github/weibospider/user_info.png)
如上图所示，迪丽热巴微博资料页的地址为"<https://weibo.cn/1669879400/info>"，其中的"1669879400"即为此微博的user_id。<br>
事实上，此微博的user_id也包含在用户主页(<https://weibo.cn/u/1669879400?f=search_0>)中，之所以我们还要点击主页中的"资料"来获取user_id，是因为很多用户的主页不是"<https://weibo.cn/user_id?f=search_0>"的形式，而是"<https://weibo.cn/个性域名?f=search_0>"或"<https://weibo.cn/微号?f=search_0>"的形式。其中"微号"和user_id都是一串数字，如果仅仅通过主页地址提取user_id，很容易将"微号"误认为user_id。

# 注意事项
1.user_id不能为爬虫微博的user_id。因为要爬微博信息，必须先登录到某个微博账号，此账号我们姑且称为爬虫微博。爬虫微博访问自己的页面和访问其他用户的页面，得到的网页格式不同，所以无法爬取自己的微博信息；<br>
2.cookie有期限限制，超过有效期需重新更新cookie。
