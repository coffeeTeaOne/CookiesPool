import random
import time
from io import BytesIO

import requests
from PIL import Image
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
from os.path import abspath, dirname
from selenium import webdriver

from ConnDB.db_mysql import Op_Mysql
from CookeisLog.logger import ProxyLogger
from CookiesPool.middleware import MiddlewareCookies

TEMPLATES_FOLDER = dirname(abspath(__file__)) + '/templates/'


class WeiboCookies():
    def __init__(self, code, browser):
        # self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/'
        # self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/'
        self.browser = browser
        self.wait = WebDriverWait(self.browser, 20)
        self.code = code
        self.log = ProxyLogger().logger

    def __del__(self):
        self.close_windows()
    
    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        try:
            midd = MiddlewareCookies(self.code).midd()
        except:
            self.log.error('mysql数据库连接错误！')
            return False
        try:
            if midd:
                url = midd['url']
                un = midd['config'][0]['value']
                u_xpath = midd['config'][0]['xpath']
                pwd = midd['config'][1]['value']
                p_xpath = midd['config'][1]['xpath']
                login_xpath = midd['config'][2]['xpath']
            else:
                self.log.error('中间件读取配置信息错误！')
                return False
        except:
            self.log.error('中间件解析错误！')
            return False
        self.browser.delete_all_cookies()
        self.browser.get(url)
        # username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        username = self.wait.until(EC.presence_of_element_located((By.XPATH, u_xpath)))
        # password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        password = self.wait.until(EC.presence_of_element_located((By.XPATH, p_xpath)))
        # submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, login_xpath)))

        username.send_keys(un)
        password.send_keys(pwd)
        time.sleep(1)
        submit.click()
        return un

    def password_error(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            return WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.ID, 'errorMsg'), '用户名或密码错误'))
        except TimeoutException:
            return False
    
    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'lite-iconf-profile'))))
        except TimeoutException:
            return False
    
    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.browser.get_cookies()

    def close_windows(self):
        """
        关闭
        :return:
        """
        try:
            self.log.info('关闭窗口异常！')
            self.browser.quit()
            del self.browser
        except TypeError:
            self.log.info('关闭窗口异常！')
            # print('关闭窗口异常！')

    def main(self):
        """
        破解入口
        :return:
        """
        user = self.open()
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
        # 如果不需要验证码直接登录成功
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies,
                'username': user
            }
        else:
            return {
                'status': 3,
                'content': '登录失败',
                'username': user
            }


if __name__ == '__main__':
    # browser = webdriver.Chrome()
    browser = webdriver.PhantomJS()

    # browser = WebDriver(executable_path=r'C:\Users\lyial\Desktop\coffee\venv\SpiderVenv\phantomjs-2.1.1-windows\bin\phantomjs',
    #           port=5001)
    result = WeiboCookies('sina', browser).main()
    print(result)




