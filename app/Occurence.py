import app.Dates as Dates
from app.models import Expense, Income


totals = []


# Please change this to a more professional name
total_dict = {"day": 0, "payday": False, "value": 5.00, }

# total_dict['day'] = 1
# print(total_dict['day'])
# totals.append(total_dict)
# print(totals[0]['day'])


class Occurences():
    pass

week = Occurences()

for x in range(len[totals]):
    week.day = totals[x]['day']
    week.payday = totals[x]['payday']
    week.value = totals[x]['value']

def occurence_list(label, income_list, expense_list):

    def calc(price, payday, deduct, range_end):
        total = price
        for t in range(1, range_end):
            print(total, deduct, t)
            pdy = False
            if t >= payday:
                total = float(price) - deduct * t
            if t < payday:
                total = float(price) - deduct * t
            if t == payday:
                pdy = True
            if t != payday:
                pdy = False
            totals.insert(t, total)
            total_dict = { 'day': t, 'payday': pdy, 'value': total}

    def range_calc(payday, price, occurence):
        # deduct = [i for elem in occurence for i in elem]
        deduct = [i for i in occurence]
        range_end = 0
        totals.insert(int(payday), price)
        if deduct[0] != 0:
            range_end = 1
            deduct = deduct[0]
            calc(price, payday, deduct, range_end)
        elif deduct[1] != 0:
            range_end = 8
            deduct = deduct[1]
            calc(price, payday, deduct, range_end)
        elif deduct[2] != 0:
            range_end = 7
            deduct = deduct[2]
            calc(price, payday, deduct, range_end)

    def occurence_parse(payday, price):
        weekly = []
        other = []
        daily = []
        for expense in expense_list:
            expense.price = round(float(expense.price), 2)
            if expense.occurence == "2":
                weekly.append(expense.price)
            elif expense.occurence == "1":
                daily.append(expense.price)
            elif expense.occurence == "3":
                other.append(expense.price)
        occurence = [sum(weekly), sum(other), sum(daily)]
        range_calc(payday, price, occurence)

    for income in income_list:
        if income.price is not None:
            price = income.price
            payday = int(income.payday)
            print(payday)
            for x in range(7):
                totals.append([])
            if label == "1":
                payday = 0
            if label == "2":
                payday = payday - int(Dates.weekday)
            print(payday)
            occurence_parse(payday, price)
        else:
            price = 0
    return totals
