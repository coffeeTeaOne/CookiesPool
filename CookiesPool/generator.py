from CookiesPool.get_cookies import WeiboCookies
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver

from CookiesPool.middleware import MiddlewareCookies


class Getter(object):
    BROWSER_TYPE = 'Chrome'
    # BROWSER_TYPE = 'PhantomJS'

    def __init__(self):
        # self.username = username
        # self.password = password
        self.init_browser()
        # 中间件生成用户名，密码，xpath，测试url
        self.midd = MiddlewareCookies()

    def init_browser(self):
        """
        通过browser参数初始化全局浏览器供模拟登录使用
        :return:
        """
        if self.BROWSER_TYPE == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps[
                "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            # self.browser = webdriver.PhantomJS()
            self.browser.set_window_size(1400, 500)
        elif self.BROWSER_TYPE == 'Chrome':
            self.browser = webdriver.Chrome()

    def process_cookies(self, res):
        """
        生成cookies
        :param res:
        :return:
        """
        dicts = {}
        cookies_dict = {}
        if res.get('status') == 1:
            cookie = res.get('content')
            for cookie in cookie:
                dicts[cookie['name']] = cookie['value']
            # return dicts
            cookies_dict['SUB'] = dicts['SUB']
            return cookies_dict
        else:
            return None

    def run(self, code):
        """
        获取cookies入口
        :return:
        """
        # 解析self.midd中间件的配置信息解析出来，生成用户名，密码，xpath，测试url，
        # res = WeiboCookies('uanpingha@sina.com', 'buckle1094', self.browser).main()
        res = WeiboCookies(code, self.browser).main()
        cookies = self.process_cookies(res)
        username = res.get('username')
        if cookies and username:
            return {
                str(cookies): username
            }
        else:
            return None


if __name__ == '__main__':
    print(Getter().run(code='sina'))