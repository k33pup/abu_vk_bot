import datetime


a = datetime.datetime.today()
future_date = datetime.datetime.today() - datetime.timedelta(minutes=5)
print(future_date)