import app.Dates as Dates
from app.models import Expense, Income
from collections import deque
from app.Calculate import Calculate, Comprehensions
from app.Lists import IncomeList, ExpenseList


class Lists():
    def __init__(self):

        # Query tables

        self.expense_list = Expense.query.all()
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
                IncomeList.existing.append(
                    ("existing",
                     [0],
                     income.price,
                     income.payday))
            if income.occurence == "2":
                IncomeList.recurring.append(
                    ("weekly",
                     Comp.weekly(int(income.payday), range_end),
                     income.price,
                     income.payday,
                     7))
            if income.occurence == "4":
                IncomeList.recurring.append(
                    ("biweekly",
                     Comp.biweekly(int(income.payday), range_end),
                     income.price,
                     income.payday,
                     14))

    def paydates(self, weekday, span):
        paydays = []
        incomes = []
        if len(IncomeList.existing) < 1:
            IncomeList.existing.append(('None', [0], '0', '0', '1'))
        if len(IncomeList.recurring) < 1:
            IncomeList.recurring.append(('None', [0], '0', '0', '7'))
        for paydates in IncomeList.recurring:
            incomes.append((int(paydates[3]), int(paydates[4])))
        for income in incomes:
            # Begin with today's Dates
            paydates = [
                i for i in range(income[0],
                                 days.span_length(span),
                                 income[1])
            ]
            paydays.append(paydates)
        return paydates

    def Expense(self, range_end, span):
        daily = []
        other = []
        ExpenseList.weekly = ("weekly",
                              Comp.weekly(0, days.span_length(span)),
                              "0.00")
        ExpenseList.biweekly = ("biweekly",
                                Comp.biweekly(0, days.span_length(span)),
                                "0.00")
        for expense in self.expense_list:
            # Round expense to two decimal places and
            # append each occuring expense to its respectable
            # list
            expense.price = round(float(expense.price), 2)
            if expense.occurence == "2":
                date = int(expense.expenseDate)
                ExpenseList.weekly = ("weekly",
                                      Comp.weekly(date, days.span_length(span)),
                                      expense.price)
            elif expense.occurence == "1":
                daily.append(expense.price)
            elif expense.occurence == "3":
                other.append(expense.price)
            elif expense.occurence == "4":
                date = int(expense.expenseDate)
                ExpenseList.biweekly = ("biweekly",
                                        Comp.biweekly(date, days.span_length(span)),
                                        expense.price)
        # Add each expense in each category and return it
        if len(daily) == 0:
            daily.append(0)
        if len(other) == 0:
            other.append(0)
        return [sum(daily), sum(other)]


class Occurence:
    def __init__(self):
        self.totals = []
        self.dailyExpenses = []

    def range_span(self, span):
        rspan = [[], []]
        for i in range(len(self.deduct)):
            if self.deduct[i] != 0:
                self.range_end = days.span_length(span)
                if i == 1:
                    rspan.insert(0, Comp.other_span(self.range_end))
                if i == 0:
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
        if (len(self.dailyExpenses) < len(self.label_span)):
            if self.deduct[1] == 0:
                self.daily_append()
            else:
                self.other_append()
        return self.dailyExpenses

    def range_calc(self, span):
        self.range_end = days.span_length(span)
        self.deduct = Lists().Expense(self.range_end, span)
        weekday = Dates.weekday
        Lists().Income(self.range_end)
        ExpenseList.daily = ("daily", self.range_calc2(span), self.deduct[0])
        return Calc.enum_balance(
            Lists().paydates(weekday, span),
            self.deduct)


def delete():
    dates.delete()


Calc = Calculate()
dates = Dates.Labels()
Comp = Comprehensions()
days = Dates.Dates()
