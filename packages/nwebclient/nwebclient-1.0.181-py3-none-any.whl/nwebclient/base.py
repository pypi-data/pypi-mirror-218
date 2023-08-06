
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
    def className(self):
        a = type(self)
        return "{0}.{1}".format(a.__class__.__module__,a.__class__.__name__)