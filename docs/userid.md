## 如何获取user_id
1.打开网址<https://weibo.cn>，搜索我们要找的人，如"迪丽热巴"，进入她的主页；<br>
![](https://picture.cognize.me/cognize/github/weibospider/user_home.png)
2.按照上图箭头所指，点击"资料"链接，跳转到用户资料页面；<br>
![](https://picture.cognize.me/cognize/github/weibospider/user_info.png)
如上图所示，迪丽热巴微博资料页的地址为"<https://weibo.cn/1669879400/info>"，其中的"1669879400"即为此微博的user_id。<br>
事实上，此微博的user_id也包含在用户主页(<https://weibo.cn/u/1669879400?f=search_0>)中，之所以我们还要点击主页中的"资料"来获取user_id，是因为很多用户的主页不是"<https://weibo.cn/user_id?f=search_0>"的形式，而是"<https://weibo.cn/个性域名?f=search_0>"或"<https://weibo.cn/微号?f=search_0>"的形式。其中"微号"和user_id都是一串数字，如果仅仅通过主页地址提取user_id，很容易将"微号"误认为user_id。<br>
上述可以获得一个user_id，如果想要获得**大量**微博，见[如何获取大量user_id](#如何获取大量user_id)部分。<br>

## 如何获取大量user_id
[如何获取user_id](#如何获取user_id)部分可以获得一个user_id，<https://github.com/dataabc/weibo-follow>可以利用这一个user_id，获取该user_id微博用户关注人的user_id，一个user_id最多可以获得200个user_id，并写入user_id_list.txt文件。程序支持读文件，利用这200个user_id，可以获得最多200X200=40000个user_id。再利用这40000个user_id可以得到40000X200=8000000个user_id，如此反复，以此类推，可以获得大量user_id。本项目也支持读文件，将上述程序的结果文件user_id_list.txt路径赋值给本项目config.json的user_id_list参数，就可以获得这些user_id用户所发布的大量微博。<br>