import asyncio
import random

from CookiesPool.generator import Getter
from CookeisLog.logger import ProxyLogger
from ConnDB.db_redis import RedisClient

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError


class Tester(object):
    # 首页认证
    # TEST_URL1 = 'https://m.weibo.cn/comments/hotflow?id=4315958677377740&mid=4315958677377740&max_id_type=0'
    # 翻页获取数据测试
    # TEST_URL2 = 'https://m.weibo.cn/comments/hotflow?id=4315958677377740&mid=4315958677377740&max_id=13854002826337244&max_id_type=0'
    # TEST_URL3 = 'https://m.weibo.cn/comments/hotflow?id=4315958677377740&mid=4315958677377740&max_id=156226683202&max_id_type=0'
    # TEST_URL4 = 'https://m.weibo.cn/comments/hotflow?id=4319937411346068&mid=4319937411346068&max_id=138145067263628&max_id_type=0'
    # 新浪微博测试url
    TEST_URL = 'https://m.weibo.cn/api/config'

    def __init__(self):
        """
        实例化
        :param total:池总数
        """
        self.redis = RedisClient()
        self.log = ProxyLogger().logger

    def test_single_cookies(self, cookies=None):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        import requests
        # 首页验证
        try:
            # allow_redirects=False不让请求跳转
            res = requests.get(self.TEST_URL, cookies=cookies, timeout=10, allow_redirects=False).json()
            print(res)
            if res['data']['login']:
                return True
            else:
                # self.redis.del_ip(str(cookies))
                # 重新获取cookies，这里是在mysql随机获取一组用户名和密码生成
                # self.redis.save(str(Getter().run()))
                return False
        except requests.exceptions.ConnectTimeout as e:
            self.log.error('请求超时！{}'.format(str(e.args)))
            return False
        except Exception as e:
            print('删除cookies2')
            # self.redis.del_ip(str(cookies))
            # self.redis.save(str(Getter().run()))
            return False

    def run(self, code):
        """
        测试主函数
        :return:
        """
        self.log.info('测试器开始运行!')
        try:
            count = self.redis.get_count()
        except:
            print(4)
            self.log.error('数据库连接错误！')
            return False
        self.log.info('当前剩余' + str(count) + '个cookies')
        mid_num = 5 - count
        # 测试池里不足5个
        if mid_num > 0:
            while mid_num:
                try:
                    result = Getter().run(code)
                    self.redis.save(key=list(result.keys())[0],value=list(result.values())[0])
                    self.log.info('cookies插入成功！')
                    mid_num -= 0
                except Exception as e:
                    self.log.error('cookies没有存入redis或获取cookies出错！' + str(e.args))
        try:
            # 获取所有的cookies
            all_cookies = self.redis.get_all()
            # self.log.info('池里的ip:' + ','.join(test_proxies))
            import json
            for cookies in all_cookies:
                cookies = json.loads(cookies)
                flag = self.test_single_cookies(cookies=cookies)
                if flag:
                    print('{}测试成功！'.format(str(cookies)))
                    self.log.info('{}测试成功！'.format(str(cookies)))
                    continue
                else:
                    # 从池里删除该cookies
                    self.redis.del_ip(str(cookies))
                    # 重新获取cookies，这里是在mysql随机获取一组用户名和密码生成
                    result = Getter().run(code)
                    self.redis.save(key=list(result.keys())[0], value=list(result.values())[0])
                    print(cookies)
                    # self.redis.del_ip(str(cookies))
            return True
        except Exception as e:
            self.log.error('测试器发生错误:' + str(e.args))
            return False


if __name__ == '__main__':
    Tester().run(code='sina')
