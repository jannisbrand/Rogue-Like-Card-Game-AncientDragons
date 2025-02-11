from typing import Type


class TEST():
    def __init__(self):
        self.testVar = 1

    def test(self):
        print("HI!")

t = TEST()
level_components: dict[Type, dict[int, any]] = dict()

level_components[type(t)] = {}
level_components[type(t)][1] = t

t.testVar
print(level_components[type(t)][1].testVar)