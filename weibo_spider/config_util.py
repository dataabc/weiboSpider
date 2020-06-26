import codecs
import os
import sys
from datetime import datetime


def _is_date(date_str):
    """判断日期格式是否正确"""
    try:
        if ':' in date_str:
            datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        else:
            datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_config(config):
    """验证配置是否正确"""

    # 验证filter、pic_download、video_download
    argument_list = ["filter", "pic_download", "video_download"]
    for argument in argument_list:
        if config[argument] != 0 and config[argument] != 1:
            sys.exit(u"%s值应为0或1,请重新输入" % config[argument])

    # 验证since_date
    since_date = str(config["since_date"])
    if (not _is_date(since_date)) and (not since_date.isdigit()):
        sys.exit(u"since_date值应为yyyy-mm-dd形式或整数,请重新输入")

    # 验证end_date
    end_date = str(config["end_date"])
    if (not _is_date(end_date)) and (end_date != 'now'):
        sys.exit(u'end_date值应为yyyy-mm-dd形式或"now",请重新输入')

    # 验证write_mode
    write_mode = ["txt", "csv", "json", "mongo", "mysql"]
    if not isinstance(config["write_mode"], list):
        sys.exit(u"write_mode值应为list类型")
    for mode in config["write_mode"]:
        if mode not in write_mode:
            sys.exit(
                u"%s为无效模式，请从txt、csv、json、mongo和mysql中挑选一个或多个作为write_mode" %
                mode)

    # 验证user_id_list
    user_id_list = config["user_id_list"]
    if (not isinstance(user_id_list,
                       list)) and (not user_id_list.endswith(".txt")):
        sys.exit(u"user_id_list值应为list类型或txt文件路径")
    if not isinstance(user_id_list, list):
        if not os.path.isabs(user_id_list):
            user_id_list = (os.path.split(os.path.realpath(__file__))[0] +
                            os.sep + user_id_list)
        if not os.path.isfile(user_id_list):
            sys.exit(u"不存在%s文件" % user_id_list)


def get_user_config_list(file_name, default_since_date):
    """获取文件中的微博id信息"""
    with open(file_name, "rb") as f:
        try:
            lines = f.read().splitlines()
            lines = [line.decode("utf-8-sig") for line in lines]
        except UnicodeDecodeError:
            sys.exit(u"%s文件应为utf-8编码，请先将文件编码转为utf-8再运行程序" % file_name)
        user_config_list = []
        for line in lines:
            info = line.split(" ")
            if len(info) > 0 and info[0].isdigit():
                user_config = {}
                user_config["user_uri"] = info[0]
                if len(info) > 2 and _is_date(info[2]):
                    if len(info) > 3 and _is_date(info[2] + " " + info[3]):
                        user_config["since_date"] = info[2] + " " + info[3]
                    else:
                        user_config["since_date"] = info[2]
                else:
                    user_config["since_date"] = default_since_date
                if user_config not in user_config_list:
                    user_config_list.append(user_config)
    return user_config_list


def update_user_config_file(user_config_file_path, user_uri, nickname,
                            start_time):
    """更新用户配置文件"""
    with open(user_config_file_path, "rb") as f:
        lines = f.read().splitlines()
        lines = [line.decode("utf-8-sig") for line in lines]
        for i, line in enumerate(lines):
            info = line.split(" ")
            if len(info) > 0:
                if user_uri == info[0]:
                    if len(info) == 1:
                        info.append(nickname)
                        info.append(start_time)
                    if len(info) == 2:
                        info.append(start_time)
                    if len(info) > 3 and _is_date(info[2] + " " + info[3]):
                        del info[3]
                    if len(info) > 2:
                        info[2] = start_time
                    lines[i] = " ".join(info)
                    break
    with codecs.open(user_config_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
