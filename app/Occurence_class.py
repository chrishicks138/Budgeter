import app.Dates as Dates
from app.models import Expense, Income
from collections import deque
from app.Calculate import Calculate, Comprehensions


class IncomeList():
    pass


class Lists():
    def __init__(self):

        # Query Expense table

        self.expense_list = Expense.query.all()

        # Query Income table

        income_list = Income.query.all()

        self.incomes = []
        for income in income_list:
            self.incomes.append(income)

    def Income(self, range_end):
        self.income_list = []
        IncomeList.recurring = []
        IncomeList.existing = []
        for income in self.incomes:
            if income.occurence == "5":
                income_occurence = ([0], income.price, income.payday)
                self.income_list.append(income_occurence)
                IncomeList.existing.append(
                    ("existing",
                     [0],
                     income.price,
                     income.payday))
            if income.occurence == "2":
                income_occurence = (Comp.weekly(range_end), income.price,
                                    income.payday, 7)
                self.income_list.append(income_occurence)
                IncomeList.recurring.append(
                    ("weekly",
                     Comp.weekly(range_end),
                     income.price,
                     income.payday,
                     7))
            if income.occurence == "4":
                income_occurence = (Comp.biweekly(range_end), income.price,
                                    income.payday, 14)
                self.income_list.append(income_occurence)
                IncomeList.recurring.append(
                    ("biweekly",
                     Comp.biweekly(range_end),
                     income.price,
                     income.payday,
                     14))

        if len(self.income_list) < 2:
            self.income_list.append(([0], 0.0, 0))
        return self.income_list

    def paydates(self, weekday, span):
        paydays = []
        incomes = []
        for paydates in IncomeList.recurring:
            incomes.append((int(paydates[3]), int(paydates[4])))
        for income in incomes:
            # Begin with today's Dates
            paydates = [
                i for i in range(income[0],
                                 Dates.Dates().span_length(span),
                                 income[1])
            ]
            paydays.append(paydates)
        return paydates

    def Expense(self, range_end):
        weekly = []
        daily = []
        other = []
        biweekly = []
        for expense in self.expense_list:
            # Round expense to two decimal places and
            # append each occuring expense to its respectable
            # list
            expense.price = round(float(expense.price), 2)
            if expense.occurence == "2":
                weekly.append(expense.price)
            elif expense.occurence == "1":
                daily.append(expense.price)
            elif expense.occurence == "3":
                other.append(expense.price)
            elif expense.occurence == "4":
                biweekly.append(expense.price)
        # Add each expense in each category and return it
        return [sum(daily), sum(other), sum(weekly), sum(biweekly)]


class Occurence:
    def __init__(self):
        self.totals = []
        self.dailyExpenses = []

    def range_span(self, span):
        rspan = [[], []]
        for i in range(len(self.deduct)):
            if self.deduct[i] != 0:
                self.range_end = Dates.Dates().span_length(span)
                if i == 1:
                    rspan.insert(0, Comp.other_span(self.range_end))
                if i == 2:
                    rspan.insert(1, Comp.daily_span(self.range_end))
        return rspan

    def daily_append(self):
        otherInsert = Comp.no_other(self.deduct, self.label_span[1])
        f = Comp.daily_add(self.deduct, otherInsert)
        for day in f:
            self.dailyExpenses.append(day)

    def other_append(self):
        otherInsert = Comp.other_add(self.deduct, self.label_span)
        otherInsert = deque(otherInsert)
        f = Comp.daily_add(self.deduct, otherInsert)
        for day in f:
            dailyOther = otherInsert.popleft()
            self.dailyExpenses.append(dailyOther)
            self.dailyExpenses.append(day)

    def range_calc2(self, span):
        # This is the complicated part, set label ranges for
        # each expense occurence, then add to a weekly range.
        self.label_span = self.range_span(span)
        while (len(self.dailyExpenses) < len(self.label_span)):
            if self.deduct[1] == 0:
                self.daily_append()
            else:
                self.other_append()
        return self.dailyExpenses

    def range_calc(self, span):
        self.range_end = Dates.Dates().span_length(span)
        self.deduct = Lists().Expense(self.range_end)
        self.dailyExpenses = self.range_calc2(span)
        incomes = Lists().Income(Dates.Dates().span_length(span))
        # import pdb; pdb.set_trace()
        prices = [int(IncomeList.existing[0][2]),
                  int(IncomeList.recurring[0][2])]
        weekday = Dates.weekday
        return Calc.enum_balance(
            Comp.weekly(Dates.Dates().span_length(span)),
            Comp.biweekly(Dates.Dates().span_length(span)),
            self.dailyExpenses,
            Dates.Dates().label(),
            Lists().paydates(weekday, span),
            # Comp.paydates(incomes, weekday, span),
            self.deduct,
            prices)


def delete():
    dates.delete()


Calc = Calculate()
dates = Dates.Labels()
Comp = Comprehensions()
