import app.Dates as Dates
from app.models import Income, Expense


class IncomeList():
    pass


class ExpenseList():
    pass


class Lists():
    def __init__(self):
        '''
        Query tables
        '''
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
                    ("existing", [0], income.price, income.payday))
            if income.occurence == "2":
                IncomeList.recurring.append(
                    ("weekly", Comp.weekly(int(income.payday), range_end),
                     income.price, income.payday, 7))
            if income.occurence == "4":
                IncomeList.recurring.append(
                    ("biweekly", Comp.biweekly(int(income.payday), range_end),
                     income.price, income.payday, 14))

    def paydates(self, weekday, span):
        paydays = []
        if len(IncomeList.existing) < 1:
            IncomeList.existing.append(('None', [0], '0', '0', '1'))
        if len(IncomeList.recurring) < 1:
            IncomeList.recurring.append(('None', [0], '0', '0', '7'))
        for paydates in IncomeList.recurring:
            '''
            Begin with today's Dates
            '''
            print(paydates[3])
            print(paydates[4])
            paydates = [
                i
                for i in range(int(paydates[3]),
                               Dates.Dates().ordinal +
                               days.span_length(span), int(paydates[4]))
            ]
            paydays.append(paydates)
        return paydays

    def Expense(self, range_end, span):
        daily = []
        other = []
        ExpenseList.weekly = ("weekly", Comp.weekly(0, days.span_length(span)),
                              "0.00")
        ExpenseList.biweekly = ("biweekly",
                                Comp.biweekly(0,
                                              days.span_length(span)), "0.00")
        for expense in self.expense_list:
            '''
            Round expense to two decimal places and
            append each occuring expense to its respectable
            list
            '''
            expense.price = round(float(expense.price), 2)
            if expense.occurence == "2":
                date = int(expense.expenseDate)
                ExpenseList.weekly = ("weekly",
                                      Comp.weekly(
                                          date, date + days.span_length(span)),
                                      expense.price)
            elif expense.occurence == "1":
                daily.append(expense.price)
            elif expense.occurence == "3":
                other.append(expense.price)
            elif expense.occurence == "4":
                date = int(expense.expenseDate)
                ExpenseList.biweekly = ("biweekly",
                                        Comp.biweekly(
                                            date,
                                            date + days.span_length(span)),
                                        expense.price)
            elif expense.occurence == "5":
                date = int(expense.expenseDate)
                ExpenseList.monthly = ("monthly",
                                       Comp.biweekly(
                                           date,
                                           date + days.span_length(span)),
                                       expense.price)
        '''
        Add each expense in each category and return it
        '''
        if len(daily) == 0:
            daily.append(0)
        if len(other) == 0:
            other.append(0)
        return [sum(daily), sum(other)]


class Comprehensions():
    '''
    # List comprehensions for the labels
    '''
    def weekly(self, start, range_end):
        return [i for i in range(start, range_end, 7)]

    def biweekly(self, start, range_end):
        return [i for i in range(start, range_end, 14)]

    def monthly(self, start, range_end):
        return [i for i in range(start, range_end, 30)]

    def daily_span(self, range_end):
        return [day for day in range(0, range_end)]

    def other_span(self, range_end):
        return [day for day in range(0, range_end, 2)]

    def other_add(self, deduct, label_span):
        daily = label_span[1]
        other = label_span[0]
        return [deduct[0] + deduct[1] for d in daily for o in other if d == o]

    def no_other(self, deduct, daily):
        return [deduct[0] for day in daily]

    def daily_add(self, deduct, otherInsert):
        return [deduct[0] for day in range(len(otherInsert))]

    def deduct_list(self, occurence):
        return [i for i in occurence]

    def stacked_list(self, occurence):
        return [i for elem in occurence for i in elem]

    def paydates(self, paydates):
        return [args for args in paydates for args in args]

    def prices(self):
        return [(float(existing[2]), float(recurring[2])) for existing in IncomeList.existing
                for recurring in IncomeList.recurring]


dates = Dates.Labels()
Comp = Comprehensions()
days = Dates.Dates()
