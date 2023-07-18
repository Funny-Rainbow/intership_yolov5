import datetime

yesterday = datetime.date.today() + datetime.timedelta(-1)
print(yesterday)