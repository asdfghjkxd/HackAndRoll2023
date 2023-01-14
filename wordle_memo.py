import wordle

from typing import *
from utils.nestedMap import NestedMap
from utils.pair import Pair
from functools import reduce


class WordleMemo(wordle.Wordle):
    def __init__(self, letters: int):
        super().__init__(letters)

    
    def solve(self, ans: List[str], t: int) -> Pair:
        y = len(ans)

        if y < 3:
            if y == 2:
                nestedMap = self.solve(ans[0:1], t).getFst()
                nestedMap.child[self.compareDict[ans[0]][ans[1]]] = self.solve(ans[1:2], t).getFst()
                nestedMap.w = ans
                return Pair(nestedMap, 3)
            
            nestedMap = NestedMap(ans[0], None)
            nestedMap.child[(3 ** self.n) - 1] = None
            nestedMap.w = ans
            return Pair(nestedMap, 1)
        
        if y < 20:
            max = 0
            n = 0
            g = {}

            for i in range(y):
                h = self.check(ans[i], ans)
                if len(h) == y:
                    nestedMap = NestedMap(ans[i], None)
                    for key in h.keys():
                        nestedMap.child[key] = self.solve(h[key], t).getFst()
                    
                    nestedMap.child[self.c] = None
                    nestedMap.w = ans
                    return Pair(nestedMap, 2 * y - 1)

                if len(h) > max:
                    max = len(h)
                    n = i
                    g = h
            
            if max == y - 1:
                nestedMap = NestedMap(ans[n], None)
                for key in g:
                    nestedMap.child[key] = self.solve(g[key], t).getFst()
                
                nestedMap.child[self.c] = None
                nestedMap.w = ans
                return Pair(nestedMap, y * 2)
        
        ls = self.successor(ans, t)
        mapped_ls = list(map(lambda inputs: self.miniSolveMemo(inputs, ans, t), ls))
        return reduce(
            lambda x, y: x if x.getSnd() < y.getSnd() else y,
            mapped_ls,
            Pair(None, float("inf"))
        )

    def miniSolveMemo(self, s: str, ls: List[str], x: int) -> Pair:
        sum = len(ls)
        hashmap = self.check(s, ls)
        nestedMap = NestedMap(s, None)
        nestedMap.w = ls

        if (len(hashmap) == 1):
            return Pair(None, float("inf"))
        
        for key in hashmap.keys():
            p1 = self.solve(hashmap[key], x)
            sum += p1.getSnd()
            nestedMap.child[key] = p1.getFst()
        
        if self.c in hashmap:
            sum -= 1
            nestedMap.child[self.c] = None
        
        return Pair(nestedMap, sum)
    
    def print(self, hashmap: NestedMap):
        if hashmap is None:
            ls = []
            ls.append([])
            return ls
        
        ls = []
        for key in hashmap.keys():
            for item in hashmap[key]:
                ls.append(item)

        for inner_ls in ls:
            inner_ls.append(hashmap.getV())
        
        return ls
    def print(self, ans: List, k: int):
        """
        Prints out the outputs from the algorithm
        """
        def inner_comparator():
            def compare(x: Pair, y: Pair):
                return x.getSnd() - y.getSnd()

            return compare
            
        grouping = []

        for i in range(len(self.allowed)):
            grouping.append(
                Pair(s=self.allowed[i], t=len(self.checkSet(self.allowed[i], ans)))
            )

        grouping.sort(key=lambda x: x.getSnd(), reverse=True)
        for i in range(min(len(self.allowed), k)):
            print(grouping[i], end="\n")

    def run(self):
        pair = self.solve(
            self.answer,
            1
        )
        print(pair)

if __name__ == "__main__":
    word = WordleMemo(5)
    word.run()
