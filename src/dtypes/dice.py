import random
from pydantic import PositiveInt
from pydantic.dataclasses import dataclass

@dataclass
class Dice():
    max: PositiveInt = 100

    def roll(self):
        return random.randint(1,self.max)
    
    def rolln(self, x:int):
        results = []
        for i in range(x):
            results.append(random.randint(1,self.max))
        return sum(results)
    
d100 = Dice(100)    

d6 = Dice(6)

if __name__ == "__main__":
    res = d100.roll()
    print(res)
    