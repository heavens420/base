import time
import datetime

while 0:
    now = time.time()
    print(now)
    print(round(now))
    time.sleep(1)


def return_two():
    a = 1 / 0
    return 1, 2


# a, b = return_two()
# print(f'{a} -- {b}')
# print(time.time() - 1631424430793 / 1000.0)


#
# print(type(time.time()))
#
# print(1631600537111222.8012824 + 0.33333 > 1631600537111222.3012824 + 0.11111)
# print(1631600537.3012824+0.1)
#
# print(datetime.datetime.now())

def another_method():
    try:
        a, b = return_two()
        print(f'{a} -- {b}')
    except Exception as e:
        print(e)


# another_method()

a1 = "2021-9-15 14:46:00"
timeArray = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
# print(timeArray)
timeStamp = int(time.mktime(timeArray))
print(timeStamp)
print(time.time() - timeStamp)

print(list() == list(set()))

print('-----------------------------------')

s2 = set()
li = list()
for i in range(99999):
    s2.add(i)
    li.append(i)

start = time.time()
ss = set(li)
ss = list(s2)
# if li != list() and set != set():
#     pass
# for i in li:
#     for j in s2:
#         pass
end = time.time()
print(end - start)
