import urllib
import re
import time
import redis

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'}

job_redis = redis.Redis(host='192.168.10.242') # host为主机的IP，port和db为默认值


class Clawer(object):

    identity = 'master'  # 或slaver

    def __init__(self):
        if self.identity == 'master':
            for i in range(10):  # 将需爬取的糗事百科前20页的url并存入urls集合
                url = 'http://www.qiushibaike.com/hot/page/%d/' % i
                job_redis.sadd('urls', url)
        self.main()

    def get_content(self):
        """
        从糗事百科中获取故事
        :return: 故事列表
        """
        stories = []
        content_pattern = re.compile('<div class="content">([\w\W]*?)</div>([\w\W]*?)class="stats"') # 匹配故事内容（第一空）和是否含有图片（第二空）的模板
        pattern = re.compile('<.*?>') # 匹配包括括号及括号内无关内容的模板
        url = job_redis.spop('urls')
        while url: # 当数据库还存在网页url，取出一个并爬取
            try:
                #request = urllib.request.Request(url, headers=headers)
                #response = urllib.request.urlopen(request)
                print(url)
            except urllib.error.URLError as e: # 若出现网页读取错误捕获并输出
                #if hasattr(e, "reason"):
                #    print(e.reason)
                pass
            url = job_redis.spop('urls')
            time.sleep(3)

        return stories

    def main(self):
        self.get_content()

if __name__ == '__main__':
    Clawer()