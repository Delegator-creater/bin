class Pair():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def first(self):
        return self.x

    def edit_first(self , new_first):
        self.x = new_first

    def second(self):
        return self.y

    def edit_second(self, new_second):
        self.y = new_second


def second_to_first(x: Pair):
    return x.second().result(x.first())