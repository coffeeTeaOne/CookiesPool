# encoding: utf-8
import os
import platform
from Env.ParseYaml import FileConfigParser


class PathLog(object):
    def sys(self):
        sysstr = platform.system()
        if sysstr == "Windows":
            return 'Windows'
        elif sysstr == "Linux":
            return 'Linux'
        elif sysstr == 'Darwin':
            return 'Linux'
        else:
            return 'Other System'

    def log_path(self):
        root_path = os.path.dirname(os.path.dirname(__file__))
        if self.sys() == 'Linux':
            log_path = FileConfigParser().get_path(server=self.sys(), key='log')
            return log_path
        if self.sys() == 'Windows':
            log_path = root_path + FileConfigParser().get_path(server=self.sys(), key='log')
            return log_path


if __name__ == '__main__':
    print(PathLog().log_path())