from Assistent_capabilities import action_controll

class Test:


    def x(self):
        for row in action_controll.search_fuction('кошка', 0):
            print(row)

    def start(self):
        self.x()

test = Test()
test.start()