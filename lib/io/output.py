import colorama
from colorama import Fore,Style
import sys,os

class diroutput():

    def __init__(self):
        colorama.init()
        self.save=None
        self.terminal_size = self.__get_terminal_size()

    def __get_terminal_size(self):
        try:
            columns = os.get_terminal_size().columns
        except Exception:
            columns = 100
        return columns

    def wordcolor(self,status):
        if status == 200:
            color = Fore.LIGHTGREEN_EX
        elif status == 404:
            color = Fore.RED
        elif status in [301, 302, 307]:
            color = Fore.LIGHTYELLOW_EX
        else:
            color = Fore.CYAN
        return color

    def print_message(self, message,nowrap=False):
        sys.stdout.write(message)
        sys.stdout.flush()

        if not nowrap:
            sys.stdout.write('\n')

    def print_pro(self,now,max):
        precent=str(format((now/max)*100,'.2f'))
        print('此进度：'+precent+'%'+str(now)+'/'+str(max))


    def print_banner(self):
        sys.stdout.write(Fore.LIGHTMAGENTA_EX + r"""
         __  __  __     __  _____    _____   _____
         |  \/  | \ \   / / |  __ \  |_   _| |  __ \
         | \  / |  \ \_/ /  | |  | |   | |   | |__) |
         | |\/| |   \   /   | |  | |   | |   |  _  /
         | |  | |    | |    | |__| |  _| |_  | | \ \
         |_|  |_|    |_|    |_____/  |_____| |_|  \_\ v_1.0
         """ + Style.RESET_ALL)
        sys.stdout.write('\n')

    def print_start(self,url):
        urlmessage='[~]target url: '+url
        sys.stdout.write(Fore.LIGHTMAGENTA_EX+urlmessage+'\n'+Style.RESET_ALL)

    def print_proccess(self,process,max):
        present=process/max*100
        string=Fore.LIGHTYELLOW_EX +'['+'#'* int(present/5)+' '*(20-int(present/5))+']'+process+'/'+max
        newstring = (string + Style.RESET_ALL)
        sys.stdout.write(newstring)
        sys.stdout.flush()

    def print_end(self):
        print(Fore.LIGHTGREEN_EX + '---------completed----------' + Style.RESET_ALL)