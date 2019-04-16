import file_handler
import ui
from url_finder import UrlCollecter
import multiprocessing
import time
from collections import defaultdict
import zmq

class Controller():

    DEFAULT_TIME_OUT = 300
    SERVER_PORT = 45454

    def __init__(self,site_list_in_excel):
        self.workers = defaultdict(tuple)
        self.url_list_in_each_site = dict()
        self.site_list = site_list_in_excel
        self.server_ports = list()

    def start(self):
        ui.show_selection(self.site_list)
        ui.continue_question()
        start_or_not = ui.get_input()
        if start_or_not == 'y':
            self.bar = ui.ProgressBar()
            self.do_jobs()
        elif start_or_not == 'n':
            return
        else:
            ui.wrong_input()
    
    def do_jobs(self):
        self.publish_job()
        gathering_pipe,subscriber_pipe = multiprocessing.Pipe()
        subcribe_process = multiprocessing.Process(target=self.subcribe_job,args=(self.server_ports,subscriber_pipe))
        subcribe_process.start()
        start_time = time.time()
        while True:
            now = time.time()
            if now - start_time > Controller.DEFAULT_TIME_OUT:
                gathering_pipe.send('stop')
                message_from_subcriber = gathering_pipe.recv()
                for message in message_from_subcriber:
                    main_domain,url_list = message
                    self.url_list_in_each_site[main_domain] = url_list
                self.bar.update(100)
                self.finish_prosess(subcribe_process)
            else:
                now - start_time
                gathering_pipe.send('keep going')
                message_from_subcriber = gathering_pipe.recv()
                self.bar.update(message_from_subcriber)

    def publish_job(self):
        self.server_ports = list(range(self.SERVER_PORT,self.SERVER_PORT+len(self.site_list)))
        for site,port in zip(self.site_list,self.server_ports):
            process = multiprocessing.Process(target=UrlCollecter.run,args=(site,port))
            process.start()
            self.workers[site] = process

    def subcribe_job(self,server_ports,message_pipe):
        subscriber_socket_list = list()
        for port in server_ports:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://127.0.0.1:%d" %(port))
            subscriber_socket_list.append(socket)
        while True:
            def progress_jobs(socket):
                socket.send_string("keep going")
                return socket.recv_string()
            def finish_jobs(socket):
                socket.send_string("stop")
                return socket.recv_pyobj()
            continue_or_not = message_pipe.recv()
            if continue_or_not == 'stop':
                message_pipe.send(list(map(finish_jobs,subscriber_socket_list)))
                return
            else:
                progress_check_set = set(map(progress_jobs,subscriber_socket_list))
                if len(progress_check_set) == 3:
                    message_pipe.send(0.2)

    def finish_prosess(self,subcribe_process):
        subcribe_process.join()
        subcribe_process.terminate()
        for process in self.workers.values():
            process.join()
            process.terminate()
        self.make_sitemap_file()

    def make_sitemap_file(self):
        maker = file_handler.SitemapMaker(self.url_list_in_each_site)
        maker.make_file()
        ui.done()
        
if __name__=='__main__':
    site_list_in_excel = file_handler.read_excel_line()
    controller = Controller(site_list_in_excel)
    controller.start()

