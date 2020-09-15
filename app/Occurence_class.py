from collections import deque
import app.Dates as Dates
from app.Calculate import Calculate
from app.Lists import ExpenseList, Comprehensions, Lists


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
        '''
        This is the complicated part, set label ranges for
        each expense occurence, then add to a weekly range.
        '''
        self.label_span = self.range_span(span)
        if (len(self.dailyExpenses) < len(self.label_span)):
            if self.deduct[1] == 0:
                self.daily_append()
            else:
                self.other_append()
        return self.dailyExpenses

    def range_calc(self, span):
        self.range_end = days.span_length(span)
        self.deduct = List.Expense(self.range_end, span)
        weekday = Dates.weekday
        List.Income(self.range_end)
        ExpenseList.daily = ("daily",
                             self.range_calc2(span),
                             self.deduct[0])
        return Calc.enum_balance(
            List.paydates(weekday, span),
            self.deduct)


def delete():
    dates.delete()


List = Lists()
Calc = Calculate()
dates = Dates.Labels()
Comp = Comprehensions()
days = Dates.Dates()
