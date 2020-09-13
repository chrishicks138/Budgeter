
class Chart():

    def __init__(self):
        self.dates = []
        print("Chart dates", self.dates)

    def days(self, *args):
        self.index = args[0]
        self.payday = args[1]
        self.total = args[2]
        self.date = args[3]
        self.expense = args[4]
        self.prices = args[5]
        print("Index", args[0])
        self.dates.append((
            self.index,
            self.payday,
            self.total,
            self.date,
            self.expense,
            self.prices,
        ))

    def print_days(self):
        print(self.dates)
