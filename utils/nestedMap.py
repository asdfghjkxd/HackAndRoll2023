from typing import *




class NestedMap:
    
    def __init__(self):
        self.v = None
        self.w = None
        self.child = {}
    
    def __init__(self, v, w):
        self.v = v
        self.w = w
        self.child = {}

    def __repr__(self):
        return str(self.v) + ", " +  str(self.w) + ":" + str(self.child)

    def __str__(self):
        return str(self.v) + ", " +  str(self.w) + ":" + str(self.child)




if __name__ == "__main__":
    nm = NestedMap(1, 2, {})
    