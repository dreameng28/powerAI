import datetime


def str2time(str_time):
    t = str_time.split('/')
    d = datetime.date(int(t[0]), int(t[1]), int(t[2]))
    return d


def day_duration(sd1, sd2):
    d1 = str2time(sd1)
    d2 = str2time(sd2)
    return (d2 - d1).days


def date2day(date2):
    return day_duration('2014/12/29', date2) % 7 + 1
