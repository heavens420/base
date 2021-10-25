import pyautogui as po
import time

# time.sleep(3)
x, y = po.position()
print(x, y)

po.click(1438, 1064)
time.sleep(1)
po.rightClick(972, 355)

po.click(1024, 467)
# time.sleep(3)
po.click(942, 548, duration=1)
# time.sleep(2)
po.doubleClick(1050, 528)
time.sleep(3)
po.hotkey('ctrl','a')
time.sleep(2)
# name = po.hotkey('ctrl','c')
# cv = po.hotkey('ctrl','v')
# print(cv)
# print(name)
# po.write("xiangpeng")

po.hotkey("Tab")
po.hotkey("Backspace")
po.write("@ZXPzxp4")
# time.sleep(5)
time.sleep(3)
x, y = po.position()
print(x, y)
