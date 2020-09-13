import app.Dates as Dates


class Date():

    def __init__(self):
        self.days = []
        self.values = []
        self.labels = []

    def add_day(self, *args):
        self.index = args[0]
        self.payday = args[1]
        self.total = args[2]
        self.date = args[3]
        self.expense = args[4]
        self.prices = args[5]
        self.days.append([
            self.index,
            self.payday,
            self.total,
            self.date,
            self.expense,
            self.prices,
        ])

    def print_day(self):
        print(self.days)

    def append_data(self):
        for day in self.days:
            self.values.append(day[2])
            self.labels.append(day[3])

    def return_data(self):
        return self.labels, self.values, self.days


class Calculate:
    def check_negative(self):
        if self.total < 0:
            self.total = 0.00
        return

    def add_income(self, price):
        self.total = float(price) + float(self.total)
        return self.total

    def add_expense(self):
        self.total = float(self.total) - self.expense
        return self.total

    def add_weekly_expense(self):
        self.total = float(self.total) - (self.week[2] + self.expense)
        return self.total

    def add_biweekly_expense(self):
        self.total = float(self.total) - (self.week[3] + self.expense)
        return self.total

    def add_monthly_expense(self):
        self.total = float(self.total) - (self.week[4] + self.expense)
        return self.total
    
    def recurring(self):
        if self.index in self.paydates:
            # Add the paycheck to the balance, else subtract from
            # previous day total
            self.payday = True
            price = self.prices[1]
            self.total = self.add_income(price)
            self.check_negative()
        if self.index not in self.paydates:
            self.payday = False
            self.total = self.add_expense()
            self.check_negative()
        # Subtract weekly expense on the week
        if self.index in self.weeklyExpense:
            self.total = self.add_weekly_expense()
            self.check_negative()
        if self.index in self.biweeklyExpense:
            self.total = self.add_biweekly_expense()
            self.check_negative()
        self.day.add_day(self.index,
                         self.payday,
                         round(self.total, 2),
                         self.date[self.index],
                         self.expense,
                         self.prices[0])

    def existing(self):
        if self.index in self.paydates:
            # Add the paycheck to the balance, else subtract from
            # previous day total
            self.payday = True
            price = self.prices[0]
            self.total = self.add_income(price)
            self.check_negative()
        if self.index not in self.paydates:
            self.payday = False
            self.total = self.add_expense()
            self.check_negative()
        # Subtract weekly expense on the week
        if self.index in self.weeklyExpense:
            self.total = self.add_weekly_expense()
            self.check_negative()
        if self.index in self.biweeklyExpense:
            self.total = self.add_biweekly_expense()
            self.check_negative()
        self.day.add_day(self.index,
                         self.payday,
                         round(self.total, 2),
                         self.date[self.index],
                         self.expense,
                         self.prices[0])

    def enum_expenses(self):
        for self.index, self.expense in enumerate(self.dailyExpenses):
            self.payday = False
            if self.index < self.paydates[0]:
                self.existing()
            else:
                self.recurring()

    def enum_balance(self, *args):
        self.weeklyExpense = args[0]
        self.biweeklyExpense = args[1]
        self.dailyExpenses = args[2]
        self.date = args[3]
        self.paydates = args[4]
        self.week = args[5]
        self.prices = args[6]
        self.days = []
        self.values = []
        self.labels = []
        self.day = Date()
        try:
            self.total = 0
            # For each expense total, subtract from balance for each day
            self.enum_expenses()
            self.day.append_data()
            # import pdb; pdb.set_trace()
        finally:
            del self.total
            del self.prices
            return self.day.return_data()


class Comprehensions():
    # List comprehensions for the labels
    def weekly(self, range_end):
        return [i for i in range(0, range_end, 7)]

    def biweekly(self, range_end):
        return [i for i in range(0, range_end, 14)]

    def daily_span(self, range_end):
        return [day for day in range(0, range_end)]

    def other_span(self, range_end):
        return [day for day in range(0, range_end, 2)]

    def other_add(self, deduct, label_span):
        daily = label_span[1]
        other = label_span[0]
        return [deduct[0] + deduct[1] for d in daily for o in other if d == o]

    def no_other(self, deduct, daily):
        return [deduct[2] for day in daily]

    def daily_add(self, deduct, otherInsert):
        return [deduct[0] for day in range(len(otherInsert))]

    def deduct_list(self, occurence):
        return [i for i in occurence]

    def stacked_list(self, occurence):
        return [i for elem in occurence for i in elem]

    def paydates(self, incomes, weekday, span):
        paydays = []
        for x in range(len(incomes)):
            if len(incomes[x][0]) == 1:
                paydates = [0]
            else:
                income = int(incomes[x][2])
                pay_span = int(incomes[x][3])
                # Begin with today's Dates
                paydates = [
                    i for i in range((income - weekday),
                                     Dates.Dates().span_length(span), pay_span)
                    if i > 0
                ]
            paydays.append(paydates)
        return paydays
