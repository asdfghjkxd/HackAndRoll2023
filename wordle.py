import os

from json import dump
from typing import *
from utils.configured_base_model import PyBaseModel
from utils.pair import Pair
from functools import reduce

class Wordle(PyBaseModel):
    """
    Main wordle solver

    :attribute allowed: List of allowed words
    :attribute answer: List of answers, with subsets of it permitted
    :attribute n: Number of letters in the word
    :attribute c: Result when the word is solved
    :attribute dict: Dictionary of comparison
    """

    allowed: Optional[List[str]]
    answer: Optional[List[str]]
    n: Optional[int]
    c: Optional[int]
    compareDict: Optional[Dict]

    def __init__(self, letters: int):
        """
        Initialises the Wordle class

        Note that the dictionaries of permitted words and answers is loaded into the object as it is
        instantiated

        :param letters: Number of letters in the word
        """

        super().__init__()
        self.allowed = self.__parse_and_load_datafile("assets/allowed.txt")
        self.answer = self.__parse_and_load_datafile("assets/answer.txt")
        self.n = letters
        self.c = (3 ** self.n) - 1
        self.compareDict = self.create(self.allowed, self.answer)

    #create a dictionary of comparison results
    def create(self, allowed: List[str], ans: List[str]) -> Dict[str, Dict[str, int]]:
        """
        Creates a dictionary of comparison results

        :param allowed: List of strings, containing the list of permitted words
        :param ans: List of strings, containing possible answers to the word
        """

        dict = {}
        n1 = len(allowed)
        n2 = len(ans)

        for i in range(n1):
            dict[allowed[i]] = {}
            for j in range(n2):
                dict[allowed[i]][ans[j]] = Wordle.compare(allowed[i], ans[j], self.n)

        with open("big_fat_dict.json", "w") as f:
            dump(dict, f)

        return dict

    #return an int that gives the result of w1 compared to w2
    @classmethod
    def compare(cls, w1: str, w2: str, n: int) -> int:
        """
        Comparison function
        """

        arr1 = [0]*n
        arr2 = [0]*n
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

    def check(self, s: str, list: List[str]) -> Dict[int, List[str]]:
        dict = {}
        for word in list:
            k = Wordle.compare(s, word, self.n)
            if k not in dict:
                dict[k] = []
            dict[k].append(word)
        return dict
    
    def checkSet(self, s: str, ans: List[str]) -> Set[int]:
        sex = set()
        for word in ans:
            k = Wordle.compare(s, word, self.n)
            if k not in sex:
                sex.add(k)
        return sex

    #return a list of successor words
    def successor(self, ans: List[str], k: int) -> List[str]:
        """
        Returns a list of successor words

        :param ans: List of strings, containing possible answers
        :param k: Integer, "Depth" of search
        """

        x = len(self.allowed)
        y = len(ans)
        l = []
        for i in range(x):
            s = self.allowed[i]
            d = self.checkSet(s, ans)
            if len(d) == y:
                return [s]
            l.append(Pair(s = s, t = len(d)))
        l.sort(key=lambda x: x.getSnd(), reverse=True)
        threshold = l[min(len(l) - 1, k)].getSnd()
        ansList = []
        i = 0
        while i < x and l[i].getSnd() >= threshold:
            ansList.append(self.allowed[i])
        return ansList

    def solve(self, ans: List[str], t: int) -> Pair:
        """
        Solving function
        """

        y = len(ans)

        if (y < 3):
            return Pair(ans[0], 2 * y - 1)
        
        if (y < 20):
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
        solve_map = list(map(lambda x: Pair(x, self.miniSolve(x, ans, t)), next_successor))
        return reduce(lambda x, y: x if x.getSnd() < y.getSnd() else y, solve_map, Pair("", 6 * y))

    def miniSolve(self, word: str, ans: List[str], t: int):
        """
        Helper function to solve()
        """

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


    @staticmethod
    def __parse_and_load_datafile(datafile: os.PathLike | str):
        """
        Reads and parse the relevant datafiles into the object

        :param datafile: str, or os.Pathlike object, a path to the txt file to read
        """

        try:
            with open(datafile, "r") as f:
                return f.readlines()
        except FileNotFoundError:
            raise ValueError("Invalid Filepath: " + str(datafile))


if __name__ == "__main__":
    word = Wordle(5)
    word.run()
