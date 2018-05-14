import sys
import platform
import os
import time

if __name__ == '__main__':
    # import模块必备
    def add_proj_path_to_syspath():
        sp = get_spliter()
        proj_path = sp.join(sys.path[0].split(sp)[0:-1])
        sys.path.append(proj_path)
        print('add project path: ' + proj_path + ' to system path')

    def get_spliter():
        if platform.system() == "Windows":
            return '\\'
        else:
            return '/'

    add_proj_path_to_syspath()

class LinearUrlScheduler(object):

    def __init__(self, spider_names, python_command, script_name, log_path):
        self.spider_names = spider_names
        self.python_command = python_command
        self.script_name = script_name
        self.log_path = log_path

    def launch(self):
        while (True):
            for i in range(len(self.spider_names)):
                command = self.python_command + ' ' + self.script_name + ' ' + self.spider_names[i] + ' ' + self.log_path
                print("launching spider: " + command)
                try:
                    process = os.popen(command)
                    output = process.read()
                    process.close()
                    print(output)
                except Exception as e:
                    print(e)
                time.sleep(6)