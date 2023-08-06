
import os
import os.path
import sys
import importlib
import json
import socket
from contextlib import closing

class Args:
    argv = []
    cfg=None
    def __init__(self, argv = None):
        if argv is None:
            self.argv = sys.argv
        else:    
            self.argv = argv
    def hasFlag(self, name):
        return '--'+name in self.argv
    def getValue(self, name, default=None):
        for i in range(len(self.argv)-1):
            if self.argv[i]=='--'+name:
                return self.argv[i+1]
        return default
    def getValues(self, name):
        res = []
        for i in range(len(self.argv)-1):
            if self.argv[i]=='--'+name:
                res.append(self.argv[i+1])
        return res
    def __read_cfg(self):
        if os.path.isfile('nweb.json'):
            with open('nweb.json') as f:
                self.cfg = json.load(f)
        else:
            self.cfg = {}
    def env(self, name, default=None):
        self.__read_cfg();
        if name in self.cfg:
            return self.cfg[name]
        return os.getenv(name, default)
    
def load_class(spec, create=False):
    """ spec = 'module.ClassName' """
    a = spec.split(':')
    m = importlib.import_module(a[0])
    c = getattr(m, a[1])
    if create:
        return c()
    else:
        return c

def exists_module(module_name):
    """
      itertools = importlib.import_module('itertools')
      import pkg_resources
      pkg_resources.get_distribution('requests').version
    """
    import importlib.util
    module_spec = importlib.util.find_spec(module_name)
    found = module_spec is not None
    return found

def download(url, filename, ssl_verify=True):
    import requests
    r = requests.get(url, stream=True, verify=ssl_verify) 
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]