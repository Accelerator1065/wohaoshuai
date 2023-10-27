import requests,threading,sys,colorama,changanya,time
from .io.arg_parse import Argument
from .io.output import diroutput
from changanya.simhash import Simhash
from colorama import Fore, Style
class controller():
    hearder={
        'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
        'Accept-Language': 'Zh-CN, zh;q=0.8, en-gb;q=0.8, en-us;q=0.8',
        'Accept-Encoding': 'identity',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }
    proxies = {
        "http": None,
        "https": None,
    }
    def __init__(self,args=None):
        self.argu=args
        self.url=Argument().init_url(self.argu.get_argu("url"))
        self.thread=self.argu.get_argu("thread")
        self.timeout=self.argu.get_argu("timeout")
        self.status = self.argu.get_argu("status")
        self.dict=self.argu.get_argu("dict")
        self.sta_list = Argument().convert_status(status=self.status)
        self.output=diroutput()
        self.TASK_STOP=False
        self.wrong_status=[404,500,501,502,503,504,505]
        #self.stop_flag=False

    def __init__404_page(self):
        _404_page=requests.get(self.url+'whoami',headers=self.hearder,proxies=self.proxies,allow_redirects=False)
        return _404_page.content

    def is_similar_page(self,text1, text2, radio=0.85):
        simhash1 = Simhash(text1.decode('utf-8'))
        simhash2 = Simhash(text2.decode('utf-8'))

        calc_radio = simhash1.similarity(simhash2)
        # print("两个页面的相似度为:%s" % calc_radio)
        if calc_radio >= radio:
            return True
        else:
            return False

    def open_dict(self):
        dict_list=[]
        dict='dict/'+self.dict
        try:
            with open(dict, 'r') as f:
                for each in f:
                    each = each.replace('\n', '')
                    dict_list.append(each)
                f.close()
            return dict_list
        except:
            print("打开字典失败！")

    def require(self,location,dict_num,dict_list,_404_page):
        real_url=self.url+dict_list[location]
        try:
            response=requests.get(real_url,headers=self.hearder,proxies=self.proxies,timeout=self.timeout)
            if (response.status_code!=404 & self.is_similar_page(response.content,_404_page)==False):
               if response.status_code in self.sta_list:
                  self.color = self.output.wordcolor(response.status_code)
                  self.content='[+]'+str(response.status_code)+' '+real_url+'=>'+response.url
                  self.output.print_message(self.color+self.content+ Style.RESET_ALL)
                  # self.output.print_proccess(dict_num,dict_proccess)
                  #self.output.print_pro(location,dict_num)
        except requests.exceptions.ConnectTimeout:
            pass

    def __start(self,dict_list,dict_num,per_th_num,i,_404_page):
           try:
               for j in range(per_th_num):
                   location=i*per_th_num+j
                   if location <= (dict_num-1):
                      self.require(location,dict_num,dict_list,_404_page)
           except KeyboardInterrupt:
               print("Aborted by userbbb!")
               sys.exit()
           except Exception as e:
               print("Fatal error occurs!")
               raise e


    def start(self):
        connect_url=requests.get(url=self.url,headers=self.hearder,proxies=self.proxies,timeout=self.timeout)
        self.output.print_start(self.url)
        if connect_url.status_code in self.wrong_status:
            print('content to url wrong')
            sys.exit()
        _404_page=self.__init__404_page()
        thread_list = []
        dict_list=self.open_dict()
        dict_num=len(dict_list)
        per_th_num=int(dict_num/self.thread)+1
        for i in range(self.thread):
            t = threading.Thread(target=self.__start,args=(dict_list,dict_num,per_th_num,i,_404_page))
            thread_list.append(t)
            t.start()

        while True:
            if threading.activeCount() <= 1:
                break
            else:
                try:
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    print("Aborted by user!")
                    sys.exit(0)

        self.output.print_end()