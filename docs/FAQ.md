## 常见问题

### 程序运行出错，错误提示中包含“'NoneType' object”字样，如何解决？
这是最常见的问题之一。出错原因是爬取速度太快，被暂时限制了。限制可能包含爬虫账号限制和ip限制。一般情况下，一段时间后限制会自动解除。可通过降低爬取速度避免被限制，具体修改weibo_spider.py文件中get_weibo_info方法的如下代码：
```
                    if (page - page1) % random_pages == 0 and page < page_num:
                        sleep(random.randint(6, 10))
                        page1 = page
                        random_pages = random.randint(1, 5)
```
上面的意思是每爬取1到5页，随机等待6到10秒。可以通过加快暂停频率（减小random_pages值）或增加等待时间（加大sleep内的值）避免被限制。
如果你设置了只爬取用户信息（不爬用户的微博），则需修改weibo_spider.py文件中的start方法，原来的代码是这样的：
```
            for user_config in self.user_config_list:
                ......
```
修改后的代码是这样的：
```
            user_count = 0
            user_count1 = random.randint(1, 5)
            random_users = random.randint(1, 5)
            for user_config in self.user_config_list:
                if (user_count - user_count1) % random_users == 0:
                    sleep(random.randint(6, 10))
                    user_count1 = user_count
                    random_users = random.randint(1, 5)
                user_count += 1
                ......
```
上面的意思是每爬1到5个用户，随机等待6到10秒，你可以根据实际情况，修改代码中的数字。
