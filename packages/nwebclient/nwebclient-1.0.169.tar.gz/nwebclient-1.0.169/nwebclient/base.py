
class Base:
    __childs = []
    __owner = None
    def owner(self):
        return self.__owner
    def addChild(self, child):
        child.__owner = self
        __childs.append(child)
    def childs(self):
        return __childs
    def isRoot(self):
        return self.__owner is None