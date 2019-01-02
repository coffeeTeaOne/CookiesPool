# encoding: utf-8
import os
import yaml


class DBConfigParser(object):

    config_file = os.path.dirname(os.path.realpath(__file__)) + '/EnvConfig/dbconfig.yaml'
    configs = yaml.load(open(config_file,'r'))

    @classmethod
    def get_config(cls, server,key=None):
        if server == 'mysql':
            server = 'mysql.config'
        if server == 'redis_weibo_cookies':
            server = 'redis.weibo.cookies'
        if server == 'redis_weibo_cookies_colony':
            server = 'redis.weibo.cookies.colony'
        section = cls.configs.get(server, None)
        if section is None:
            raise NotImplementedError
        value = section.get(key, None)
        if value is None:
                raise NotImplementedError
        dbconfig = {}
        for v in value.split(' '):
            na = v.split(':')[0]
            va = v.split(':')[1]
            if na == 'port':
                va = int(va)
            dbconfig[na] = va
        return dbconfig


class FileConfigParser(object):

    config_file = os.path.dirname(os.path.realpath(__file__)) + '/EnvConfig/filepathconfig.yaml'
    configs = yaml.load(open(config_file, 'r'))

    @classmethod
    def get_config(cls, server, key=None):
        section = cls.configs.get(server, None)
        if section is None:
            raise NotImplementedError
        value = section.get(key, None)
        if value is None:
            raise NotImplementedError
        fileconfig = {}
        for v in value.split(' '):
            na = v.split(':')[0]
            va = v.split(':')[1]
            if na == 'port':
                va = int(va)
            fileconfig[na] = va
        return fileconfig

    @classmethod
    def get_path(cls,server,key):
        config = cls.get_config(server=server, key=key)
        return config['path']

# if __name__ == '__main__':
#     mysql_conn = DBConfigParser().get_config(server='redis', key='localhostconn')
#     print(mysql_conn['host'])
