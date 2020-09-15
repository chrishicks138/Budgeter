import app.Dates as Dates
from app.Lists import Comprehensions, ExpenseList


class Date():
    def __init__(self):
        self.days = []
        self.values = []
        self.labels = []

    def add_day(self, *args):
        self.index = args[0]
        self.total = args[1]
        self.day = args[2]
        self.expense = args[3]
        self.prices = args[4]
        self.days.append([
            self.index,
            self.total,
            self.day,
            self.expense,
            self.prices,
        ])

    def append_data(self):
        for day in self.days:
            self.values.append(day[1])
            self.labels.append(day[2])

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
        self.total = float(self.total) - (float(ExpenseList.weekly[2]) + self.expense)
        return self.total

    def add_biweekly_expense(self):
        self.total = float(self.total) - (float(ExpenseList.biweekly[2]) + self.expense)
        return self.total

    def add_monthly_expense(self):
        self.total = float(self.total) - (self.week[4] + self.expense)
        return self.total

    def calc(self, income):
        if self.index in self.paydates:
            '''
            Add the paycheck to the balance, else subtract from
            previous day total and subtract weekly expense
            on the week
            '''
            price = self.prices[0][income]
            self.total = self.add_income(price)
            self.check_negative()
        if self.index not in self.paydates:
            self.total = self.add_expense()
            self.check_negative()
        if self.index in self.weeklyExpense:
            self.total = self.add_weekly_expense()
            self.check_negative()
        if self.index in self.biweeklyExpense:
            self.total = self.add_biweekly_expense()
            self.check_negative()
        self.day.add_day(self.index, round(self.total, 2),
                         self.date[self.index], self.expense, self.prices[0][income])

    def recurring(self):
        income = 1
        self.calc(income)

    def existing(self):
        income = 0
        self.calc(income)

    def enum_expenses(self):
        for self.index, self.expense in enumerate(self.dailyExpenses):
            if self.index < self.paydates[0]:
                self.existing()
            else:
                self.recurring()

    def enum_balance(self, *args):
        self.weeklyExpense = ExpenseList.weekly[1]
        self.biweeklyExpense = ExpenseList.biweekly[1]
        self.dailyExpenses = ExpenseList.daily[1]
        self.date = Dates.Dates().label()
        self.paydates = Comp.paydates(args[0])
        self.week = args[1]
        self.prices = Comp.prices()
        self.days = []
        self.values = []
        self.labels = []
        self.day = Date()
        try:
            self.total = 0
            # For each expense total, subtract from balance for each day
            self.enum_expenses()
            self.day.append_data()
        finally:
            del self.total
            del self.prices
            return self.day.return_data()



Comp = Comprehensions()
