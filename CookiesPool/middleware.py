
"""
处理读取mysql数据配置信息，生成midd数组，用于后面解析
"""
import random

from ConnDB.db_mysql import Op_Mysql
from ConnDB.db_redis import RedisClient
from CookeisLog.logger import ProxyLogger


class MiddlewareCookies(object):
    def __init__(self, code='sina'):
        self.code = code
        self.log = ProxyLogger().logger

    def midd(self):
        """
        解析mysql配置信息
        :return:
        """
        try:
            datas = Op_Mysql().Select_Query(tablename='spi_auto_login', output=['ACCOUNTS_', 'URL_', 'SCRIPT_'],
                                           where='CODE_="%s"' % self.code)[0]
        except:
            self.log.error('mysql数据库连接错误！')
            return False
        middle = {}
        user_dict = {}
        try:
            users = eval(datas[0])
            for u in users:
                new_data = list(u.values())
                user_dict[new_data[0]] = new_data[1]
            # 登录的url
            url = datas[1]
            middle['url'] = url
            config = eval(datas[2])
            for k, v in user_dict.items():
                all_user = RedisClient().get_values()
                # 判断该微博账号是否在redis里面存在
                if k in all_user:
                    continue
                else:
                    # config加入用户名
                    config[0]['value'] = k
                    # config加入密码
                    config[1]['value'] = v
                    break
        except Exception as e:
            self.log.error('中间件数据解析错误！')
            return False
        # xpath，username，password
        middle['config'] = config
        return middle


if __name__ == '__main__':
    MiddlewareCookies().midd()