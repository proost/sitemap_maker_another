import file_handler
import ui
from url_finder import UrlCollecter
import multiprocessing
import time
from collections import defaultdict

class Controller():

    DEFAULT_TIME_OUT = 600
    TIMEOUT_CONFIG = True

    def __init__(self,site_list_in_excel):
        self.workers = defaultdict(tuple)
        self.url_list_in_each_site_dict = dict()
        self.site_list = site_list_in_excel
        self.ports = list(range(6770,6770+len(self.site_list)))
        self.socket_list = list()

    def start(self):
        ui.show_selection(self.site_list)
        ui.continue_question()
        start_or_not = ui.get_input()
        if start_or_not == 'y':
            self.setup_workers()
        elif start_or_not == 'n':
            return
        else:
            ui.wrong_input()

    def setup_workers(self):
        self.temp_file_manager = file_handler.TempFileManager(self.site_list)
        for site,port in zip(self.site_list,self.ports):
            collector = UrlCollecter(site,port)
            process = multiprocessing.Process(target=collector.run)
            process.start()
            self.workers[site] = (collector,process)
        self.listen_progress()

    def listen_progress(self):
        self.start_time = time.time()
        while True:
            if self.TIMEOUT_CONFIG == True:
                now = time.time()
                if now - self.start_time > self.DEFAULT_TIME_OUT:
                    self.finish_progress()
                    return 
            self.check_dump()

    def check_dump(self):
        for collector,process in self.workers.values():
            if len(collector.temporary_url_list) > 100:
                self.temp_file_manager.dump_temporary_url_list(collector.main_domain,collector.temporary_url_list)
                collector.temporary_url_list.clear()

    def finish_progress(self):
        for collector,process in self.workers.values():
            collector.stop_flag = True
            temporary_url_list = self.temp_file_manager.load_temporary_url_list(collector.main_domain)
            url_list_in_each_site = collector.url_list_in_each_site + temporary_url_list
            self.url_list_in_each_site_dict[collector.main_domain] = list(set(url_list_in_each_site))
            process.terminate()
        print('크롤링이 끝났습니다.')
        self.make_sitemap_file()

    def make_sitemap_file(self):
        maker = file_handler.SitemapMaker(self.url_list_in_each_site_dict)
        maker.make_file()
        self.temp_file_manager.remove_temp_files()
        print('사이트맵 파일을 생성하였습니다.')
        
if __name__=='__main__':
    site_list_in_excel = file_handler.read_excel_line()
    controller = Controller(site_list_in_excel)
    controller.start()

