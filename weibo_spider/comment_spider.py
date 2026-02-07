# 爬取某一篇微博的评论，保存到评论.csv文件中，需要用户主页下，每条微博的id 获取字段为data['statuses']['id']
import requests
import csv
import re

f = open('评论.csv', mode='a', encoding='utf-8-sig', newline='')
csv_write = csv.writer(f)
csv_write.writerow(['id', 'screen_name', 'text_raw', 'like_counts', 'total_number', 'created_at'])

# 爬取到用户信息后需要微博id 举个例子
id_ = '5087364530046999'
# 请求头
headers = {
    # 用户身份信息
    'cookie': 'WEIBOCN_FROM=1110006030; _T_WM=43533142690; MLOGIN=1; SCF=AmOv6sTYo8tm64SYk9cQ7IW3mBPM4eikzCKM-cACAJF4IQhJSndnC0gqWOc4UzLjmbaH1_D8DPRv9yVUh3I4pEw.; SUB=_2A25KDmmDDeRhGeVN6lEW8CrLyD2IHXVpYuNLrDV6PUJbktANLUzQkW1NTJq1agw77ehhYZHzmIv_UkQqfZxInPXV; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhObfqXWFqrr0fL7DHZMxPq5NHD95Q0e020S05XS0epWs4Dqcj-i--fiKy2iKnpi--Xi-zRiKn0dNQt; SSOLoginState=1728715219; ALF=1731307219; XSRF-TOKEN=10536b; M_WEIBOCN_PARAMS=lfid%3D5088422838404723%26luicode%3D20000174',
    # 防盗链
    'referer': 'https://m.weibo.cn/detail/'+id_,
    # 浏览器基本信息
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}
# 下列函数抓取的版本为微博用户主页微博进入详情页
#  从其他地方进入的微博详情爬取评论需要使用另一种方式（url和具体字段不完全相同）,详情见get_next_other
def get_next(next='', n=50):
    # 用n控制递归次数，每滚动一次获得的页面中max_id与上一次获得中的max_id相同，首次获得的页面中参数为空,后续替换为max_id
    url = f'https://m.weibo.cn/comments/hotflow?id={id_}&mid={id_}{next}&max_id_type=0'
    response = requests.get(url=url, headers=headers)
    json_data = response.json()

    data_list = json_data['data']['data']
    max_id = json_data['data']['max_id']
    for data in data_list:
        id = data['user']['id']  # 评论用户id
        screen_name = data['user']['screen_name']  # 用户名字
        source = data['source'][2:]  # ip属地
        text = data['text']  # 评论内容（html格式），需要进行进一步处理排除表情格式；若使用第二种方式则可以直接获取text_raw对应内容

        text_raw = re.sub(r"<span class=\"url-icon\">.*?alt=", "", text)
        text_raw = re.sub(r" src=.*?span>", "", text_raw)
        like_counts = data['like_count']  # 点赞数
        floor_number = data['floor_number']  # 盖楼数
        created_at = data['created_at']  # 发布时间
        print(id, screen_name, source, text_raw, like_counts, floor_number, created_at)

        csv_write.writerow([id, screen_name, source, text_raw, like_counts, floor_number, created_at])
    if max_id == 0:  # 评论无法滚动时获取的最后一个页面的max_id为0
        n = 0
    max_str = '&max_id=' + str(max_id)
    if n < 0:
        return
    get_next(max_str , n-1)


# 这种url触发方式咱不得知，改一下请求头中的url即可comment_spider.py
def get_next_other(next='count=10', n=50):
    url = f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=5088449407484921&is_show_bulletin=2&is_mix=0&{next}&uid=7888222767&fetch_level=0&locale=zh-CN'
    response = requests.get(url=url, headers=headers)
    json_data = response.json()

    data_list = json_data['data']
    max_id = json_data['max_id']
    for data in data_list:
        id = data['user']['id']  # 评论用户id
        screen_name = data['user']['screen_name']  # 用户名字
        source = data['source'][2:]  # ip属地
        text_raw = data['text_raw']  # 评论内容
        like_counts = data['like_counts']  # 点赞数
        floor_number = data['floor_number']  # 盖楼数
        created_at = data['created_at']  # 发布时间

        print(id, screen_name, source, text_raw, like_counts, floor_number, created_at)

        csv_write.writerow([id, screen_name, source, text_raw, like_counts, floor_number, created_at])
    if max_id == 0:  # 评论无法滚动时获取的最后一个页面的max_id为0
        n = 0
    max_str = '&max_id=' + str(max_id)
    if n < 0:
        return
    get_next_other(max_str , n-1)

get_next()