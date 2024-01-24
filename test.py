
class myClass:

    def __init__(self, my_var):
        self.my_var = my_var

    def doStuff(self, var):
        print(var)

class Main():

    test = myClass(123)
    print(test.my_var)
    test.doStuff(test.my_var)