class Argument():

    def __init__(self):
        import argparse
        parser = argparse.ArgumentParser(prog='mydir.py',epilog='Example:\n mydir.py -u http://example.com')
        parser.add_argument('-u',dest='url', action='store',required=True,
                            help='target url')
        parser.add_argument('-th', dest='thread', type=int,
                            help='\nthe thread for connecting', default=5)
        parser.add_argument('-t',dest='timeout',type=int,
                            help='\nthe timeout for connecting to url',default=10)
        parser.add_argument('-e', dest="extention",
                            help="""\nSuffix name used for fuzzing. [Default: php]""", default="php")
        parser.add_argument("-o", dest="output",
                            help="\nOutput dir", default=None)
        parser.add_argument('-d',dest='dict', default='dict.txt')
        parser.add_argument('-s',dest='status',
                            help='output the status that you want',default='default')
        self.args = parser.parse_args()

    def get_argu(self, arg_name=None):
        try:
            if arg_name:
                return eval("self.args." + arg_name)
        except Exception as e:
            pass
        return None

    def init_url(self,url):
        url=url if url.find('://') != -1 else 'http://%s' % url
        if url[-1] !='/':
            url=url+'/'
        return url

    def convert_status(self,status='default'):
        status_list=[]
        if status=='default':
                    status_list=[200,201,202,203,204,205,206,300,301,302,302,304,305,306,307,
                         400,401,402,403,405,406,407,408,409,410,500,501,502,503,504,505]

        elif ',' in status:
            temp_list = status.split(",")
            for sp_status in temp_list:
                if "-" in sp_status:
                    for p in range(int(sp_status.split("-")[0]), int(sp_status.split("-")[1]) + 1):
                        status_list.append(p)
                else:
                    sp_status.append(sp_status)
        elif "-" in status:
            for p in range(int(status.split("-")[0]), int(status.split("-")[1]) + 1):
                status_list.append(p)
        else:
            status_list.append(status)

        return status_list
