import os

from typing import *
from pydantic import BaseModel
from utils.pair import Pair
from functools import reduce


class Wordle:
    # allowed is the list of allowed words
    # answer is the list of answer, subset of allowed
    # number of letters
    allowed: List
    answer: List
    n: int
    # the result when the word is solved
    c: int
    dict: Dict

    class Config:
        validate_assignment = True
        allow_mutation = True

    def __init__(self, letters: int): 
        self.allowed = self.__parse_and_load_datafile("assets/allowed.txt")
        self.answer = self.__parse_and_load_datafile("assets/answer.txt")
        self.n = letters
        self.c = 3**self.n - 1
        self.dict = self.create(self.allowed, self.answer)

    #create a dictionary of comparison results
    def create(self, allowed: List[str], ans: List[str]) -> Dict:
        dict = {}
        n1 = len(allowed)
        n2 = len(ans)
        for i in range(n1):
            dict[allowed[i]] = {}
            for j in range(n2):
                dict[allowed[i]][ans[j]] = Wordle.compare(allowed[i], ans[j], self.n)
        return dict


    #return an int that gives the result of w1 compared to w2
    @classmethod
    def compare(cls, w1: str, w2: str, n: int) -> int:
        arr1 = [0 for i in range(n)]
        arr2 = [0 for i in range(n)]
        for i in range(n):
            if w1[i] == w2[i]:
                arr1[i] = 2
                arr2[i] = 2

        for i in range(n):
            if arr1[i] != 0:
                continue
            for j in range(n):
                if arr2[j] != 0:
                    continue
                if w1[i] == w2[j]:
                    arr1[i] = 1
                    arr2[j] = 1
                    break
        ans = 0
        for i in range(n):
            ans += 3**i * arr1[i]
        return ans 
            

    def check(self, s: str, list: List[str]) -> Dict[int: List[str]]:
        dict = {}
        for word in list:
            k = Wordle.compare(s, word, self.n)
            if k not in dict:
                dict[k] = []
            dict[k].append(word)
        return dict
            

    
    def checkSet(self, s: str, list: List[str]) -> Set[int]:
        set = {}
        for word in list:
            k = Wordle.compare(s, word, self.n)
            if k not in set:
                set.add(k)
        return set

    #return a list of successor words
    def successor(self, ans: List[str], k: int) -> List[str]:
        x = len(self.allowed)
        y = len(ans)
        l = []
        for i in range(x):
            s = self.allowed[i]
            d = self.checkSet(s, ans)
            if len(d) == y:
                return [s]
            l.append(Pair(s, len(d)))
        l.sort(lambda x: x.getSnd(), reverse = True)
        threshold = l[min(len(l) - 1, k)]
        anslist = []
        i = 0
        for 
        

    def solve(self, ans: List[str], t: int) -> Pair:
        y = len(ans)

        if (y < 3):
            return Pair(ans[0], 2 * y - 1)
        elif (y < 20):
            max = -float("inf")
            string = ""

            for i in range(y):
                temp_h = self.checkSet(ans[i], ans)
            
                if (len(temp_h) == max):
                    return Pair(ans[i], 2 * y - 1)
                elif (len(temp_h) > max):
                    max = len(temp_h)
                    string = ans[i]
            
            if (max == y - 1):
                return Pair(string, 2 * y)
        
        next_successor = self.successor(ans, t)
        solve_map = list(map(lambda x: Pair(x, self.miniSolve(x, ans, t), next_successor)))
        return reduce(lambda x, y: x if x.getSnd() < y.getSnd() else y, solve_map, Pair("", 6 * y))

    def miniSolve(self, word: str, ans: List[str], t: int):
        hashing = self.check(word, ans)

        if len(hashing) == 1:
            return float("inf")
        elif len(hashing) == len(ans):
            return 2 * len(ans)
        
        sum = len(ans)

        for key in hashing.keys():
            sum += self.solve(hashing[key], t).getSnd()

        if self.c in hashing:
            sum -= 1
        
        return sum


    def print(self, ans: List, k: int):
        def inner_comparator():
            def compare(x: Pair, y: Pair):
                return x.getSnd() - y.getSnd()

            return compare
            
        grouping = []

        for i in range(len(self.allowed)):
            grouping.append(
                Pair(s=self.allowed[i], len(self.checkSet(self.allowed[i], ans)))
            )

        
        grouping = sorted(grouping, cmp=inner_comparator())

    

    # read and parse the datafile
    def __parse_and_load_datafile(self, datafile: os.PathLike | str):
        try:
            with open(datafile, "r") as f:
                return f.readlines()
        except FileNotFoundError:
            raise ValueError("Invalid Filepath: " + str(datafile))
        