import time
import os
import os.path
import sys

from nwebclient import base as b

class Process(b.Base):
    name = 'process'
    cpu = None
    def __init__(self, name='Process'):
        self.name = name
    def tick(self):
        pass
    def configure(self, arg):
        pass
    def cmd(self, args):
        return False

class CmdEcho(Process):
    """
       nwebclient.ticker.CmdEcho
    """
    def __init__(self):
        super().__init__('CmdEcho')
    def cmd(self, args):
        print("CMD: " + ' '.join(args))
        return False

class Ticker(Process):
    last = 0
    interval = 10
    fn = None
    def __init__(self, name = 'ticker', interval = 15, fn = None):
        super().__init__(name) 
        self.interval = interval
        self.fn = fn
    def tick(self):
        t = int(time.time())
        dur = t - self.last;
        if dur > self.interval:
            self.last = t
            self.execute()
    def cmd(self, args):
        if args[0]==self.name and args[1]=='set_interval':
            self.interval = int(args[2])
            return true
        return super().cmd(args)
    def execute(self):
        if not self.fn is None:
            self.fn()

class FileExtObserver(Ticker):
    def __init__(self, name = 'ext_observer', ext='.sdjob', interval = 15):
        super().__init__(name=name, interval=interval) 
        self.ext = ext
    def processFile(self, filename):
        pass
    def execute(self):
        filelist = [ f for f in os.listdir('.') if f.endswith(self.ext) ]
        for f in filelist:
            print(self.name + ": Found file: "+ f)
            self.processFile(f)

class UrlDownloader(Ticker):
    """
      Laedt periodisch eine URL in eine Datei
    """
    def __init__(self, name = 'UrlDownloader', interval = 3600, url='https://bsnx.net/4.0/', filename='data.txt', fail_on_exists = True):
        super().__init__(name, interval) 
        self.url = url
        self.filename = filename
        self.fail_on_exists = fail_on_exists
    def execute(self):
        res = requests.get(self.url)
        if not (os.path.isfile(self.filename) and self.fail_on_exists):
            with open(self.filename, 'w') as f:
                f.write(self.filename)
                
class JobFetcher(Ticker):
    def __init__(self, name = 'UrlDownloader', interval = 120, url = None):
        super().__init__(name, interval) 
        self.url = url 
    def execute(self):
        res = requests.get(self.url)
        job = json.loads(res.text)
        self.cpu.jobs.append(job)

class TypeJobExecutor():
    def __init__(self, name = 'jobtype', interval = 61, executor= None):
        super().__init__(name, interval) 
        self.executor = executor
    def execute(self):
        if len(self.cpu.jobs)>0:
            if self.cpu.jobs[0].type == self.name:
                current = self.cpu.jobs.pop(0)
                result = self.executor(current)
                self.cpu.cmd(['jobresult', result, current])
                print(str(result))
                
class TypeMapJobExecutor():
    def __init__(self, name = 'jobtype', interval = 61, executor= None):
        super().__init__(name, interval) 
        self.executor = executor
    def execute(self):
        if len(self.cpu.jobs)>0:
            if self.cpu.jobs[0].type == self.name:
                current = self.cpu.jobs.pop(0)
                result = self.executor(current)
                self.cpu.jobs.append(result)
                
class NWebJobFetch(Ticker):
    """ 
      NWebFetch(NWebClient(...), 42)  
      
      npy-ticker nwebclient.sd.JobFetch:42
    """
    key = None
    def __init__(self, interval = 60, nwebclient=None, group=None):
        super().__init__("NWebFetch",interval) 
        self.nweb = nwebclient
        self.group = group
    def configure(self, arg):
        #from nwebclient import NWebClient
        #self.nweb = NWebClient()
        #self.group = arg
        pass
    def execute(self):
        docs = self.nweb.docs('group_id='+str(self.group))
        for doc in docs:
            self.download(doc)
    def download(self, doc):
        self.log("Start Download")
        content = doc.content()
        self.cpu.jobs.append(json.loads(content))
        self.nweb.deleteDoc(doc.id())
    def log(self, message):
        print("JobFetch: "+str(message))

class UrlPostShTicker(Ticker):
    """
      Sendet Daten an einen POST-Endpoint
    """
    uptime_counter = 0
    def __init__(self, name = 'UrlPostShTicker', interval = 7200, url='https://bsnx.net/4.0/'):
        super().__init__(name, interval) 
        self.url = url  
    def execute(self):
        self.uptime_counter = self.uptime_counter + self.interval
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        requests.post(self.url, data={'uptime': str(self.uptime_counter)+"s up, "+current_time})

class WebProcess(Process):
    def __init__(self, port = 9080):
        super().__init__('WebProcess')
        self.port = port
    def startServer(self):
        import threading 
        f = lambda: self.startAsync()
        x = threading.Thread(target=f)
        x.start()
    def index():
        return "Hallo Welt"
    def createApp(self):
        from flask import Flask
        app = Flask(self.name)
        app.add_url_rule('/', 'index', lambda: self.index())
        app.add_url_rule('/status', 'status', lambda: "ok")
        app.add_url_rule('/job-count', 'job_count', lambda: str(len(self.cpu.jobs)))
    def startAsync(self):
        app = self.createApp()
        app.run(port=self.port)


class Cpu:
    processes = []
    sleep_time = 1
    jobs = []
    def __init__(self, *args):
        for arg in args:
            self.add(arg)
    def __iter__(self):
        return self.processes.__iter__()
    def add(self, process):
        process.cpu = self
        self.addChild(process)
        self.processes.append(process)
    def tick(self):
        for p in self.processes:
            p.tick()
        if self.sleep_time > 0:
            time.sleep(self.sleep_time)
    def cmd(self, args):
        for p in self.processes:
            p.cmd(args)
    def loop(self):
        while True:
            self.tick()
    def runTicks(self, count=100) :
        for i in range(count):
             self.tick()
    def __str__(self):
        s = "Cpu("
        for p in self.processes:
            s = s + ' ' + str(p)
        return s

def load_class(cl):
    d = cl.rfind(".")
    classname = cl[d+1:len(cl)]
    m = __import__(cl[0:d], globals(), locals(), [classname])
    return getattr(m, classname)

def load_from_arg(cpu, arg):
    a = arg.split(':')
    a.append('')
    cls = load_class(a[0])
    c = cls()
    c.configure(''.join(a[1:]))
    cpu.add(c)
                
def main():
    print("npy-ticker")
    print("npy-ticker namespace.Proc:cfg ...")
    cpu = Cpu()
    for arg in sys.argv[1:]:
        print("Loading: " + arg)   
        load_from_arg(cpu, arg)
    print(str(cpu))
    #cpu.loop()
    
# 
if __name__ == '__main__': # npy-ticker vom python-package bereitgestellt
    main()