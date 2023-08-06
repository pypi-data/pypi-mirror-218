import sys
import json
import datetime

from nwebclient import base


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
    def info(self, msg
        #out = lambda msg: "[JobRunner] "+str(msg)
        print("[JobRunner] " + msg)
    def execute_job(self, job):
        try:
            result = self.jobexecutor(job)
        except MoreJobs as mj:
            result = self.execute_data(mj.data)
        except Exception as e:
            self.info('Error: Job faild', file=sys. stderr)
            result = job
            result['error'] = True
            result['error_message'] = str(s)
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
            self.info("Faild to execute JSON-File "+str(infile))
    def execute_rest(self, port=8080, run=True, route='/', app=None):
        self.info("Starting webserver")
        from flask import Flask, render_template, request, response
        from flask import session, copy_current_request_context
        if app is None:
            app = Flask(__name__)
        #@app.route('/')
        #def home():
        #    return json.dumps(execute_data(request.form.to_dict(), jobexecutor))
        app.add_url_rule(route, 'job_runner', view_func=lambda: json.dumps(self.execute_data(request.form.to_dict())))
        if run:
            app.run(host='0.0.0.0', port=port)
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
    def dependsOn(cls):
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
    def __call__(self, data):
        if self.key in data:
            runner = self.runners[data[self.key]]
            return runner(data)
        else:
            return {'success': False, 'message': "Key not in Data", 'data': data}
    def canExecute(self, data):
        if self.key in data:
            return data[self.key] in self.runners
        return False
        
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
        