from typing import *


# declare the generics
K = TypeVar('K') 
V = TypeVar('V')
W = TypeVar('W') 

class NestedMap(K, V, W):
    v: Optional[V]
    w: Optional[W]
    # child: Dict[K, 'NestedMap(K, V, W)']
    child: Dict[K, 'NestedMap']
    
    def __init__(self):
        self.v = V
        self.w = W
        self.child = {}
    
    def __init__(self, v: V, w: W):
        self.v = v
        self.w = w
        self.child = {}



if __name__ == "__main__":
    nm = NestedMap(1, 2, {})
    