
class Base:
    __childs = []
    __owner = None
    def owner(self):
        return self.__owner
    def addChild(self, child):
        child.__owner = self
        self.__childs.append(child)
    def childs(self):
        return self.__childs
    def isRoot(self):
        return self.__owner is None
    def getParents(self):
        res = []        
        current = self.__owner
        while not current is None:
            res.append(current)
            current = current.__owner
    def getParantClass(self, cls):
        for p in self.getParents():
            if isinstance(p, cls):
                return p
        return None
    def onParentClass(self, cls, action):
        p = self.getParnetClass(cls)
        if not p is None:
            action()
    def className(self):
        a = type(self)
        return "{0}.{1}".format(a.__class__.__module__,a.__class__.__name__)