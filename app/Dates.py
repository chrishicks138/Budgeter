import datetime
import time

x = datetime.datetime.now()
today = x.strftime("%m-%d")
date = x.strftime("%m-%d-%Y")
weekday = datetime.datetime.strptime(date, "%m-%d-%Y").weekday() + 1


class Now():

    def start(self):
        now = time.time_ns()
        return now

    def end(self):
        now = time.time_ns()
        return now

    def result(self):
        nanoseconds = (self.end() - self.start())
        print(nanoseconds)
        milliseconds, nanoseconds = divmod(nanoseconds, 1000)
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return (days, hours, minutes, seconds, milliseconds, nanoseconds)


class Labels():
    def __init__(self):
        self.today_label = []

    def add_today_label(self, data):
        self.today_label.append(data)

    def delete(self):
        self.today_label = []

    def label_chooser(self):
        return self.today_label


labels = Labels()


class Comprehensions():
    d = [datetime.datetime.fromordinal(day).strftime("%m-%d") for day in range(datetime.datetime.toordinal(x), datetime.datetime.toordinal(x) + 365)]


class Dates:
    def __init__(self):
        self.dates = [datetime.datetime.fromordinal(day).strftime("%m-%d") for day in range(datetime.datetime.toordinal(x), datetime.datetime.toordinal(x) + 365)]

    def span_length(self, span):
        week = 7
        if span == "1":
            week = week + 1
        if span == "2":
            week = week * 2
        if span == "3":
            week = week * 4
        if span == "4":
            week = week * 12
        if span == "5":
            week = week * 24
        return week

    def today_b(self, e):
        return e

    def today_e(self, e, span):
        # result = e + 90
        result = e + self.span_length(span)
        return result

    def date_selector(self, span):
        for e, d in enumerate(self.dates):
            if today in d:
                for i in range(self.today_b(e), self.today_e(e, span)):
                    labels.add_today_label(self.dates[i])

    def label(self):
        return labels.label_chooser()
