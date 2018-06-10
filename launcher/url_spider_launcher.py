import sys
import platform

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

from scheduler.linear_url_scheduler import LinearUrlScheduler

python_command = 'C:\Python35\python.exe'
script_name = 'D:/Projects/news-spider/launcher/launch_once/launch_url_ppl.py'
spider_names = ['SohuAnimationSpider', 'SohuEntertainmentSpider', 'SohuFashionSpider', 'SohuFinanceSpider',
                'SohuGameSpider', 'SohuInternationalSpider', 'SohuMilitarySpider', 'SohuPoliticsSpider',
                'SohuSportSpider', 'SohuTechnologySpider',
                'SinaHomeSpider', 'TencentModuleSpider', 'TencentHomeSpider']
log_path = 'D:/Projects/news-spider/logs/URL1.log'

lrs = LinearUrlScheduler(spider_names, python_command, script_name, log_path, 12 * 3600)
lrs.launch()