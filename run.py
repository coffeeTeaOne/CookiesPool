
import sys
import io
import time

from ConnDB.db_mysql import Op_Mysql
from CookiesPool.tester import Tester
from CookeisLog.logger import ProxyLogger

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

log = ProxyLogger().logger
code = 'sina'


def main():
    log.info('开始运行---')
    print('开始运行')
    # max_num = sys.argv[1]
    try:
        flag = Tester().run(code)
        print('测试完成！')
        if flag:
            print(0)
            log.info('success')
        else:
            print(9)
            log.error('failed')
    except Exception as e:
        print(5)
        log.error(e.args)


if __name__ == '__main__':
    main()
