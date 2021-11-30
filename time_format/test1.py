import datetime

now = datetime.datetime.now()
print(now)

now_f1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(now_f1)

now_f2 = datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
print(now_f2)
