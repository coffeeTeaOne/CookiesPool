# encoding: utf-8
from Env.ParseYaml import DBConfigParser
import pymysql
import traceback

from CookeisLog.logger import ProxyLogger


class Static_Config:

    def __init__(self,host=None,port=None,user=None,password=None,dbanme=None):
        if host is None and port is None and user is None and password is None and dbanme is None:
            # self.config = DBConfigParser().get_config(server='mysql', key='43conn')
            self.config = DBConfigParser().get_config(server='mysql', key='localhostconn')
            # self.config = DBConfigParser().get_config(server='mysql', key='222conn')
            # self.config = DBConfigParser().get_config(server='mysql', key='41conn')
            # self.config = DBConfigParser().get_config(server='mysql', key='41conn_test')
            # self.config = DBConfigParser().get_config(server='mysql', key='67.25conn')
            self.config['cursorclass'] = pymysql.cursors.DictCursor
        else:
            self.config = {
                'host': host,
                'port': port,
                'user': user,
                'password': password,
                'db': dbanme,
                'charset': 'utf8',
                'cursorclass': pymysql.cursors.DictCursor,
            }

        self.log = ProxyLogger().logger


class Op_Mysql(Static_Config):
    # 返回可用于multiple rows的sql拼装值
    def multipleRows(self, params):
        """
        将sql列的数据信息处理为标准格式:(‘值1’，‘值2’，)
        insert into tablename (列1，列2，）values (‘值1’，‘值2’，)
        :param params: 任意格式的params（需存储数据）
        :return:
        """
        ret = []
        # 根据不同值类型分别进行sql语法拼装
        for param in params:
            if isinstance(param, (int,  float, bool)):
                ret.append(str(param))
            elif isinstance(param, (str, 'utf-8')):
                param = param.replace('"','\\"')
                ret.append('"' + param + '"')
            else:
                print('unsupport value: %s ' % param)
        return '(' + ','.join(ret) + ')'

    def Insert_Query(self, tablename, column, datas):
        """
        插入数据
        :param tablename: 表名
        :param column:   列名，数据项（list，str）
        :param datas:    列对应的数据信息list（调用multipleRows这个函数处理为标准格式:'("值1","值2","值3")'
        :return:
        """
        try:
            # 创建连接
            connection = pymysql.connect(**self.config)
        except pymysql.err.OperationalError as e:
            # 单独捕捉这个错误出来
            self.log.error('pymysql.err.OperationalError:%s' % str(e))
            raise e
        except Exception as e:
            self.log.error(e)
            raise e
        count = 0
        try:
            # with打开的连接不需要关闭
            with connection.cursor() as cursor:
                # column有多少个元素‘%s’就生成多少个
                v = ','.join(["%s" for _ in range(len(column))])
                if isinstance(column, list):
                     column = ','.join(column)  # 生成‘a,b,c,d'这样格式
                try:
                    if len(datas) == 1:
                        # 插入一个数据项
                        query_sql = 'INSERT INTO ' + tablename + '(' + column + ') VALUES%s' % self.multipleRows(datas[0])
                        cursor.execute(query_sql)
                    else:
                        # 插入多个数据项，这里的v表示(%s,%s,%s,%s,%s)
                        query_sql = 'INSERT INTO ' + tablename + '(' + column + ') VALUE(' + v + ')'
                        # datas模板字符串的参数，是一个列表，列表中的每一个元素必须是元组！！！
                        # 例如：  [(1,'小明'),(2,'zeke'),(3,'琦琦'),(4,'韩梅梅')]
                        cursor.executemany(query_sql, datas)
                    # 插入次数
                    count = count + 1
                    # 提交
                    connection.commit()
                except pymysql.err.IntegrityError as e:
                       self.log.info(e)
                       self.log.info(datas)
                       # errorcode = eval(str(e))[0]
                       # if errorcode == 1062:
                       #     print('主键重复')
                       pass
                except Exception as e:
                    # 定位错误在哪里
                    traceback.print_exc()
                    #print(e,datas)
                    # 回滚处理
                    connection.rollback()
                     #print('需要特殊处理','INSERT INTO %s(%s) VALUES (%s)',datas)
                finally:
                    # 关闭（双保险）
                    connection.close()
        finally:
            # 关闭（双保险）
            connection.close()
        # print('本次共插入%d条' % count)

    def Select_Query(self, tablename, output=None, where='1=1', dict_=False):
        """
        查询数据
        :param tablename: 表名str
        :param output: 输出数据项list（查询后的数据列）
        :param where: 查询条件str
        :param dict_: 布尔类型的的值，True直接输出
        :return:
        """
        try:
            connection = pymysql.connect(**self.config)
        except pymysql.err.OperationalError as e:
            self.log.error('pymysql.err.OperationalError:%s' % str(e))
            raise e
        except Exception as e:
            self.log.error(e)
            raise e

        try:
            with connection.cursor() as cursor:
                outputlist = []
                if not output:
                    # 查询所有数据项
                    sql = 'select * from %s where %s' % (tablename, where)
                if isinstance(output, list):
                    # 查询output指定列数据项，output是list
                    sql = 'select %s from %s where %s' % (','.join(output), tablename, where)
                if isinstance(output, str):
                    # 查询output指定列数据项，output是str
                    sql = 'select %s from %s where %s' % (output, tablename, where)
                cursor.execute(sql)
                # 获取结果，这里的result是一个多重括号
                result = cursor.fetchall()

                if dict_:
                    return result

                if result is None or isinstance(result, tuple):
                    return None
                # 处理result，将其处理为outputlist列表
                for res_ in result:
                    r = []
                    if isinstance(output, list):
                        for item in output:
                            r.append(res_[item])
                        outputlist.append(r)
                    if isinstance(output, str):
                        outputlist.append(res_[output])
                # 没有output直接输出result
                if not output:
                    outputlist = result

                # if len(outputlist)==1 and isinstance(outputlist[0],str):
                #     return outputlist[0]
                # else:
                return outputlist
        finally:
            # 关闭
            connection.close()
