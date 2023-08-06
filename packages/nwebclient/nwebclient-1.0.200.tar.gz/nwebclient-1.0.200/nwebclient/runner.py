import sys
import json
import traceback
import importlib
import requests
from  datetime import datetime

from nwebclient import base
from nwebclient import util
from nwebclient import ticker


# if __name__ == '__main__':
#     from nwebclient import runner
#     runner.main(custom_job)

class MoreJobs(Exception):
    """ raise MoreJobs([...]) """
    def __init__(self,jobs= []):
        self.data  = {'jobs': jobs}

class JobRunner(base.Base):
    
    counter = 0 
    
    # Start Time
    start = None
    
    jobexecutor = None
    
    def __init__(self, jobexecutor):
        self.jobexecutor = jobexecutor
        self.addChild(self.jobexecutor)
    def info(self, msg):
        #out = lambda msg: "[JobRunner] "+str(msg)
        print("[JobRunner] " + msg)
    def __call__(self, job):
        return self.execute_job(job)
    def execute(self, job):
        return self.execute_job(job)
    def execute_job(self, job):
        try:
            result = self.jobexecutor(job)
        except MoreJobs as mj:
            result = self.execute_data(mj.data)
        except Exception as e:
            self.info('Error: Job faild')
            result = job
            result['success'] = False
            result['error'] = True
            result['error_message'] = str(e)
        return result
    def execute_data(self, data):
        self.start = datetime.now()
        result = {'jobs': []}
        for job in data['jobs']:
            job_result = self.execute_job(job)
            result['jobs'].append(job_result)
            self.counter = self.counter + 1
        delta = (datetime.now()-self.start).total_seconds() // 60
        self.info("Duration: "+str(delta)+"min")
        return result
    def execute_file(self, infile, outfile = None):
        try:
            data = json.load(open(infile))
            result = self.execute_data(data)
            outcontent = json.dumps(result)
            print(outcontent)
            if not outfile is None:
                if outfile == '-':
                    print(outcontent)
                else:
                    with open(outfile, 'w') as f:
                        f.write(outcontent)
        except Exception as e:
            self.info("Error: " + str(e))
            self.info(traceback.format_exc());
            self.info("Faild to execute JSON-File "+str(infile))
    def execute_rest(self, port=8080, run=True, route='/', app=None):
        self.info("Starting webserver")
        from flask import Flask,request
        if app is None:
            app = Flask(__name__)
        #@app.route('/')
        #def home():
        #    return json.dumps(execute_data(request.form.to_dict(), jobexecutor))
        app.add_url_rule(route, 'job_runner', view_func=lambda: json.dumps(self.execute_job(request.args.to_dict() | request.form.to_dict())))
        app.add_url_rule('/job-counter', 'job_counter', view_func=lambda: str(self.count))
        if run:
            app.run(host='0.0.0.0', port=int(port))
        else:
            return app

        
class BaseJobExecutor(base.Base):
    def __call__(self, data):
        return self.execute(data)
    def execute(self, data):
        pass
    def canExecute(self, data):
        return True
    @classmethod
    def pip_install(cls):
        print("PIP Install")
        print(cls.MODULES)

class MultiExecutor(BaseJobExecutor):
    executors = []
    def __init__(self, *executors):
        self.executors = executors
    def execute(self, data):
        for exe in self.executors:
            if exe.canExecute(data):
                exe(data)
    def canExecute(self, data):
        for exe in self.executors:
            if exe.canExecute(data):
                return True
        return False

class SaveFileExecutor(BaseJobExecutor):
    filename_key = 'filename'
    content_key = 'content'
    def execute(self, data):
        with open(data[self.filename_key], 'w') as f:
            f.write(data[self.content_key])
    def canExecute(self, data):
        return 'type' in data and data['type']=='savefile'
    @staticmethod
    def run(data):
        r = SaveFileExecutor()
        return r(data)
    
class Pipeline(BaseJobExecutor):
    executors = []
    def __init__(self, *args):
        self.executors.extend(args)
        for item in self.executors:
            self.addChild(item)
    def execute(self, data):
        for item in self.executors:
            data = item(data)
        return data
      
class Dispatcher(BaseJobExecutor):
    key = 'type'
    runners = {}
    def __init__(self, key='type',**kwargs):
        #for key, value in kwargs.items():
        self.key = key
        self.runners = kwargs
        for item in self.runners.values():
            self.addChild(item)
    def execute(self, data):
        if self.key in data:
            runner = self.runners[data[self.key]]
            return runner(data)
        else:
            return {'success': False, 'message': "Key not in Data", 'data': data}
    def canExecute(self, data):
        if self.key in data:
            return data[self.key] in self.runners
        return False
    

class LazyDispatcher(BaseJobExecutor):
    key = 'type'
    classes = {}
    instances = {}
    def __init__(self, key='type',**kwargs):
        self.key = key
        self.loadDict(kwargs)
    def loadDict(self, data):
        if data is None:
            return
        for k in data.keys():
            v = data[k]
            if isinstance(v, str):
                print("[LazyDispatcher] type:"+k+" "+v )
                self.classes[k] = util.load_class(v)
    def execute(self, data):
        if self.key in data:
            t = data[self.key]
            if t in self.instances:
                data = self.instances[t].execute(data)
            elif t in self.classes:
                c = self.classes[t]
                self.instances[t] = c()
                data = self.instances[t].execute(data)
            else:
                data['success'] = False
                data['message'] = 'Unkown Type'
        else:
            data['success'] = False
        return data
    def canExecute(self, data):
        if self.key in data:
            return data[self.key] in self.classes
        return False


class AutoDispatcher(LazyDispatcher):
    def __init__(self, key='type',**kwargs):
        super().__init__(key, **kwargs)
        args = util.Args()
        data = args.env('runners')
        if isinstance(data, dict):
            self.loadDict(data)
           
        
class RestRunner(BaseJobExecutor):
    ssl_verify = False
    def __init__(self, url):
        self.url = url
    def execute(self, data):
        response = requests.post(self.url, data=data, verify=self.ssl_verify)
        return json.load(response.content)       


def main(jobexecutor):
    if len(sys.argv)>2:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        runner = JobRunner(jobexecutor)
        if infile == 'rest':
            runner.execute_rest()
        else:
            runner.execute_file(infile, outfile)
    else:
        print("Usage: infile outfile")
        print("Usage: rest api")
        
if __name__ == '__main__':
    args = util.Args()
    print("Usage: "+sys.executable+" -m nwebclient.runner --install --ticker --executor module:Class --in in.json --out out.json")
    executor = args.getValue('executor')
    if executor is None:
        print("No executor found.")
        exit(1)
    print("Executor: " + executor)
    if args.hasFlag('install'):
        print("Install")
        util.load_class(executor, create=False).pip_install()
    jobrunner = util.load_class(executor, create=True)
    runner = JobRunner(jobrunner)
    if args.hasFlag('ticker'):
        ticker.create_cpu(args).add(JobExecutor(executor=runner)).loopAsync()
    if args.hasFlag('rest'):
        runner.execute_rest(port=args.getValue('port',8080))
    else:
        runner.execute_file(args.getValue('in', 'input.json'), args.getValue('out', 'output.json'))
