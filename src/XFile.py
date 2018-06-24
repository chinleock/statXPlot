import numpy as np
import XH1 import *

class XFile:
    
    def __init__(self, path, action='r'):
        self.path   = path
        self.action = action
        self.XH1    = {}

    def Write(self, h):
        if not is_writeMode: return self
        if is_nameExist(h.name, self.XH1.keys): return self
        self.XH1[h.name]=h
        return self

    #def Close(self):



    def GetXH1Names(self):
        return self.XH1.keys

    #def LoadXH1s(self):
    def GetXH1(self, name):
        return self.XH1s[name]
